const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
let drawing = false;
let lastX = 0;
let lastY = 0;
let isErasing = false;
let hasDrawn = false;
const undoStack = [];
let currentColor = '#000000'; // Default color

// Save the current canvas state for undo
function saveState() {
    if (undoStack.length === 10) {
        undoStack.shift(); // Limit stack to 10 states
    }
    undoStack.push(canvas.toDataURL());
}

// Restore the last state for undo
function undo() {
    if (undoStack.length > 1) {
        undoStack.pop(); // Remove current state
        const previousState = undoStack[undoStack.length - 1];
        const img = new Image();
        img.src = previousState;
        img.onload = () => {
            ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear the canvas
            ctx.drawImage(img, 0, 0); // Draw the previous state
        };
    }
}

// Initialize canvas size dynamically
function resizeCanvas() {
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    const tempCtx = tempCanvas.getContext('2d');
    tempCtx.drawImage(canvas, 0, 0);


    canvas.width = canvas.clientWidth;
    canvas.height = 300;
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height); 


    ctx.drawImage(tempCanvas, 0, 0); // Restore content after resizing
}

// Begin drawing or erasing
canvas.addEventListener('mousedown', (e) => {
    drawing = true;
    lastX = e.offsetX;
    lastY = e.offsetY;
    saveState(); // Save state before a new operation
});

canvas.addEventListener('mouseup', () => {
    drawing = false;
    ctx.beginPath(); // Reset path
});

canvas.addEventListener('mousemove', (e) => {
    if (!drawing) return;

    ctx.lineWidth = isErasing ? 10 : 2;
    ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = isErasing ? 'destination-out' : 'source-over';
    ctx.strokeStyle = isErasing ? 'rgba(0,0,0,1)' : currentColor; // Fix the erasing mode issue

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(e.offsetX, e.offsetY);
    ctx.stroke();

    lastX = e.offsetX;
    lastY = e.offsetY;
    hasDrawn = true;
});

// Handle touch events for mobile
canvas.addEventListener('touchstart', (e) => {
    e.preventDefault();
    const touch = e.touches[0];
    lastX = touch.clientX - canvas.getBoundingClientRect().left;
    lastY = touch.clientY - canvas.getBoundingClientRect().top;
    drawing = true;
    saveState();
});

canvas.addEventListener('touchmove', (e) => {
    if (!drawing) return;
    e.preventDefault();

    const touch = e.touches[0];
    ctx.lineWidth = isErasing ? 10 : 2;
    ctx.lineJoin = 'round';
    ctx.globalCompositeOperation = isErasing ? 'destination-out' : 'source-over';
    ctx.strokeStyle = isErasing ? 'rgba(0,0,0,1)' : currentColor; // Fix the erasing mode issue

    ctx.beginPath();
    ctx.moveTo(lastX, lastY);
    ctx.lineTo(
        touch.clientX - canvas.getBoundingClientRect().left,
        touch.clientY - canvas.getBoundingClientRect().top
    );
    ctx.stroke();

    lastX = touch.clientX - canvas.getBoundingClientRect().left;
    lastY = touch.clientY - canvas.getBoundingClientRect().top;
    hasDrawn = true;
});

canvas.addEventListener('touchend', () => {
    drawing = false;
    ctx.beginPath();
});

// Toggle eraser
const eraserButton = document.getElementById('eraserButton');
eraserButton.addEventListener('click', () => {
    isErasing = !isErasing;
    eraserButton.textContent = isErasing ? 'Switch to Drawing' : 'Toggle Eraser';
});

// Undo functionality
const undoButton = document.getElementById('undoButton');
undoButton.addEventListener('click', undo);

// Handle color changes
const colorPicker = document.getElementById('colorPicker');
colorPicker.addEventListener('input', (e) => {
    currentColor = e.target.value; // Update the current color
});

// Save doodle only if content exists
function saveDoodle() {
    const doodleInput = document.getElementById('doodleInput');
    if (!hasDrawn) {
        doodleInput.value = ''; // Don't save blank data
        return;
    }
    doodleInput.value = canvas.toDataURL('image/png', 0.5);
}

// Validate note
function validateNote() {
    const noteInput = document.getElementById('noteInput');
    if (noteInput.value.trim() === '') {
        alert('Please enter a note before submitting.');
        return false;
    }
    saveDoodle();
    return true;
}

