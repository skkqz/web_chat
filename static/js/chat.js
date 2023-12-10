const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);
const room_name = JSON.parse(document.getElementById('json-room-name').textContent);

const chatMessages = document.querySelector('#chat-messages');

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
);

socket.onopen = function (e) {
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function (e) {
    console.log("CONNECTION LOST");
}

socket.onerror = function (e) {
    console.error(e);
}

socket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);

    if (data.username == message_username) {
        appendMessage('sent', data.message);
    } else {
        appendMessage('received', data.message);

        if (!data.is_seen && data.username !== message_username) {
            // Вызовите функцию для обновления UI для статуса "прочитано"
            markMessageAsRead(data);
        }
    }

    // Прокрутка вниз при появлении новых сообщений
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

function markMessageAsRead(data) {
    notifications.send(JSON.stringify({
        'room_name': data.room_name,
        'notification_id': data.notification_id,
    }));
}

window.onload = function() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    sendMessage();
};

// Отправка сообщения при нажатии клавиши "Enter"
document.querySelector('#message-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); // Предотвращаем перенос строки
        sendMessage();
    }
});

function sendMessage() {
    const message_input = document.querySelector('#message-input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message': message,
        'username': message_username,
        'receiver': receiver,
        'room_name': room_name,
    }));

    message_input.value = '';
}

function appendMessage(type, message) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    const now = new Date();
    const date = now.toLocaleTimeString(navigator.language, {hour: '2-digit', minute:'2-digit'});
    messageDiv.innerHTML = `
        <div class="message-text">
            <p>${message}</p>
            <p class="message-date">${date}</p>
        </div>
    `;
    chatMessages.appendChild(messageDiv);

    // Прокрутка вниз при добавлении нового сообщения
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
