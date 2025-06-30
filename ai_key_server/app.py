from flask import Flask, request, jsonify
from flask_cors import CORS
from keygen import generate_dynamic_key, DUMMY_MESSAGES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)
CORS(app)  # Enable CORS

# In-memory chat storage
chats = {}

def encrypt_message(plaintext, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ct = encryptor.update(padded) + encryptor.finalize()
    return iv + ct  # IV prepended

def decrypt_message(ciphertext, key):
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    pt = unpadder.update(padded) + unpadder.finalize()
    return pt.decode()

@app.route('/send', methods=['POST'])
def send():
    data = request.json
    session_id = data['session_id']
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    message = data['message']
    
    messages = chats.get(session_id, [])
    key = generate_dynamic_key(messages, session_id, sender_id, receiver_id)
    ciphertext = encrypt_message(message, key)
    chats.setdefault(session_id, []).append(message)

    # === PRINT INFO ONLY ON SEND ===
    print("----- MESSAGE SENT -----")
    print(f"Sender         : {sender_id}")
    print(f"Message        : {message}")
    print(f"Encryption Key : {key.hex()}")
    print(f"Cipher Text    : {ciphertext.hex()}")
    print("------------------------\n")
    
    return jsonify({
        'ciphertext': ciphertext.hex()
    })

@app.route('/receive', methods=['POST'])
def receive():
    data = request.json
    session_id = data['session_id']
    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    ciphertext = bytes.fromhex(data['ciphertext'])
    
    messages = chats.get(session_id, [])
    key = generate_dynamic_key(messages, session_id, sender_id, receiver_id)
    plaintext = decrypt_message(ciphertext, key)
    chats.setdefault(session_id, []).append(plaintext)

    # NO PRINT STATEMENTS HERE

    return jsonify({
        'message': plaintext
    })

@app.route('/generate-key', methods=['POST'])
def generate_key():
    data = request.json
    messages = data.get('messages', [])
    session_id = data.get('session_id', '')
    sender_id = data.get('sender_id', '')
    receiver_id = data.get('receiver_id', '')
    key = generate_dynamic_key(messages, session_id, sender_id, receiver_id)
    return jsonify({'key': key.hex()})

@app.route('/')
def index():
    return "LSTM AI Key Server is running."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
