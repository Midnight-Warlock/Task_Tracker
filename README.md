# Task Tracker App

A simple task tracking desktop application built with Python and PyQt6. This app allows users to add, edit, complete, and delete tasks. Additionally, it stores tasks with timestamps and checks for overdue tasks every hour.

## Features

- Add tasks with a name and optional details
- Edit existing tasks
- Mark tasks as complete, which saves them to a separate `completed_tasks.csv` file
- Delete tasks
- Automatically checks for overdue tasks that have not been modified in the last 24 hours
- Saves tasks in a `tasks.csv` file, preserving data between sessions
- Clear and intuitive user interface

## Installation

### Prerequisites

- Python 3.7 or higher
- PyQt6

### Steps

1. Clone this repository or download the source code.
2. Install PyQt6 if you don't have it already: `pip install PyQt6`
3. Run the `main.py` file: `python main.py`

## Usage

1. Enter a task name in the "Enter Task Name" field.
2. (Optional) Enter task details in the "Enter Task Details" field.
3. Click the "Add Task" button to add the task to the list.
4. To edit a task, select it in the list and click the "Edit Task" button.
5. To mark a task as complete, select it in the list and click the "Complete Task" button.
6. To delete a task, select it in the list and click the "Delete Task" button.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss any proposed changes or improvements.

## License

This project is open-source and available under the MIT License.
