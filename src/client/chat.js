// chat.js - fixed streaming version with debug 

const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let sessionId = null;
let userName = null;

// Start by asking for name
addMessage("What is your name?");

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, true);
  userInput.value = '';

  if (!userName) {
    userName = text;
    sessionId = "user_" + userName.toLowerCase().replace(/\s+/g, "_") + "_" + Date.now();
    await streamResponse("", userName); // send name on first message
    return;
  }

  await streamResponse(text);
}

async function streamResponse(message, name = null) {
  console.log("[JS] Sending request:", { session_id: sessionId, message, name });

  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        message: message,
        name: name
      })
    });

    console.log("[JS] Response status:", res.status);

    if (!res.body) {
      console.error("[JS] No stream body");
      addMessage("[ERROR] No stream received.");
      return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    // Create the agent message element once
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', 'agent');
    if (Math.random() > 0.7) messageElement.classList.add('glitch');
    messagesDiv.appendChild(messageElement);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    // In streamResponse, after creating messageElement:
    const typingText = document.createElement('span');
    typingText.classList.add('typing-text');
    typingText.textContent = 'Agent Smith is typing...';
    messageElement.appendChild(typingText);

    // Blink animation via CSS (add to styles.css)

    let fullReply = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        console.log("[JS] Stream complete. Final reply:", fullReply);
        break;
      }

      const chunk = decoder.decode(value);
      console.log("[JS] Raw chunk:", chunk);

      // Split into lines (SSE can send multiple in one chunk)
      const lines = chunk.split('\n');
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed) continue;

        if (trimmed.startsWith('data: ')) {
          const dataStr = trimmed.slice(6).trim();
          console.log("[JS] Data:", dataStr);

          if (dataStr === '[DONE]') {
            console.log("[JS] [DONE] received");
            break;
          }

          try {
            const data = JSON.parse(dataStr);
            if (data.chunk) {
              fullReply += data.chunk;
              messageElement.textContent = fullReply;
              messagesDiv.scrollTop = messagesDiv.scrollHeight;
              console.log("[JS] Appended:", data.chunk);
            }
          } catch (e) {
            console.error("[JS] Parse error:", e, "on:", dataStr);
          }
        }
      }
    }
  } catch (err) {
    console.error("[JS] Fetch/stream error:", err);
    addMessage("[ERROR] Connection failed.");
  }
}

sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
  if (e.key === 'Enter') {
    sendMessage();
  }
});

function addMessage(text, isUser = false) {
  const msg = document.createElement('div');
  msg.classList.add('message');
  msg.classList.add(isUser ? 'user' : 'agent');
  if (!isUser && Math.random() > 0.7) {
    msg.classList.add('glitch');
  }
  msg.textContent = text;
  messagesDiv.appendChild(msg);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}