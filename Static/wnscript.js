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
        const undoButton = document.createElement('button');
        undoButton.textContent = 'Undo';
        undoButton.style.marginTop = '10px';
        undoButton.addEventListener('click', undo);
        editor.appendChild(undoButton);
        
        // Begin drawing or erasing
        canvas.addEventListener('mousedown', () => {
            isDrawing = true;
            saveState();
        });
        canvas.addEventListener('mouseup', () => isDrawing = false);
        canvas.addEventListener('mousemove', (event) => {
            if (isDrawing) {
                const rect = canvas.getBoundingClientRect();
                ctx.lineTo(event.clientX - rect.left, event.clientY - rect.top);
                ctx.strokeStyle = 'black';
                ctx.lineWidth = 2;
                ctx.stroke();
            } else {
                ctx.beginPath();
            }
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
        
    }
});