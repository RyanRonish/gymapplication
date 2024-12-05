// gymStatus.js
const gymStatusSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/gym_status/'
);

gymStatusSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    document.querySelector('#gym-status').textContent = data.status ? 'Occupied' : 'Available';
};

gymStatusSocket.onclose = function(e) {
    console.error('Gym status socket closed unexpectedly');
};