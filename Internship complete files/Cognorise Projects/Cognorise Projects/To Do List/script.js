$(document).ready(function() {
    // Load tasks from local storage on page load
    loadTasks();

    $('#addTaskButton').click(function() {
        let taskInput = $('#taskInput').val();
        if (taskInput) {
            let ul = $('#taskList');
            let li = $('<li class="animate__animated animate__fadeInRight"></li>').text(taskInput);
            let removeButton = $('<button><i class="fas fa-trash"></i></button>');
            
            // Add task to local storage
            saveTask(taskInput);

            removeButton.click(function() {
                li.addClass('animate__fadeOutLeft');
                li.on('animationend', function() {
                    li.remove();
                    // Remove task from local storage
                    removeTask(taskInput);
                });
            });

            li.append(removeButton);
            ul.append(li);
            $('#taskInput').val('');
        }
    });

    // Function to load tasks from local storage
    function loadTasks() {
        let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        tasks.forEach(task => {
            let ul = $('#taskList');
            let li = $('<li class="animate__animated animate__fadeInRight"></li>').text(task);
            let removeButton = $('<button><i class="fas fa-trash"></i></button>');
            
            removeButton.click(function() {
                li.addClass('animate__fadeOutLeft');
                li.on('animationend', function() {
                    li.remove();
                    removeTask(task);
                });
            });

            li.append(removeButton);
            ul.append(li);
        });
    }

    // Function to save task to local storage
    function saveTask(task) {
        let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        tasks.push(task);
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }

    // Function to remove task from local storage
    function removeTask(task) {
        let tasks = JSON.parse(localStorage.getItem('tasks')) || [];
        tasks = tasks.filter(t => t !== task);
        localStorage.setItem('tasks', JSON.stringify(tasks));
    }
});
