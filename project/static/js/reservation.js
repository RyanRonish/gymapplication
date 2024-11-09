function loadTimeSlots() {
    const date = document.getElementById('reservation-date').value;
    const timeSlotsContainer = document.getElementById('time-slots');

    // Reset time slots container
    timeSlotsContainer.innerHTML = '';

    if (date) {
        // Simulate loading time slots (replace this with an AJAX call in a real application)
        const timeSlots = [
            '09:00', '09:20', '09:40', '10:00',
            '10:20', '10:40', '11:00', '11:20'
        ];

        timeSlots.forEach(slot => {
            const timeSlotDiv = document.createElement('div');
            timeSlotDiv.classList.add('col-md-3', 'mb-3');
            
            timeSlotDiv.innerHTML = `
                <div class="card text-center">
                    <div class="card-body">
                        <h5 class="card-title">${slot}</h5>
                        <button class="btn btn-primary" onclick="openReservationModal('${slot}')">Select</button>
                    </div>
                </div>
            `;
            timeSlotsContainer.appendChild(timeSlotDiv);
        });
    }
}

function openReservationModal(slot) {
    document.getElementById('selected-slot-time').textContent = slot;
    $('#reservationModal').modal('show');
}

document.getElementById('confirm-reservation-btn').addEventListener('click', function() {
    const date = document.getElementById('reservation-date').value;
    const slot = document.getElementById('selected-slot-time').textContent;

    // Simulate making a reservation (replace this with an AJAX call in a real application)
    console.log(`Making reservation for ${date} at ${slot}`);

    // Close the modal after confirming
    $('#reservationModal').modal('hide');
});
