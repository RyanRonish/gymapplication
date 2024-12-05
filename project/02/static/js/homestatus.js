$(document).ready(function() {
    // Handle "I'm Working Out" button click
    $('.start-workout-btn').click(function(event) {
        event.preventDefault();
        const btn = $(this);
        const gymId = btn.data('gym-id');

        // AJAX request to mark the gym as occupied
        $.ajax({
            url: btn.data('url'),
            type: 'GET',
            success: function(response) {
                if (response.status === 'success') {
                    // Update the gym status bar
                    const statusDiv = btn.closest('.card').find('.gym-status');
                    statusDiv.removeClass('bg-success').addClass('bg-danger').text('Occupied');

                    // Toggle button visibility
                    btn.addClass('d-none');
                    btn.siblings('.end-workout-btn').removeClass('d-none');

                    // Disable the reservation button
                    const reservationBtn = btn.closest('.card').find('.btn-primary');
                    reservationBtn.addClass('disabled');
                }
            },
            error: function() {
                alert('Failed to start workout. Please try again.');
            }
        });
    });

    // Handle "I'm Done Working Out" button click
    $('.end-workout-btn').click(function(event) {
        event.preventDefault();
        const btn = $(this);
        const gymId = btn.data('gym-id');

        // AJAX request to mark the gym as open
        $.ajax({
            url: btn.data('url'),
            type: 'GET',
            success: function(response) {
                if (response.status === 'success') {
                    // Update the gym status bar
                    const statusDiv = btn.closest('.card').find('.gym-status');
                    statusDiv.removeClass('bg-danger').addClass('bg-success').text('Open');

                    // Toggle button visibility
                    btn.addClass('d-none');
                    btn.siblings('.start-workout-btn').removeClass('d-none');

                    // Enable the reservation button
                    const reservationBtn = btn.closest('.card').find('.btn-primary');
                    reservationBtn.removeClass('disabled');
                }
            },
            error: function() {
                alert('Failed to end workout. Please try again.');
            }
        });
    });
});
