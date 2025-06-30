import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Embedding, Dense
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import hashlib

VOCAB_SIZE = 5000
EMBED_DIM = 128
LSTM_UNITS = 256
KEY_BYTES = 32
SEQ_LEN = 20

df = pd.read_csv('random_messages_dataset.csv')
if 'message' in df.columns:
    DUMMY_MESSAGES = df['message'].astype(str).tolist()[:5]
else:
    DUMMY_MESSAGES = [
        "Welcome to secure chat!",
        "Initializing session...",
        "Encryption handshake started.",
        "Let us begin your private conversation.",
        "Default message to start LSTM state."
    ]

tokenizer = Tokenizer(num_words=VOCAB_SIZE, oov_token="<OOV>")
tokenizer.fit_on_texts(DUMMY_MESSAGES)

def prepare_input(messages, session_id, sender_id, user_id, seq_len=SEQ_LEN):
    if not messages:
        messages = DUMMY_MESSAGES
    concat = ' '.join(messages) + f" SESSION:{session_id} SENDER:{sender_id} USER:{user_id}"
    seq = tokenizer.texts_to_sequences([concat])
    seq_pad = pad_sequences(seq, maxlen=seq_len, padding='pre', truncating='pre')
    return seq_pad

def build_model():
    model = Sequential([
        Embedding(VOCAB_SIZE, EMBED_DIM, input_length=SEQ_LEN),
        LSTM(LSTM_UNITS, return_sequences=False),
        Dense(KEY_BYTES, activation='linear')
    ])
    return model

model = build_model()

def generate_dynamic_key(messages, session_id, sender_id, user_id):
    inp = prepare_input(messages, session_id, sender_id, user_id)
    key_raw = model.predict(inp, verbose=0)[0]
    key_bytes = np.clip(key_raw, 0, 255).astype(np.uint8).tobytes()
    final_key = hashlib.sha256(key_bytes).digest()
    return final_key