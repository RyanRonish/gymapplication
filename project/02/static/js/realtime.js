document.addEventListener("DOMContentLoaded", function () {
    // Connect to the WebSocket
    const socket = new WebSocket('ws://' + window.location.host + '/ws/gym-status/');

    gymStatusSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        document.querySelector('#gym-status').textContent = data.status ? 'Occupied' : 'Available';
    };
    
    gymStatusSocket.onclose = function(e) {
        console.error('Gym status socket closed unexpectedly');
    };

    function updateGymStatus(occupied) {
        gymStatusSocket.send(JSON.stringify({
            'status': occupied
        }));
    }


    // Handle incoming WebSocket messages
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const gymId = data.gym_id;
        const status = data.status;

        // Update the UI for the gym
        const statusDiv = document.getElementById(`gym-status-${gymId}`);
        const startButton = document.getElementById(`start-workout-${gymId}`);
        const endButton = document.getElementById(`end-workout-${gymId}`);
        const reservationButton = document.getElementById(`reservation-btn-${gymId}`);

        if (status === 'open') {
            statusDiv.classList.remove("bg-danger");
            statusDiv.classList.add("bg-success");
            statusDiv.textContent = "Open";
            startButton.classList.remove("d-none");
            endButton.classList.add("d-none");
            reservationButton.classList.remove("disabled");
        } else if (status === 'occupied') {
            statusDiv.classList.remove("bg-success");
            statusDiv.classList.add("bg-danger");
            statusDiv.textContent = "Occupied";
            startButton.classList.add("d-none");
            endButton.classList.remove("d-none");
            reservationButton.classList.add("disabled");
        }
    };

    // Send "I'm Working Out" message via WebSocket
    document.querySelectorAll('.start-workout-btn').forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const gymId = this.getAttribute("data-gym-id");
            socket.send(JSON.stringify({ gym_id: gymId, status: 'occupied' }));
        });
    });

    // Send "I'm Done Working Out" message via WebSocket
    document.querySelectorAll('.end-workout-btn').forEach(function (button) {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const gymId = this.getAttribute("data-gym-id");
            socket.send(JSON.stringify({ gym_id: gymId, status: 'open' }));
        });
    });

    // Log errors or disconnects
    socket.onerror = function (error) {
        console.error("WebSocket Error:", error);
    };

    socket.onclose = function () {
        console.warn("WebSocket connection closed");
    };
});
