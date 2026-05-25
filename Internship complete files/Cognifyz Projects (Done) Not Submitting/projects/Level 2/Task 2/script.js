// script.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('applicationForm');
    const responseMessage = document.getElementById('responseMessage');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');

        // Simulate submission for demonstration purposes
        setTimeout(() => {
            responseMessage.textContent = `Thank you, ${name}! Your application has been submitted.`;
            form.reset();
        }, 1000);
    });
});
