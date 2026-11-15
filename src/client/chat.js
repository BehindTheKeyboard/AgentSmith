// Chat and permanent scan terminal. Consumes the existing /chat SSE protocol.
'use strict';

const messagesDiv = document.getElementById('messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatStatus = document.getElementById('chat-status');
let sessionId = null;
let sending = false;

addMessage(
  "How did you find this terminal? Tell me your name, or ask a question. " +
  "You can introduce yourself anytime by saying 'My name is' followed by your name."
);

function scrollChat() { messagesDiv.scrollTop = messagesDiv.scrollHeight; }

function addMessage(text, isUser = false) {
  const element = document.createElement('div');
  element.classList.add('message', isUser ? 'user' : 'agent');
  if (!isUser && Math.random() > 0.7) {
    element.classList.add('glitch');
    element.style.animationDelay = `0s, ${Math.random() * 10}s`;
  }
  element.textContent = text;
  messagesDiv.appendChild(element);
  scrollChat();
  return element;
}

async function sendMessage() {
  const text = userInput.value.trim();
  if (!text || sending) return;
  sending = true;
  sendBtn.disabled = true;
  chatStatus.textContent = 'RESPONDING';
  userInput.value = '';
  addMessage(text, true);

  try {
    if (!sessionId) {
      sessionId = 'session_' + (globalThis.crypto?.randomUUID?.() ||
        `${Date.now()}_${Math.random().toString(36).slice(2)}`);
    }
    await streamResponse(text);
  } finally {
    sending = false;
    sendBtn.disabled = false;
    chatStatus.textContent = 'READY';
  }
}

document.getElementById('chat-form').addEventListener('submit', (event) => {
  event.preventDefault();
  sendMessage();
});

async function streamResponse(message, name = null) {
  const messageElement = addMessage('');
  const typingText = document.createElement('span');
  typingText.className = 'typing-text';
  typingText.textContent = 'Agent Smith is typing...';
  messageElement.appendChild(typingText);
  let fullReply = '';
  let reader;
  let completed = false;

  function consumeEvent(frame) {
    const dataText = frame.split(/\r?\n/)
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).replace(/^ /, ''))
      .join('\n');
    if (!dataText) return;
    if (dataText.trim() === '[DONE]') { completed = true; return; }
    const data = JSON.parse(dataText);
    if (data.scan) {
      console.debug('[SCAN] Received:', data.scan);
      window.matrixScanTerminal(data.scan);
    }
    if (typeof data.chunk === 'string' && data.chunk) {
      const follow = messagesDiv.scrollHeight - messagesDiv.scrollTop - messagesDiv.clientHeight < 90;
      fullReply += data.chunk;
      messageElement.textContent = fullReply;
      if (follow) scrollChat();
    }
  }

  try {
    const response = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message, name }),
    });
    if (!response.ok) throw new Error(`Chat request failed (HTTP ${response.status}).`);
    if (!response.body) throw new Error('No response stream was received.');
    reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (!completed) {
      const { done, value } = await reader.read();
      buffer += done ? decoder.decode() : decoder.decode(value, { stream: true });
      let boundary;
      while (!completed && (boundary = /\r?\n\r?\n/.exec(buffer))) {
        const frame = buffer.slice(0, boundary.index);
        buffer = buffer.slice(boundary.index + boundary[0].length);
        consumeEvent(frame);
      }
      if (done) {
        if (!completed && buffer.trim()) consumeEvent(buffer);
        break;
      }
    }

    if (!fullReply.trim()) {
      messageElement.textContent = '[No text response received. Check the client log.]';
    } else if (!completed) {
      messageElement.textContent += '\n[Connection ended before the response finished.]';
    }
    // Only an unfinished scan changes state; completed findings remain visible.
    window.matrixScanTerminal({ action: 'interrupted', message: 'Chat stream ended before scan completion.' });
  } catch (error) {
    console.error('[CHAT] Streaming failed:', error);
    messageElement.textContent = (fullReply ? fullReply + '\n' : '') +
      '[ERROR] ' + error.message;
    window.matrixScanTerminal({ action: 'error', message: 'Chat connection or stream failed.' });
  } finally {
    if (reader) {
      try { await reader.cancel(); } catch { /* Already closed or disconnected. */ }
      reader.releaseLock();
    }
    scrollChat();
  }
}

