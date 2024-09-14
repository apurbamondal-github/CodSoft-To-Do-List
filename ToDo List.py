import tkinter as tk
from tkinter import messagebox, simpledialog
import os

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")

        # File to store tasks
        self.tasks_file = "tasks_with_priority.txt"

        # Task list with priorities and timers
        self.tasks = []

        # Load tasks from file
        self.load_tasks()

        # Title Label
        self.title_label = tk.Label(root, text="To-Do List", font=("Helvetica", 18), bg="#f0f0f0")
        self.title_label.pack(pady=10)

        # Task Entry Field
        self.task_entry = tk.Entry(root, width=30, font=("Helvetica", 14))
        self.task_entry.pack(pady=10)

        # Priority Dropdown
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_dropdown = tk.OptionMenu(root, self.priority_var, "High", "Medium", "Low")
        self.priority_dropdown.config(width=10, font=("Helvetica", 14))
        self.priority_dropdown.pack(pady=5)

        # Timer Entry Field
        self.timer_entry = tk.Entry(root, width=10, font=("Helvetica", 14))
        self.timer_entry.pack(pady=10)
        self.timer_entry.insert(0, "Time in min")

        # Add Task Button
        self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task, width=15, font=("Helvetica", 14), bg="#007BFF", fg="white")
        self.add_task_button.pack(pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50, height=10, font=("Helvetica", 14))
        self.task_listbox.pack(pady=10)
        self.update_listbox()

        # Update and Delete Buttons
        self.update_task_button = tk.Button(root, text="Update Task", command=self.update_task, width=15, font=("Helvetica", 14), bg="#FFC107")
        self.update_task_button.pack(pady=5)

        self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task, width=15, font=("Helvetica", 14), bg="#DC3545", fg="white")
        self.delete_task_button.pack(pady=5)

        # Mark Task as Done Button
        self.mark_done_button = tk.Button(root, text="Mark as Done", command=self.mark_done, width=15, font=("Helvetica", 14), bg="#28A745", fg="white")
        self.mark_done_button.pack(pady=5)

        # Save tasks before closing the application
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_tasks(self):
        """Load tasks from the file into the task list."""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, "r") as file:
                self.tasks = [line.strip().split("|") for line in file.readlines()]

    def save_tasks(self):
        """Save the current tasks to a file."""
        with open(self.tasks_file, "w") as file:
            for task, priority, timer in self.tasks:
                file.write(f"{task}|{priority}|{timer}\n")

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_var.get()
        timer = self.timer_entry.get()

        if task != "" and timer.isdigit():
            self.tasks.append((task, priority, timer))
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
            self.timer_entry.delete(0, tk.END)
            self.save_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a valid task and time in minutes.")

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for index, (task, priority, timer) in enumerate(self.tasks):
            display_text = f"{index + 1}. {task} [Priority: {priority}, Time: {timer} min]"
            self.task_listbox.insert(tk.END, display_text)

    def delete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_task_index]
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def update_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            new_task = self.task_entry.get()
            new_priority = self.priority_var.get()
            new_timer = self.timer_entry.get()

            if new_task != "" and new_timer.isdigit():
                self.tasks[selected_task_index] = (new_task, new_priority, new_timer)
                self.update_listbox()
                self.task_entry.delete(0, tk.END)
                self.timer_entry.delete(0, tk.END)
                self.save_tasks()
            else:
                messagebox.showwarning("Input Error", "Please enter a valid task and time in minutes.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to update.")

    def mark_done(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task, priority, timer = self.tasks[selected_task_index]
            self.tasks[selected_task_index] = (f"{task} (Done)", priority, timer)
            self.update_listbox()
            self.save_tasks()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def on_closing(self):
        """Save tasks and close the application."""
        self.save_tasks()
        self.root.destroy()

# Create the root window
root = tk.Tk()

# Create the application
app = TodoApp(root)

# Run the application
root.mainloop()
