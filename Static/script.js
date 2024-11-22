const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let lastX = 0;
let lastY = 0;
let hasDrawn = false;
let isErasing = false;

// Stack to store canvas states for undo
const undoStack = [];

// Fill the canvas with a white background
function fillCanvas() {
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}

// Save the current canvas state
function saveState() {
    if (undoStack.length === 10) {
        undoStack.shift(); // Limit stack to 10 states
    }
    undoStack.push(canvas.toDataURL());
}

// Restore the last canvas state
function undo() {
    if (undoStack.length > 0) {
        const previousState = undoStack.pop();
        const img = new Image();
        img.src = previousState;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
            ctx.drawImage(img, 0, 0); // Restore the previous state
        };
    }
}

// Initialize the canvas
fillCanvas();

// Event listeners for drawing
canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
    saveState(); // Save the state before starting a new drawing action
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath(); // Reset the path
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;
    hasDrawn = true;

    ctx.strokeStyle = isErasing ? 'white' : 'black';
    ctx.lineWidth = isErasing ? 10 : 2;
    ctx.lineJoin = 'round';

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();
    lastX = e.offsetX;
    lastY = e.offsetY;
});

// Handle touch events (mobile)
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    lastX = touch.clientX - canvas.getBoundingClientRect().left;
    lastY = touch.clientY - canvas.getBoundingClientRect().top;
    drawing = true;
    saveState(); // Save the state before starting a new drawing action
});

canvas.addEventListener('touchmove', (e) => {
    if (!drawing) return;
    e.preventDefault();

    const touch = e.touches[0];
    ctx.strokeStyle = isErasing ? 'white' : 'black';
    ctx.lineWidth = isErasing ? 10 : 2;
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
    ctx.beginPath();
});

// Undo button functionality
const undoButton = document.getElementById('undoButton');
undoButton.addEventListener('click', undo);

// Eraser button functionality
const eraserButton = document.getElementById('eraserButton');
eraserButton.addEventListener('click', () => {
    isErasing = !isErasing;
    eraserButton.textContent = isErasing ? 'Switch to Drawing' : 'Toggle Eraser';
});

// Resize canvas
function resizeCanvas() {
    canvas.width = canvas.clientWidth;
    canvas.height = 300;
}

// Save doodle only if there's content
function saveDoodle() {
    const doodleInput = document.getElementById('doodleInput');

    if (!hasDrawn) {
        doodleInput.value = '';
        return;
    }

    doodleInput.value = canvas.toDataURL();
}

// Validate note before submission
function validateNote() {
    const noteInput = document.getElementById('noteInput');

    if (noteInput.value.trim() === '') {
        alert('Please enter a note before submitting.');
        return false;
    }

    saveDoodle();
    return true;
}

// Resize canvas on load and resize
window.addEventListener('load', resizeCanvas);
window.addEventListener('resize', resizeCanvas);