// Permanent panel; same window.matrixScanTerminal(event) interface as before.
(() => {
  const panel = document.getElementById('matrix-scan-terminal');
  const output = document.getElementById('scan-output');
  const status = document.getElementById('scan-status');
  const badge = document.getElementById('scan-state');
  const results = document.getElementById('scan-results');
  const operation = document.getElementById('scan-operation');
  const location = document.getElementById('scan-location');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const toolNames = { scan_matrix: 'Matrix anomaly scan', scan_for_agents: 'Nearby agent scan', scan_agents: 'Nearby agent scan', detect_the_one: 'Candidate investigation' };
  const characters = Array.from('零壱弐参四五六七八九電脳仮想空間接続解析情報異常探索アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ<>[]{}:=+-*/     ');
  let timer = null;
  let running = false;
  let started = 0;
  let generated = 0;
  let retainedLines = [];

  function readable(value) { return String(value ?? '').replaceAll('_', ' '); }
  function stopTimer() { clearInterval(timer); timer = null; }
  function randomInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
  function createCodeLine() {
    return Array.from({ length: randomInt(12, 64) }, () => characters[randomInt(0, characters.length - 1)]).join('');
  }
  function appendLines(lines) {
    retainedLines.push(...lines);
    retainedLines = retainedLines.slice(-500);
    output.textContent = retainedLines.join('\n');
    output.scrollTop = output.scrollHeight;
  }
  function addText(parent, text, tag = 'p', className = '') {
    const node = document.createElement(tag);
    node.textContent = text;
    if (className) node.className = className;
    parent.appendChild(node);
    return node;
  }
  function showResult(message, action) {
    results.replaceChildren();
    let data = message;
    if (typeof message === 'string') {
      try { data = JSON.parse(message); } catch { /* Plain-text tool response. */ }
    }
    if (!data || typeof data !== 'object' || Array.isArray(data)) {
      addText(results, String(message || (action === 'complete' ? 'Scan complete.' : 'Scan stopped.')));
      return false;
    }
    if (data.location_name) location.textContent = data.location_name;
    if (data.error) addText(results, String(data.error));
    if (data.message) addText(results, String(data.message));
    if (typeof data.threat === 'boolean') {
      addText(results, data.threat ? 'Potential threat reported.' : 'No active threat reported by this scan.');
    }
    if (Array.isArray(data.findings)) {
      data.findings.forEach((finding) => {
        if (!finding || typeof finding !== 'object') {
          addText(results, String(finding));
          return;
        }
        const card = document.createElement('article');
        card.className = 'finding' + (finding.threat ? ' threat' : '');
        addText(card, readable(finding.agent || finding.title || finding.id || 'Finding'), 'h4');
        if (finding.alignment) addText(card, `Alignment: ${readable(finding.alignment)}`, 'p', 'muted');
        if (typeof finding.threat === 'boolean') addText(card, finding.threat ? 'Threat activity detected' : 'No hostile activity observed', 'p', 'muted');
        if (finding.severity) addText(card, `Severity: ${readable(finding.severity)}`, 'p', 'muted');
        if (finding.description) addText(card, String(finding.description));
        if (finding.activity) addText(card, String(finding.activity));
        results.appendChild(card);
      });
    } else if (!data.message && !data.error) {
      addText(results, JSON.stringify(data, null, 2), 'pre', 'result-raw');
    }
    return Boolean(data.error);
  }

  window.matrixScanTerminal = (event) => {
    if (!event || !event.action) return;
    if (event.action === 'start') {
      stopTimer();
      running = true;
      started = Date.now();
      generated = 0;
      panel.dataset.state = 'running';
      badge.textContent = 'SCANNING';
      operation.textContent = toolNames[event.tool] || readable(event.tool || 'Matrix scan');
      location.textContent = readable(event.location_name || event.location || event.environment || 'Local sector');
      retainedLines = [];
      appendLines(['> System scan initiated.', '> Awaiting tool result...']);
      results.replaceChildren();
      addText(results, 'Scan in progress. Findings will appear here.', 'p', 'muted');
      status.textContent = 'Scanning… awaiting tool result.';
      if (reducedMotion.matches) return;
      const targetLines = randomInt(100, 1000);
      timer = setInterval(() => {
        const elapsed = Date.now() - started;
        const expected = Math.floor(Math.min(elapsed / 2400, 1) * targetLines);
        const batch = [];
        while (generated < expected) { batch.push(createCodeLine()); generated++; }
        if (batch.length) appendLines(batch);
        status.textContent = `Scanning · ${generated} code lines · awaiting tool result`;
        // Animation is decorative. Completion comes only from the backend event.
        if (generated >= targetLines) stopTimer();
      }, 60);
      return;
    }
    if (!running || !['complete', 'error', 'interrupted'].includes(event.action)) return;
    stopTimer();
    running = false;
    const toolFailed = showResult(event.message, event.action);
    const action = toolFailed ? 'error' : event.action;
    panel.dataset.state = action;
    badge.textContent = action === 'complete' ? 'COMPLETE' : action === 'error' ? 'ERROR' : 'STOPPED';
    appendLines([`> ${badge.textContent} / see findings below.`]);
    status.textContent = action === 'complete'
      ? `Scan complete · ${((Date.now() - started) / 1000).toFixed(1)}s`
      : 'Scan stopped. Details are shown below.';
  };
})();