function editNote(noteId) {
    const editForm = document.getElementById(`edit-form-${noteId}`);
    const editCanvas = document.getElementById(`edit-canvas-${noteId}`);
    const editCtx = editCanvas.getContext('2d');

    if (editForm.style.display === "none" || editForm.style.display === "") {
        editForm.style.display = "block";
        loadDoodle(noteId, editCtx); // Load existing doodle when the edit form is displayed
        initializeDoodleCanvas(noteId, editCtx); // Initialize doodle canvas for editing
    } else {
        editForm.style.display = "none";
    }
}

// Load existing doodle into the edit canvas
function loadDoodle(noteId, editCtx) {
    const doodleData = document.getElementById(`doodle-${noteId}`).value;
    
    if (doodleData) {
        const img = new Image();
        img.src = doodleData;
        img.onload = () => {
            editCtx.clearRect(0, 0, editCanvas.width, editCanvas.height); // Clear the canvas
            editCtx.drawImage(img, 0, 0); // Draw the existing doodle
        };
    } else {
        // Clear the canvas if no doodle exists
        editCtx.clearRect(0, 0, editCanvas.width, editCanvas.height);
    }
}

// Initialize doodle canvas for editing
function initializeDoodleCanvas(noteId, editCtx) {
    const editCanvas = document.getElementById(`edit-canvas-${noteId}`);
    let drawing = false;
    let lastX = 0;
    let lastY = 0;
    let isErasing = false;
    let currentColor = '#000000'; // Default color

    // Begin drawing
    editCanvas.addEventListener('mousedown', (e) => {
        drawing = true;
        lastX = e.offsetX;
        lastY = e.offsetY;
    });

    editCanvas.addEventListener('mouseup', () => {
        drawing = false;
        editCtx.beginPath(); // Reset path
    });

    editCanvas.addEventListener('mousemove', (e) => {
        if (!drawing) return;

        editCtx.lineWidth = isErasing ? 10 : 2;
        editCtx.lineJoin = 'round';
        editCtx.globalCompositeOperation = isErasing ? 'destination-out' : 'source-over';
        editCtx.strokeStyle = isErasing ? 'rgba(0,0,0,1)' : currentColor;

        editCtx.beginPath();
        editCtx.moveTo(lastX, lastY);
        editCtx.lineTo(e.offsetX, e.offsetY);
        editCtx.closePath();
        editCtx.stroke();

        lastX = e.offsetX;
        lastY = e.offsetY;
    });

    // // Color picker
    const colorPicker = document.getElementById(`colorPicker-${noteId}`);
    colorPicker.addEventListener('input', (e) => {
        currentColor = e.target.value; // Update current color
    });

    // Eraser toggle
    const eraserButton = document.getElementById(`eraserButton-${noteId}`);
    eraserButton.addEventListener('click', () => {
        isErasing = !isErasing; // Toggle eraser mode
        eraserButton.textContent = isErasing ? 'Use Pen' : 'Toggle Eraser'; // Update button text
    });

    // Undo functionality
    const undoButton = document.getElementById(`undoButton-${noteId}`);
    undoButton.addEventListener('click', () => {
        // Implement undo functionality (this can be done using a stack to store states)
        // For simplicity, this example does not implement undo
        alert('Undo functionality not implemented yet.');
    });
}

// Save the edited doodle when saving the note
function saveEditedDoodle(noteId) {
    const editCanvas = document.getElementById(`edit-canvas-${noteId}`);
    const doodleInput = document.getElementById(`doodle-${noteId}`);
    
    doodleInput.value = editCanvas.toDataURL('image/png', 0.5); // Save the edited doodle
}

// Modify the edit form submission to save the doodle
const editForms = document.querySelectorAll('form[action^="/edit_note"]');
editForms.forEach(form => {
    form.addEventListener('submit', (e) => {
        const noteId = form.action.split('/').pop(); // Get the note ID from the action URL
        saveEditedDoodle(noteId); // Save the edited doodle before submitting
    });
});

// Resize canvas on window load and resize
window.addEventListener('load', resizeCanvas);
window.addEventListener('resize', resizeCanvas);