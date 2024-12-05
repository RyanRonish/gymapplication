$(document).ready(function () {
    // Connect to the WebSocket
    const socket = new WebSocket('ws://' + window.location.host + '/ws/gym-status/');

    // Handle incoming WebSocket messages to update the UI in real-time
    socket.onmessage = function (event) {
        const data = JSON.parse(event.data);
        const gymId = data.gym_id;
        const status = data.status;

        // Find the relevant card and update its status
        const statusDiv = $(`.card:has([data-gym-id="${gymId}"])`).find('.gym-status');
        const startButton = $(`.start-workout-btn[data-gym-id="${gymId}"]`);
        const endButton = $(`.end-workout-btn[data-gym-id="${gymId}"]`);
        const reservationBtn = $(`.card:has([data-gym-id="${gymId}"])`).find('.btn-primary');

        if (status === 'open') {
            // Update to "Open" status
            statusDiv.removeClass('bg-danger').addClass('bg-success').text('Open');
            startButton.removeClass('d-none');
            endButton.addClass('d-none');
            reservationBtn.removeClass('disabled');
        } else if (status === 'occupied') {
            // Update to "Occupied" status
            statusDiv.removeClass('bg-success').addClass('bg-danger').text('Occupied');
            startButton.addClass('d-none');
            endButton.removeClass('d-none');
            reservationBtn.addClass('disabled');
        }
    };

    // Handle "I'm Working Out" button click
    $('.start-workout-btn').click(function (event) {
        event.preventDefault();
        const btn = $(this);
        const gymId = btn.data('gym-id');

        // Update the status via WebSocket
        socket.send(JSON.stringify({
            gym_id: gymId,
            status: 'occupied',
        }));

        // Update the status locally via AJAX for redundancy
        $.ajax({
            url: btn.data('url'),
            type: 'GET',
            success: function (response) {
                if (response.status === 'success') {
                    // Update the UI locally
                    const statusDiv = btn.closest('.card').find('.gym-status');
                    statusDiv.removeClass('bg-success').addClass('bg-danger').text('Occupied');
                    btn.addClass('d-none');
                    btn.siblings('.end-workout-btn').removeClass('d-none');
                    const reservationBtn = btn.closest('.card').find('.btn-primary');
                    reservationBtn.addClass('disabled');
                }
            },
            error: function () {
                alert('Failed to start workout. Please try again.');
            }
        });
    });

    // Handle "I'm Done Working Out" button click
    $('.end-workout-btn').click(function (event) {
        event.preventDefault();
        const btn = $(this);
        const gymId = btn.data('gym-id');

        // Update the status via WebSocket
        socket.send(JSON.stringify({
            gym_id: gymId,
            status: 'open',
        }));

        // Update the status locally via AJAX for redundancy
        $.ajax({
            url: btn.data('url'),
            type: 'GET',
            success: function (response) {
                if (response.status === 'success') {
                    // Update the UI locally
                    const statusDiv = btn.closest('.card').find('.gym-status');
                    statusDiv.removeClass('bg-danger').addClass('bg-success').text('Open');
                    btn.addClass('d-none');
                    btn.siblings('.start-workout-btn').removeClass('d-none');
                    const reservationBtn = btn.closest('.card').find('.btn-primary');
                    reservationBtn.removeClass('disabled');
                }
            },
            error: function () {
                alert('Failed to end workout. Please try again.');
            }
        });
    });

    // Handle WebSocket errors
    socket.onerror = function (error) {
        console.error('WebSocket Error: ', error);
    };

    // Handle WebSocket disconnection
    socket.onclose = function () {
        console.warn('WebSocket connection closed');
    };
});
