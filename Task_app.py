from tkinter import *
from tkinter import ttk, Text, messagebox
import json

# ======================    CONSTANTS   ====================================

BUTTON_WIDTH = 100
FONT = "SegoeUI 13 normal"


# =======================   Main App    =====================================
def clear_fields(title, description):
    """Clears the Entry and Text boxes of any text in them

    :param title: The title Entry label name to clear
    :param description: The description Text label name to clear
    """
    title.delete(0, END)
    description.delete("1.0", END)


def read_file():
    """
    Tries to open and read JSON file if it doesn't exist, then it creates one and reads it

    :return: Returns data variable of the JSON file contents
    """
    try:
        with open("tasks_data.json", "r") as df:
            data = json.load(df)
            return data
    except FileNotFoundError:
        with open("tasks_data.json", "w") as df:
            json.dump(data, df, indent=4)

        with open("tasks_data.json", "r") as data_file:
            data = json.load(data_file)
            return data


def update_listbox():
    """
    Clears the listbox reads the JSON file and extracts the data in the data variable
    if the length of data is 0 (empty) lets user know

    Otherwise, it iterates through the data and prints out the values in the listbox
    """
    listbox.delete(0, END)
    data = read_file()

    if len(data) == 0:
        listbox.insert(END, "No tasks please add New Task")
    else:
        fix_task_ids()
        for values in data:
            display_tasks = f"{values}      {data[values]["title"]}"
            listbox.insert(END, display_tasks)


def create_new_task_window():
    """
    Creates a new_task_window with functionality to create a new task saves it to a JSON file

    Has three entry boxes for information the program needs to create a new task
    Title entry box
    description entry box

    It Has a function within itself create_new_task,
    which gets the entry items in the boxes and creates a JSON entry for a new task it fixes the
    task_id and updates the listbox after the entry has been created

    It also has two buttons create and cancel
    > create button calls on to the create_new_task and creates a new entry
    > cancel closes the window
    """
    new_task_window = Tk()
    new_task_window.title("Create New Task")
    new_task_window.geometry("500x500")

    # ---------------
    #    LABELS     #
    # ---------------

    title_label = Label(new_task_window, text="Title: ")
    title_label.place(x=40, y=40)

    description_label = Label(new_task_window, text="Description: ")
    description_label.place(x=40, y=90)

    # ---------------
    #    ENTRY     #
    # ---------------

    title_entry = Entry(new_task_window)
    title_entry.focus()
    title_entry.place(x=140, y=40, width=300)

    description_entry = Text(new_task_window)
    description_entry.place(x=140, y=90, width=300, height=300)

    def create_new_task():
        """Gets the length of the data in the json file and creates a new task_id based on the
        length

        Gets the information from the:
        > title_entry
        > priority_entry
        > description_entry
        and create a new_data entry in the form of a dictionary. Save that data to a json file

        If any fields are empty, warning lets the user know
        if the task was created successfully lets the user know and clears all fields ready for new
        entry
        fixes the task_id keys in the JSON in case anything was deleted
        updates the listbox after the entry.
        """

        #  takes data in the entry fields for creation of new entry
        title = title_entry.get()
        description = description_entry.get("1.0", END)

        # gets length of task_data and determines the task_id
        data = read_file()
        new_entry = len(data) + 1

        # saves a new_task under new_data variable in a dictionary format. uses the arguments
        # for the data
        new_data = {
            new_entry: {
                "title": title,
                "description": description,
            }
        }

        # Checks if any of the fields are empty if they are pops up with a warning message
        if len(title) == 0 or len(description) == 0:
            messagebox.showwarning(title="Oops", message="Please dont leave any fields empty!")
        else:
            # if everything is filled out, it tries opening the json file to read if the file
            # does not exist, it creates a new one and saves the new task entry in to the file
            try:
                with open("tasks_data.json", "r") as df:
                    data = json.load(df)

            except FileNotFoundError:
                with open("tasks_data.json", "w") as df:
                    json.dump(new_data, df, indent=4)

            # if file exists it just updates the file with the new data and adds it in to the file
            else:
                data.update(new_data)

                with open("tasks_data.json", "w") as df:
                    json.dump(data, df, indent=4)

            # If everything was successfully lets user know and clears all the entry boxes,
            # fix the tas_id in the JSON so everything's in ascending numerical order
            # update the listbox
            finally:
                fix_task_ids()
                update_listbox()
                clear_fields(title_entry, description_entry)
                messagebox.showinfo(title="Success", message="Task saved")

    # ---------------
    #    BUTTONS    #
    # ---------------

    # take data from entry fields and create a new task
    create = Button(new_task_window, text="Create", highlightthickness=0, command=create_new_task)
    create.place(x=139, y=400, width=BUTTON_WIDTH)

    # closes the window
    cancel = Button(new_task_window, text="Cancel", highlightthickness=0, command=new_task_window.destroy)
    cancel.place(x=340, y=400, width=BUTTON_WIDTH)


