document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('drawingCanvas');
    const editor = document.getElementById('editor');
    const undoButton = document.getElementById('undoButton');
    const toggleCanvas = document.getElementById('toggleCanvas');

    canvas.width = editor.offsetWidth;
    canvas.height = 500;

    const ctx = canvas.getContext('2d');
    const undoStack = [];
    let isDrawing = false;
    let isErasing = false; // Default mode: Drawing
    let currentColor = 'black';

    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    saveState();

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

    // Undo functionality
    undoButton.addEventListener('click', undo);

    // Toggle between drawing and erasing
    toggleCanvas.addEventListener('click', () => {
        isErasing = !isErasing;
        toggleCanvas.style.color = isErasing ? 'red' : 'black'; // Change icon color
        toggleCanvas.title = isErasing ? 'Eraser Mode' : 'Drawing Mode'; // Tooltip update
    });

    // Begin drawing or erasing
    canvas.addEventListener('mousedown', () => {
        isDrawing = true;
        saveState();
    });
    canvas.addEventListener('mouseup', () => (isDrawing = false));
    canvas.addEventListener('mousemove', (event) => {
        if (isDrawing) {
            const rect = canvas.getBoundingClientRect();
            ctx.lineTo(event.clientX - rect.left, event.clientY - rect.top);
            ctx.strokeStyle = isErasing ? 'white' : currentColor; // Use white for erasing
            ctx.lineWidth = isErasing ? 10 : 2; // Thicker stroke for eraser
            ctx.stroke();
        } else {
            ctx.beginPath();
        }
    });

    // Handle touch events for mobile
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        ctx.moveTo(
            touch.clientX - canvas.getBoundingClientRect().left,
            touch.clientY - canvas.getBoundingClientRect().top
        );
        isDrawing = true;
        saveState();
    });

    canvas.addEventListener('touchmove', (e) => {
        if (!isDrawing) return;
        e.preventDefault();
        const touch = e.touches[0];
        const rect = canvas.getBoundingClientRect();
        ctx.lineTo(
            touch.clientX - rect.left,
            touch.clientY - rect.top
        );
        ctx.strokeStyle = isErasing ? 'white' : currentColor; // Use white for erasing
        ctx.lineWidth = isErasing ? 10 : 2; // Thicker stroke for eraser
        ctx.stroke();
    });

    canvas.addEventListener('touchend', () => {
        isDrawing = false;
        ctx.beginPath();
    });
});
