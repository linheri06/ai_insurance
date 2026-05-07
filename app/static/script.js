// async function sendMessage() {
//     const input = document.getElementById("user-input");
//     const chatBox = document.getElementById("chat-box");

//     const message = input.value;
//     if (!message) return;

//     // Hiển thị user
//     chatBox.innerHTML += `<div class="message user">${message}</div>`;

//     input.value = "";

//     // Gửi API
//     const response = await fetch("/ask", {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify({ query: message })
//     });

//     const data = await response.json();

//     // Hiển thị bot
//     chatBox.innerHTML += `<div class="message bot">${data.answer}</div>`;

//     chatBox.scrollTop = chatBox.scrollHeight;
// }
// ===== Tiện ích =====
function getTime() {
    return new Date().toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
}

function scrollToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ===== Hiển thị tin nhắn =====
function appendMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');

    const row = document.createElement('div');
    row.className = 'message-row ' + (sender === 'user' ? 'user-row' : 'bot-row');

    const initials = sender === 'user' ? 'BN' : 'BH';
    const avatarClass = sender === 'user' ? 'user-av' : 'bot-av';
    const alignClass = sender === 'user' ? '' : '';

    row.innerHTML = `
        <div class="avatar ${avatarClass}">${initials}</div>
        <div class="bubble-wrap">
            <div class="message ${sender}">${text}</div>
            <span class="msg-time">${getTime()}</span>
        </div>
    `;

    chatBox.appendChild(row);
    scrollToBottom();
}

// ===== Typing indicator =====
function showTyping() {
    const chatBox = document.getElementById('chat-box');
    const row = document.createElement('div');
    row.className = 'typing-row';
    row.id = 'typing-indicator';
    row.innerHTML = `
        <div class="avatar bot-av">BH</div>
        <div class="typing-bubble">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    chatBox.appendChild(row);
    scrollToBottom();
}

function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}


// ===== Gửi tin nhắn qua input =====
async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    input.value = '';
    input.disabled = true;


    showTyping();
    await fetchAnswer(message);
    input.disabled = false;
    input.focus();
}

// ===== Gọi API Flask =====
async function fetchAnswer(query) {
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });

        if (!response.ok) {
            throw new Error('Lỗi server: ' + response.status);
        }

        const data = await response.json();

        removeTyping();
        appendMessage(data.answer || 'Xin lỗi, tôi chưa có câu trả lời cho câu hỏi này.', 'bot');

    } catch (error) {
        removeTyping();
        appendMessage(
            'Xin lỗi, đã xảy ra lỗi kết nối. Vui lòng thử lại hoặc liên hệ hotline <strong>1800-xxxx</strong> để được hỗ trợ.',
            'bot'
        );
        console.error('Lỗi:', error);
    }
}


// ===== Upload PDF =====
document.getElementById("pdf-file").addEventListener("change", uploadPDF);

async function uploadPDF() {
    const fileInput = document.getElementById("pdf-file");
    const statusEl  = document.getElementById("upload-status");

    const file = fileInput.files[0];
    if (!file) return;

    statusEl.innerText = "Đang tải lên...";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/upload_pdf", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.status === "ok") {
            statusEl.innerText = "✅ " + data.message;

            // show trong chat luôn
            appendMessage(
                `📄 Đã tải tài liệu: <strong>${file.name}</strong>`,
                "bot"
            );

        } else {
            statusEl.innerText = "❌ " + (data.error || "Lỗi upload");
        }

    } catch (err) {
        statusEl.innerText = "❌ Lỗi kết nối server";
        console.error(err);
    }

    fileInput.value = ""; // reset input
}