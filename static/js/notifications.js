const room_name = JSON.parse(document.getElementById('json-room-name').textContent);
const receiver_user = JSON.parse(document.getElementById('json-username').textContent);

const notifications = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + 'notifications/'
)

notifications.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data);

    // Обработка уведомления о прочтении сообщения
    updateNotificationUI(data);
}

function updateNotificationUI(data) {
    const notificationCount = data.count;
}
