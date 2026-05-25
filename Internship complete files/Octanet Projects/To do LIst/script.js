document.addEventListener('DOMContentLoaded', () => {
    const taskInput = document.getElementById('new-task');
    const addTaskBtn = document.getElementById('add-task-btn');
    const todoList = document.getElementById('todo-list');
    const clearTasksBtn = document.getElementById('clear-tasks-btn');

    addTaskBtn.addEventListener('click', addTask);
    taskInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addTask();
        }
    });
    clearTasksBtn.addEventListener('click', clearTasks);

    function addTask() {
        const taskText = taskInput.value.trim();
        if (taskText !== '') {
            const listItem = document.createElement('li');
            const taskSpan = document.createElement('span');
            taskSpan.textContent = taskText;

            taskSpan.addEventListener('click', () => {
                listItem.classList.toggle('completed');
            });

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = 'Delete';
            deleteBtn.addEventListener('click', () => {
                todoList.removeChild(listItem);
            });

            listItem.appendChild(taskSpan);
            listItem.appendChild(deleteBtn);
            todoList.appendChild(listItem);

            taskInput.value = '';
            taskInput.focus();
        }
    }

    function clearTasks() {
        todoList.innerHTML = '';
    }

    // Draggable shapes
    const shapes = document.querySelectorAll('.shape');
    shapes.forEach(shape => {
        shape.addEventListener('mousedown', (e) => {
            let shiftX = e.clientX - shape.getBoundingClientRect().left;
            let shiftY = e.clientY - shape.getBoundingClientRect().top;

            function moveAt(pageX, pageY) {
                shape.style.left = pageX - shiftX + 'px';
                shape.style.top = pageY - shiftY + 'px';
            }

            function onMouseMove(event) {
                moveAt(event.pageX, event.pageY);
            }

            document.addEventListener('mousemove', onMouseMove);

            shape.onmouseup = function() {
                document.removeEventListener('mousemove', onMouseMove);
                shape.onmouseup = null;
            };
        });

        shape.ondragstart = function() {
            return false;
        };
    });
});
