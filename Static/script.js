const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let lastX = 0;
let lastY = 0;

// Fill the canvas with a white background
function fillCanvas() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Call fillCanvas to set the initial background
fillCanvas();

// Start drawing
canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
});

// Stop drawing
canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath(); // Reset the path
});

// Draw on the canvas
canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    lastX = e.offsetX;
    lastY = e.offsetY;
});

// Handle touch events for mobile
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault(); // Prevent scrolling
    const touch = e.touches[0];
    lastX = touch.clientX - canvas.getBoundingClientRect().left;
    lastY = touch.clientY - canvas.getBoundingClientRect().top;
    drawing = true;
});

canvas.addEventListener('touchmove', (e) => {
    if (!drawing) return;
    e.preventDefault(); // Prevent scrolling
    const touch = e.touches[0];
    ctx.strokeStyle = 'black';
    ctx.lineWidth = 2;
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(touch.clientX - canvas.getBoundingClientRect().left, touch.clientY - canvas.getBoundingClientRect().top);
    ctx.stroke();
    lastX = touch.clientX - canvas.getBoundingClientRect().left;
    lastY = touch.clientY - canvas.getBoundingClientRect().top;
});

canvas.addEventListener('touchend', () => {
    drawing = false;
    ctx.beginPath(); // Reset the path
});

// Resize canvas to fit the width of the screen
function resizeCanvas() {
    canvas.width = canvas.clientWidth; // Set canvas width to its client width
    canvas.height = 300; // Set a fixed height
}

// Save doodle as image
function saveDoodle() {

    const doodleInput = document.getElementById('doodleInput');

    const dataURL = canvas.toDataURL('image/png');

    doodleInput.value = dataURL; // Save the doodle data to the hidden input

}


function validateNote() {

    const noteInput = document.getElementById('noteInput');

    if (noteInput.value.trim() === '') {

        alert('Please enter a note before submitting.'); // Alert if the note is empty

        return false; // Prevent form submission

    }

    saveDoodle(); // Save doodle data before submitting

    return true; // Allow form submission

}
// Resize canvas on window load and resize
window.addEventListener('load', resizeCanvas);
window.addEventListener('resize', resizeCanvas);