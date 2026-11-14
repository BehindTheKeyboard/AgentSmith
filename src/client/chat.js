// chat.js - fixed streaming version with debug 

const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

let sessionId = null;
let userName = null;

// Start by asking for name

addMessage(
  "Well, hello. Tell me your name. If you don't not want to reveal your identity, you can ask a question instead. " +
  "Introduce yourself anytime by saying 'My name is' and your name."
);

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, true);
  userInput.value = '';

  if (!sessionId) {
    sessionId = "session_" + crypto.randomUUID();
  }

  // Always send the actual message.
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
    let sseBuffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        window.matrixScanTerminal({ action: 'interrupted', message: 'Stream ended before scan completion.' });
        console.log("[JS] Stream complete. Final reply:", fullReply);
        break;
      }

      const chunk = decoder.decode(value, { stream: true });
      console.log("[JS] Raw chunk:", chunk);

      // Split into lines (SSE can send multiple in one chunk)
      sseBuffer += chunk;
      const lines = sseBuffer.split('\n');
      sseBuffer = lines.pop();
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
            if (data.scan) {
              window.matrixScanTerminal(data.scan);
              continue;
            }
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
    window.matrixScanTerminal({ action: 'error', message: 'Connection failed.' });
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

// MATRIX_SCAN_POPUP_V1: embedded terminal; no HTML or CSS file changes needed.
(() => {
  let dialog;
  let output;
  let status;
  let timer = null;
  let running = false;

  function stopTimer() {
    clearInterval(timer);
    timer = null;
  }

  function createTerminal() {
    if (dialog) return;

    const style = document.createElement('style');
    style.textContent = `
      #matrix-scan-terminal {
        box-sizing: border-box; width: min(640px, 92vw); max-height: 80vh;
        background: #050b07; color: #79ff9c; border: 1px solid #35b961;
        border-radius: 8px; padding: 20px; box-shadow: 0 0 35px #24ac4040;
        font: 14px/1.6 Consolas, monospace;
      }
      #matrix-scan-terminal::backdrop { background: #000a; }
      #matrix-scan-terminal header {
        display: flex; justify-content: space-between; align-items: center;
        gap: 16px; margin-bottom: 16px;
      }
      #matrix-scan-terminal button {
        background: #102418; color: #a0ffb9; border: 1px solid #35b961;
        padding: 5px 12px; border-radius: 4px; cursor: pointer;
      }
      #matrix-scan-terminal pre { white-space: pre-wrap; overflow-wrap: anywhere; }
    `;
    document.head.appendChild(style);

    dialog = document.createElement('dialog');
    dialog.id = 'matrix-scan-terminal';
    dialog.setAttribute('aria-labelledby', 'matrix-scan-title');

    const header = document.createElement('header');
    const title = document.createElement('strong');
    title.id = 'matrix-scan-title';
    title.textContent = 'MATRIX // SCAN TERMINAL';
    const close = document.createElement('button');
    close.type = 'button';
    close.textContent = 'Close';
    close.addEventListener('click', () => dialog.close());
    header.append(title, close);

    output = document.createElement('pre');
    status = document.createElement('div');
    status.setAttribute('role', 'status');
    dialog.append(header, output, status);
    dialog.addEventListener('close', stopTimer);
    document.body.appendChild(dialog);
  }

  window.matrixScanTerminal = (event) => {
    createTerminal();
    if (event.action === 'start') {
      stopTimer();
      running = true;
      output.textContent =
        'System Scan INITIATED.\n' +
        '> ' + (event.tool || 'scan_matrix') + ' ' +
        (event.location || 'local sector') + '\n' +
        '[START] Tool execution started.\n';
      status.textContent = '[SCAN] Scanning...';
      if (!dialog.open) dialog.showModal();
      
            const started = Date.now();

      const characters = Array.from(
        '零壱弐参四五六七八九電脳仮想空間接続解析情報異常探索' +
        'アイウエオカキクケコサシスセソタチツテトナニヌネノ' +
        'ハヒフヘホマミムメモヤユヨラリルレロワヲン' +
        '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<>[]{}:=+-*/' +
        ' '
      );

      function randomInt(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
      }

      function createCodeLine() {
        const length = randomInt(12, 90);
        let line = '';

        for (let i = 0; i < length; i++) {
          line += characters[randomInt(0, characters.length - 1)];
        }

        return line;
      }

      // Choose a new amount for every scan.
      const targetLines = randomInt(100, 1000);
      const animationDuration = 2400;
      let linesWritten = 0;

      output.style.maxHeight = '280px';
      output.style.overflowY = 'auto';
      output.style.fontFamily =
        '"Yu Gothic", "Meiryo", Consolas, monospace';

      timer = setInterval(() => {
        const elapsed = Date.now() - started;

        // Spread the chosen number of lines across the animation.
        const progress = Math.min(elapsed / animationDuration, 1);
        const expectedLines = Math.floor(progress * targetLines);
        const batch = [];

        while (linesWritten < expectedLines) {
          batch.push(createCodeLine());
          linesWritten++;
        }

        if (batch.length > 0) {
          output.textContent += batch.join('\n') + '\n';
          output.scrollTop = output.scrollHeight;
        }

        status.textContent =
          `[SCAN] ${linesWritten} code lines generated — awaiting tool result`;
      }, 40);

    } else if (running && ['complete', 'error', 'interrupted'].includes(event.action)) {
      stopTimer();
      running = false;
      output.textContent += (event.action === 'complete' ? '[RESULT] ' : '[ERROR] ') +
        (event.message || 'Scan interrupted.') + '\n';
      status.textContent = event.action === 'complete' ? '[DONE] Scan complete.' : '[STOPPED]';
    }
  };
})();