def read_selected_task_window():
    """
    This function creates a new window that displays the task contents in read-only format
    """

    # fixes the JSON task_ids in case something was deleted or added, so the program
    # iteration would match with the listbox selection reads the file, so we can work with the JSON
    fix_task_ids()
    data = read_file()
    if len(data) <= 0:
        messagebox.showinfo("Error", "There are no tasks to read pleas create a New Task.")
    else:
        # Gets the selected item(task) from the listbox and create a new window
        for i in listbox.curselection():
            # add 1 since every task in the JSON starts from 1 and when we iterate it starts from 0
            task_chosen = str(i + 1)
            read_task_window = Tk()
            read_task_window.title(f"You are reading task: {data[task_chosen]["title"]}")
            read_task_window.geometry("500x500")

            # ---------------
            #    LABELS     #
            # ---------------

            # creates all the labels for the window and places them on the window
            title_label = Label(read_task_window, text="Title: ")
            title_label.place(x=40, y=40)

            description_label = Label(read_task_window, text="Description: ")
            description_label.place(x=40, y=90)

            # ---------------------
            #    TASK CONTENT     #
            # --------------------

            # creates all the labels that wil display the task contents that are selected from the JSON file
            title_of_task = Label(read_task_window, text=f"{data[task_chosen]["title"]}")
            title_of_task.place(x=140, y=40)

            description_of_task = Label(read_task_window, text=f"{data[task_chosen]["description"]}",
                                        wraplength=300, justify="left")
            description_of_task.place(x=140, y=90)

            # ---------------
            #     BUTTONS   #
            # ---------------

            # closes the window on cancel
            cancel = Button(read_task_window, text="Cancel", highlightthickness=0, command=read_task_window.destroy)
            cancel.place(x=350, y=450, width=BUTTON_WIDTH)


def edit_selected_task_window():
    """
    This function allows the user to select the task from the listbox and press edit selected
    button. This opens a new window in the app with the details of the task they want to edit,
    and it allows them to change text in it.

    It fixes the listbox first in case anything was deleted and updates it.
    Read the JSON file to extract the data.
    Then it iterates through the choice in the listbox to find the selected item in the data.
    Create a new window with boxes filled in with the selected task details that can be edited.

    Has an update_selected_task() function within itself that gets all the entry items in the
    entry boxes once the user clicks the confirmation button. It saves the update and updates the listbox
    as well as it fixes the task_id to be in ascending order.
    """
    # fixes the task_id in case something was deleted or changed without saving reads the JSON to
    # extract data creates a new window
    fix_task_ids()
    data = read_file()
    if len(data) <= 0:
        messagebox.showinfo("Error", "There are no tasks to edit pleas create a New Task.")
    else:
        for i in listbox.curselection():
            # gets listbox selection and finds the selected task key by adding 1 to it
            # add 1 since every task in the JSON starts from 1, and when we iterate it starts from 0
            selected_task = str(i + 1)
            edit_task_window = Tk()
            edit_task_window.title(f"You are editing {selected_task}")
            edit_task_window.geometry("500x500")

            # ---------------
            #    LABELS     #
            # ---------------

            # creates all the labels for the item(task) content
            title_label = Label(edit_task_window, text="Title: ")
            title_label.place(x=40, y=40)

            description_label = Label(edit_task_window, text="Description: ")
            description_label.place(x=40, y=90)

            # ---------------
            #    ENTRY     #
            # ---------------

            # creates entry boxes and inserts the selected item contents that can be edited
            updated_title_entry = Entry(edit_task_window)
            updated_title_entry.focus()
            updated_title_entry.insert(0, f"{data[selected_task]["title"]}")
            updated_title_entry.place(x=140, y=40, width=300)

            updated_description_entry = Text(edit_task_window)
            updated_description_entry.insert("1.0", f"{data[selected_task]["description"]}")
            updated_description_entry.place(x=140, y=90, width=300, height=300)

            def update_selected_task():
                """
                This function gets the entry boxes contents and updates the item(task) with the changed
                contents

                If the fields are empty lets the user know
                If everything else is okay, it saves the update and updates listbox and lets the user
                know when successfully
                """

                # gets the data in the entry boxes of the edit task window
                new_title = updated_title_entry.get()
                new_description = updated_description_entry.get("1.0", END)

                # creates new data out of the data
                new_data = {
                    selected_task: {
                        "title": new_title,
                        "description": new_description,
                    }
                }

                # Checks if fields are empty warn user. If everything else is okay, it saves and updates the
                # task and updates listbox as well as lets the user know it was successful
                if len(new_title) == 0 or len(new_description) == 0:
                    messagebox.showwarning("Oops", "Please dont leave any fields empty")
                else:
                    try:
                        with open("tasks_data.json", "r") as df:
                            file_data = json.load(df)

                    except FileNotFoundError:
                        with open("tasks_data.json", "w") as df:
                            json.dump(new_data, df, indent=4)

                    else:
                        file_data.update(new_data)

                        with open("tasks_data.json", "w") as df:
                            json.dump(file_data, df, indent=4)
                    finally:
                        update_listbox()
                        messagebox.showinfo("Success", "Task updated successfully")

            # ---------------
            #    BUTTONS    #
            # ---------------

            # confirms the change button that calls on the update_selected_task
            confirm = Button(edit_task_window, text="Confirm", highlightthickness=0, command=update_selected_task)
            confirm.place(x=139, y=400, width=BUTTON_WIDTH)

            # closes the window
            cancel = Button(edit_task_window, text="Cancel", highlightthickness=0, command=edit_task_window.destroy)
            cancel.place(x=340, y=400, width=BUTTON_WIDTH)


