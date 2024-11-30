document.getElementById('toggleCanvas').addEventListener('click', function () {
    const editor = document.getElementById('editor');
    const existingCanvas = document.querySelector('#editor canvas');
    if (!existingCanvas) {
        editor.innerHTML = '';
        const canvas = document.createElement('canvas');
        canvas.id = 'drawingCanvas';
        canvas.width = editor.offsetWidth;
        canvas.height = 500;
        canvas.style.border = '1px solid #000';
        editor.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        const undoStack = [];
        let isDrawing = false;
        let hasDrawn = false;
        let isErasing = false;
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
        const undoButton = document.getElementById('undoButton');
        undoButton.addEventListener('click', undo);

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
                ctx.strokeStyle = currentColor;
                ctx.lineWidth = isErasing ? 10 : 2;
                ctx.stroke();
                hasDrawn = true;
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
            ctx.strokeStyle = currentColor;
            ctx.lineWidth = isErasing ? 10 : 2;
            ctx.stroke();
            hasDrawn = true;
        });

        canvas.addEventListener('touchend', () => {
            isDrawing = false;
            ctx.beginPath();
        });
    }
});

// Make validateNote globally accessible
function validateNote() {
    const noteInput = document.getElementById('noteInput');
    const doodleInput = document.getElementById('doodleInput');
    const canvas = document.getElementById('drawingCanvas');

    // Check if note input is empty
    if (noteInput.value.trim() === '') {
        alert('Please enter a note before submitting.');
        return false;
    }

    // Save doodle data if canvas exists
    if (canvas) {
        const ctx = canvas.getContext('2d');
        if (ctx.getImageData(0, 0, canvas.width, canvas.height).data.some((pixel) => pixel !== 255)) {
            doodleInput.value = canvas.toDataURL('image/png', 0.5);
        }
    }
    return true;
}
