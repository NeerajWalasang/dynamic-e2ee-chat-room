// src/backendService.js

export async function sendMessage(sessionId, senderId, receiverId, message) {
  const response = await fetch("http://localhost:5001/send", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      sender_id: senderId,
      receiver_id: receiverId,
      message,
    }),
  });
  return await response.json(); // { ciphertext: ... }
}

export async function receiveMessage(sessionId, senderId, receiverId, ciphertext) {
  const response = await fetch("http://localhost:5001/receive", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      session_id: sessionId,
      sender_id: senderId,
      receiver_id: receiverId,
      ciphertext,
    }),
  });
  return await response.json(); // { message: ... }
}
