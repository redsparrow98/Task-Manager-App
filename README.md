# Task Manager App

This is a simple task managing application built with Python using Tkinter for the GUI.
The application allows users to create, read, update, and delete tasks.
Tasks are stored in a JSON file (tasks_data.json) and displayed in a listbox within the
application interface.

## Features
**Create New Task:** Users can create a new task by providing a title and description.

**Read Task:** Users can view the details of a selected task in a read-only window.

**Edit Task:** Users can edit the details of a selected task, including the title and description.

**Delete Task:** Users can delete a selected task.

**List Tasks:** All tasks are listed in a scrollable listbox for easy access.

## How to Use

**1) Creating a New Task:**

- Click the *New task* button.
- Enter the title and description of the task in the provided fields.
- Click the *Create* button to save the task.

**2) Reading a Task:**

- Select a task from the listbox.
- Click the *Read selected* button to view the details of the selected task.

**3) Editing a Task:**

- Select a task from the listbox.
- Click the "Edit selected" button.
- Update the title and description of the task in the provided fields.
- Click the "Confirm" button to save the changes.

**4) Deleting a Task:**

- Select a task from the listbox.
- Click the *Delete selected* button to remove the task.

## Important Notes
If no tasks are available, appropriate messages will be displayed.
The application uses a JSON file (tasks_data.json) to store task data.
All task IDs are automatically managed to ensure sequential ordering.

## Dependencies
- Python 3.x
- Tkinter (usually included in Python installations)

## Running the Application
Clone this repository to your local machine.
Make sure you have Python installed.
Navigate to the cloned directory and Run the program

# Contributing
**Contributions are welcome!** Please feel free to submit any issues or pull requests.