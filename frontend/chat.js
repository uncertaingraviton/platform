const API_URL = "/chat"; // Adjust if backend is on a different host/port
const STREAM_URL = "/chat/stream";

const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const chatMessages = document.getElementById("chat-messages");

function appendMessage(text, sender) {
  const msg = document.createElement("div");
  msg.className = `chat-msg ${sender}`;
  msg.textContent = text;
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage(userText) {
  appendMessage(userText, "user");
  appendMessage("...", "assistant");
  try {
    // Use streaming endpoint for fast feedback
    const response = await fetch(STREAM_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_input: userText, stream: true })
    });
    if (!response.body) throw new Error("No response body");
    const reader = response.body.getReader();
    let assistantMsg = "";
    let done = false;
    // Remove the placeholder '...'
    chatMessages.removeChild(chatMessages.lastChild);
    const msgDiv = document.createElement("div");
    msgDiv.className = "chat-msg assistant";
    chatMessages.appendChild(msgDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    while (!done) {
      const { value, done: doneReading } = await reader.read();
      done = doneReading;
      if (value) {
        const chunk = new TextDecoder().decode(value);
        assistantMsg += chunk;
        msgDiv.textContent = assistantMsg;
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }
    }
  } catch (err) {
    chatMessages.removeChild(chatMessages.lastChild);
    appendMessage("[Error] " + err.message, "assistant");
  }
}

chatForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const userText = chatInput.value.trim();
  if (!userText) return;
  chatInput.value = "";
  sendMessage(userText);
}); 