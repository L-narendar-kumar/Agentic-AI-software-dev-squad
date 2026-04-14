document.addEventListener('DOMContentLoaded', () => {
    const newTaskInput = document.getElementById('newTaskInput');
    const addTaskButton = document.getElementById('addTaskButton');
    const taskList = document.getElementById('taskList');

    // Function to create a new task element
    function createTaskElement(taskText) {
        const listItem = document.createElement('li');
        listItem.classList.add('task-item'); // Add a class for styling and event delegation

        const taskSpan = document.createElement('span');
        taskSpan.textContent = taskText;
        taskSpan.classList.add('task-text'); // Add a class for styling and event delegation

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.classList.add('delete-task-btn'); // Add a class for styling and event delegation

        listItem.appendChild(taskSpan);
        listItem.appendChild(deleteButton);

        return listItem;
    }

    // Add Task functionality
    addTaskButton.addEventListener('click', () => {
        const taskText = newTaskInput.value.trim();
        if (taskText !== '') {
            const newTask = createTaskElement(taskText);
            taskList.appendChild(newTask);
            newTaskInput.value = ''; // Clear the input field
        }
    });

    // Allow adding tasks by pressing Enter key in the input field
    newTaskInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            addTaskButton.click(); // Simulate a click on the add button
        }
    });

    // Event delegation for task completion and deletion
    // This single listener handles clicks on dynamically added task items
    taskList.addEventListener('click', (event) => {
        const target = event.target;

        // Handle deleting a task
        // If the clicked element has the 'delete-task-btn' class
        if (target.classList.contains('delete-task-btn')) {
            const listItem = target.closest('.task-item'); // Find the parent <li> element
            if (listItem) {
                listItem.remove(); // Remove the task item from the DOM
            }
        }
        // Handle marking a task as complete/incomplete
        // If the clicked element is the task item itself or its child span
        else if (target.classList.contains('task-item') || target.classList.contains('task-text')) {
            const listItem = target.closest('.task-item'); // Find the parent <li> element
            if (listItem) {
                listItem.classList.toggle('completed'); // Toggle the 'completed' CSS class
            }
        }
    });
});
