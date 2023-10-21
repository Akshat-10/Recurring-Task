frappe.pages['task-view'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Task View',
		single_column: true
	});
	
	function generateHTMLStructure() {
        const taskContainer = $('<div>').appendTo(wrapper);
        taskContainer.addClass('task-container');

        const today = frappe.datetime.get_today();
        const dateOffsets = [-2, -1, 0, 1, 2];

        for (let i = 0; i < dateOffsets.length; i++) {
            const dateOffset = dateOffsets[i];
            const date = frappe.datetime.add_days(today, dateOffset);

            const column = $('<div>').appendTo(taskContainer);
            column.addClass('task-column');

            const header = $('<div>').appendTo(column);
            header.addClass('task-header');
            header.text(frappe.datetime.str_to_user(date));


            // Increase font size for date
            header.css('font-size', '20px'); // Adjust the font size as needed

            fetchTaskData(date, column);
        }
    }

    function fetchTaskData(date, column) {
        frappe.call({
            method: 'frappe.client.get_list',
            args: {
                doctype: 'Task',
                fields: ['name', 'subject', 'exp_start_date', 'exp_end_date'],
                filters: {
                    'exp_start_date': date
                }
            },
            callback: function(response) {
                if (response.message) {
                    displayTaskData(response.message, date, column);
                }
            }
        });
    }

    function displayTaskData(tasks, date, column) {
        if (tasks.length === 0) {
            const noTasksMessage = $('<p>').appendTo(column);
            noTasksMessage.text('No tasks for this date.');
        } else {
            for (let i = 0; i < tasks.length; i++) {
                const task = tasks[i];
                const taskBox = $('<div>').appendTo(column);
                taskBox.addClass('task-box');

                const taskId = task.name || 'N/A';

                const taskLink = $(`<a href="/app/task/${task.name}">`)
                    .appendTo(taskBox)
                    .append(`<h2>${task.subject} (Task ID: ${taskId})</h2>`);

                // Increase font size for task titles
                taskLink.find('h2').css('font-size', '18px'); // Adjust the font size as needed

                taskLink.click(function() {
                    frappe.set_route('task', task.name);
                });

                taskBox.append(`<p style="font-size: 18px;">Start Date: ${task.exp_start_date}</p>`);
                taskBox.append(`<p style="font-size: 18px;">End Date: ${task.exp_end_date}</p>`);

                // Add a line after each task
                taskBox.css('border-bottom', '1px solid #ccc'); // Adjust the border style as needed

            }
        }
    }

    generateHTMLStructure();

    const css = `
        .task-container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
        }
        
        .task-column {
            border: 1px solid #ccc;
            padding: 20px;
            margin: 10px;
            text-align: center;
            flex: 1;
            width: calc(20% - 20px);
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .task-header {
            font-weight: bold;
            margin-bottom: 10px;
        }
    `;

    // Append the CSS to the head of the HTML
    const styleElement = document.createElement('style');
    styleElement.type = 'text/css';
    styleElement.appendChild(document.createTextNode(css));
    document.head.appendChild(styleElement);
}