def fix_task_ids():
    """
    This function iterates through the JSON file and updates all the keys to be in the increasing
    numerical order. If some tasks are deleted and task_ids are no longer in order, it causes a bug
    this way the program can still search through the JSON when other functions are called.

    It also looks mor pleasing to the user for everything to be neat
    """
    # open file to get data
    with open("tasks_data.json", "r") as file:
        data = json.load(file)

    # Create a list of task IDs
    task_ids = list(data.keys())

    # Convert task IDs to integers and sort them
    sorted_ids = sorted(map(int, task_ids))

    # Create a dictionary to store the updated tasks
    updated_data = {}

    # Iterate through the sorted IDs and assign new sequential IDs
    new_id = 1
    for old_id in sorted_ids:
        # If the current ID is not the expected next ID, update the key
        if old_id != new_id:
            updated_data[new_id] = data[str(old_id)]
        else:
            updated_data[str(old_id)] = data[str(old_id)]
        new_id += 1

    # Write the updated data back to the file
    with open("tasks_data.json", "w") as file:
        json.dump(updated_data, file, indent=4)


def delete_selected_task():
    """
    This function completely removes an entry(task) From the JSON file adn updates the listbox to reflect
    the removal.
    """
    # fix the task_ids, so it can iterate trough file
    fix_task_ids()
    data = read_file()
    if len(data) <= 0:
        messagebox.showinfo("Error", "There are no tasks to delete pleas create a New Task.")
    else:
        for i in listbox.curselection():
            # add 1 since every task in the JSON starts from 1 and when we iterate it starts from 0
            task_to_remove = str(i + 1)

            # confirm user wants to delete
            confirm = messagebox.askyesno("Warning", f"Are you sure you want to delete task {task_to_remove}?")

            # checking if the key exists before removing
            if confirm is True:
                data.pop(task_to_remove)
                messagebox.showinfo("Success", "Task deleted successfully.")

                # saving the updated JSON data back to the file
                with open("tasks_data.json", "w") as file:
                    json.dump(data, file, indent=4)

                # fix the task_id and update the listbox
                fix_task_ids()
                update_listbox()


# ====================  JSON file   =========================================

# create a json file in case it was missing
open_json = {}
with open("tasks_data.json", "w") as initial_file:
    json.dump(open_json, initial_file, indent=4)


# =====================     UI      ==========================================

# -------------------
#    MAIN WINDOW    #
# -------------------

# Create the main window
main_window = Tk()
main_window.geometry("500x500")
main_window.title("Task manager")
main_window.config(padx=50, pady=50)


# ---------------
#     LISTBOX   #
# ---------------

# list all the tasks in the app
# Create a horizontal scrollbar if there is to many tasks to be listed at once
scrollbar = ttk.Scrollbar(main_window, orient="vertical")
scrollbar.place(x=400, y=10, height=300, width=20)

# Add a Listbox Widget to list all the tasks
listbox = Listbox(main_window, yscrollcommand=scrollbar.set, width=350, font=FONT)
listbox.place(y=10, height=300, width=398)

# Config the scrollbar to move the list of items
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)


# populate the listbox
update_listbox()


# ---------------
#     BUTTONS   #
# ---------------

# read selected entry in the listbox
read_task = Button(text="Read selected", highlightthickness=0, command=read_selected_task_window)
read_task.place(y=320, width=BUTTON_WIDTH)

# edit selected entry in the listbox
edit_selected = Button(text="Edit selected", highlightthickness=0, command=edit_selected_task_window)
edit_selected.place(y=350, width=BUTTON_WIDTH)

# delete selected entry in the listbox
delete_selected = Button(text="Delete selected", highlightthickness=0, command=delete_selected_task)
delete_selected.place(y=380, width=BUTTON_WIDTH)

# opens a window to create a new task
new_task = Button(text="New task", highlightthickness=0, command=create_new_task_window)
new_task.place(x=300, y=320, width=BUTTON_WIDTH)

# Main loop to keep the window on
main_window.mainloop()
