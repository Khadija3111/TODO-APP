"""
CLI Interface

This module provides the command-line interface for the todo application.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.task_store import TaskStore
from models.task import Task
from typing import Optional


class TodoCLI:
    """
    Command-line interface for the todo application.
    """

    def __init__(self):
        """
        Initialize the CLI interface with a TaskStore.
        """
        self.task_store = TaskStore()

    def run(self):
        """
        Run the main application loop.
        """
        while True:
            self.display_menu()
            choice = self.get_user_input("Enter your choice: ")

            if choice == "1":
                self.add_task_flow()
            elif choice == "2":
                self.view_tasks_flow()
            elif choice == "3":
                self.update_task_flow()
            elif choice == "4":
                self.delete_task_flow()
            elif choice == "5":
                self.toggle_task_completion_flow()
            elif choice == "6":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")

    def display_menu(self):
        """
        Display the main menu options.
        """
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Completion")
        print("6. Exit")
        print("------------------------")

    def get_user_input(self, prompt: str) -> str:
        """
        Get user input with proper error handling.

        Args:
            prompt (str): The prompt to display to the user

        Returns:
            str: The user's input
        """
        try:
            return input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nApplication interrupted. Exiting...")
            exit()

    def add_task_flow(self):
        """
        Handle the add task flow.
        """
        print("\n--- Add Task ---")

        title = self.get_user_input("Enter task title: ")

        if not title:
            print("Task title cannot be empty.")
            return

        description = self.get_user_input("Enter task description (optional): ")

        try:
            task_id = self.task_store.add_task(title, description)
            print(f"Task added successfully with ID: {task_id}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def format_task_output(self, task: Task) -> str:
        """
        Format a single task for display.

        Args:
            task (Task): The task to format

        Returns:
            str: Formatted string representation of the task
        """
        status = "Completed" if task.completed else "Pending"
        return f"ID: {task.id} | Title: {task.title} | Description: {task.description} | Status: {status}"

    def view_tasks_flow(self):
        """
        Handle the view tasks flow.
        """
        print("\n--- Tasks ---")
        tasks = self.task_store.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            formatted_task = self.format_task_output(task)
            print(formatted_task)

    def update_task_flow(self):
        """
        Handle the update task flow.
        """
        print("\n--- Update Task ---")
        task_id_str = self.get_user_input("Enter task ID to update: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Task ID must be a number.")
            return

        task = self.task_store.get_task(task_id)
        if not task:
            print(f"No task found with ID: {task_id}")
            return

        print(f"Current task: {task.title}")
        new_title = self.get_user_input(f"Enter new title (current: '{task.title}', press Enter to keep current): ")
        new_description = self.get_user_input(f"Enter new description (current: '{task.description}', press Enter to keep current): ")

        # Use current values if user didn't provide new ones
        updated_title = new_title if new_title else task.title
        updated_description = new_description if new_description else task.description

        success = self.task_store.update_task(task_id, updated_title, updated_description)
        if success:
            print(f"Task {task_id} updated successfully.")
        else:
            print(f"Failed to update task {task_id}.")

    def delete_task_flow(self):
        """
        Handle the delete task flow.
        """
        print("\n--- Delete Task ---")
        task_id_str = self.get_user_input("Enter task ID to delete: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Task ID must be a number.")
            return

        success = self.task_store.delete_task(task_id)
        if success:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"No task found with ID: {task_id}")

    def toggle_task_completion_flow(self):
        """
        Handle the toggle task completion flow.
        """
        print("\n--- Toggle Task Completion ---")
        task_id_str = self.get_user_input("Enter task ID to toggle completion: ")

        try:
            task_id = int(task_id_str)
        except ValueError:
            print("Task ID must be a number.")
            return

        success = self.task_store.toggle_task_completion(task_id)
        if success:
            task = self.task_store.get_task(task_id)
            status = "completed" if task.completed else "pending"
            print(f"Task {task_id} marked as {status}.")
        else:
            print(f"No task found with ID: {task_id} or failed to toggle completion.")