# AI Key Server

## Usage

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure `random_messages_dataset.csv` is in this folder.

3. Start the server:
   ```
   python app.py
   ```

4. POST to http://localhost:5001/generate-key with:
   ```
   {
     "messages": ["msg1", "msg2", ...],
     "session_id": "s1",
     "sender_id": "alice",
     "receiver_id": "bob"
   }
   ```
   Returns: `{ "key": "<hex key>" }`