"""
CLI Interface

This module provides the command-line interface for the todo application.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from services.task_store import TaskStore
from services.config_service import ConfigService
from backend.models.task import Task
from typing import Optional, List
from utils.sorters import sort_tasks
from cli.renderers import format_task_output


class TodoCLI:
    """
    Command-line interface for the todo application.
    """

    def __init__(self, use_color=True):
        """
        Initialize the CLI interface with a TaskStore.
        """
        self.task_store = TaskStore()
        self.config_service = ConfigService()
        self.use_color = use_color  # Default to using color unless disabled

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
                self.search_tasks_flow()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                print("Exiting the application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

    def display_menu(self):
        """
        Display the main menu options.
        """
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks (with optional filtering and sorting)")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Toggle Task Completion")
        print("6. Search Tasks")
        print("7. Help")
        print("8. Exit")
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

    def show_help(self):
        """
        Display help information with examples of all new features.
        """
        print("\n--- Help - Todo Application ---")
        print("This application allows you to manage your tasks with the following features:")
        print()
        print("BASIC FEATURES:")
        print("  • Add tasks with title and optional description")
        print("  • View all tasks with their completion status")
        print("  • Update task title and description")
        print("  • Delete tasks")
        print("  • Mark tasks as complete/incomplete")
        print()
        print("INTERMEDIATE FEATURES:")
        print("  • PRIORITIES: Assign priority levels (high/medium/low) to tasks")
        print("    Example: When adding a task, enter 'high', 'medium', or 'low' for priority")
        print()
        print("  • TAGS: Add one or more tags to tasks for better organization")
        print("    Example: When adding a task, enter comma-separated tags like 'work,urgent'")
        print()
        print("  • SEARCH: Find tasks by keywords in title or description")
        print("    Example: Use option 6 to search for specific terms")
        print()
        print("  • FILTER: Filter tasks by status, priority, and tags")
        print("    Example: In View Tasks (option 2), specify filters when prompted")
        print()
        print("  • SORT: Sort tasks by due date, priority, alphabetical, or creation date")
        print("    Example: In View Tasks (option 2), specify sort options when prompted")
        print()
        print("  • CONFIGURATION: Persistent sort preferences stored in config file")
        print("    Example: Your last used sort settings are saved automatically")
        print()
        print("  • ANSI COLORS: Enhanced output with color coding for better readability")
        print("    Note: Use --no-color flag when running the application to disable colors")
        print()
        print("USAGE EXAMPLES:")
        print("  1. Add a high priority work task with tags:")
        print("     - Choose option 1")
        print("     - Enter title: 'Complete project'")
        print("     - Enter priority: 'high'")
        print("     - Enter tags: 'work,important'")
        print()
        print("  2. View tasks with filters and sorting:")
        print("     - Choose option 2")
        print("     - Filter by priority: 'high'")
        print("     - Sort by: 'priority'")
        print("     - Sort order: 'desc'")
        print()
        print("  3. Search for specific tasks:")
        print("     - Choose option 6")
        print("     - Enter keyword: 'project'")
        print()
        print("Press Enter to return to the main menu...")
        input()

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

        # Get priority
        priority = self.get_user_input("Enter priority (high/medium/low, optional): ")
        if priority and priority.lower() not in ['high', 'medium', 'low']:
            print("Invalid priority. Using no priority.")
            priority = None
        elif priority:
            priority = priority.lower()
        else:
            priority = None

        # Get tags
        tags_input = self.get_user_input("Enter tags (comma-separated, optional): ")
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]

        try:
            task_id = self.task_store.add_task(title, description, priority, tags)
            print(f"Task added successfully with ID: {task_id}")
            if priority:
                print(f"Priority: {priority}")
            if tags:
                print(f"Tags: {', '.join(tags)}")
        except ValueError as e:
            print(f"Error adding task: {e}")
            # In CLI context, we don't want to exit the whole application
            # just continue the loop

    def view_tasks_flow(self):
        """
        Handle the view tasks flow.
        """
        print("\n--- Tasks ---")

        # Get filter options from user
        print("Filter options (press Enter to skip):")
        status_filter = self.get_user_input("Filter by status (all/pending/completed): ")
        if status_filter.lower() in ['all', 'pending', 'completed', '']:
            if status_filter == '':
                status_filter = None
        else:
            print("Invalid status. Using no filter.")
            status_filter = None

        priority_filter = self.get_user_input("Filter by priority (high/medium/low/any): ")
        if priority_filter.lower() in ['high', 'medium', 'low', 'any', '']:
            if priority_filter == '':
                priority_filter = None
        else:
            print("Invalid priority. Using no filter.")
            priority_filter = None

        tags_filter_input = self.get_user_input("Filter by tags (comma-separated): ")
        tags_filter = None
        if tags_filter_input:
            tags_filter = [tag.strip() for tag in tags_filter_input.split(',') if tag.strip()]

        # Get sort options from user
        print("\nSort options (press Enter to use default from config):")
        sort_field = self.get_user_input("Sort by (created/priority/alpha/due): ")
        if sort_field.lower() in ['created', 'priority', 'alpha', 'due', '']:
            if sort_field == '':
                # Use default from config
                sort_field = self.config_service.get_config_value('default_sort_field', 'created')
            else:
                sort_field = sort_field.lower()
                # Update config with user's choice
                self.config_service.set_config_value('last_used_sort_field', sort_field)
        else:
            print("Invalid sort field. Using default 'created'.")
            sort_field = 'created'

        sort_order = self.get_user_input("Sort order (asc/desc): ")
        if sort_order.lower() in ['asc', 'desc', '']:
            if sort_order == '':
                # Use default from config
                sort_order = self.config_service.get_config_value('default_sort_order', 'asc')
            else:
                sort_order = sort_order.lower()
                # Update config with user's choice
                self.config_service.set_config_value('last_used_sort_order', sort_order)
        else:
            print("Invalid sort order. Using default 'asc'.")
            sort_order = 'asc'

        # Apply filters if any are specified
        if status_filter or priority_filter or tags_filter:
            try:
                filtered_tasks = self.task_store.filter_tasks(status_filter, priority_filter, tags_filter)
            except Exception as e:
                print(f"Error applying filters: {e}")
                print("Please check your filter criteria and try again.")
                return
        else:
            filtered_tasks = self.task_store.get_all_tasks()

        if not filtered_tasks:
            print("No tasks found with the specified filters.")
            return

        # Sort tasks based on user's choice
        sorted_tasks = sort_tasks(filtered_tasks, sort_field, sort_order)

        print(f"Displaying {len(sorted_tasks)} task(s), sorted by {sort_field} ({sort_order}):")
        for task in sorted_tasks:
            formatted_task = format_task_output(task, self.use_color)
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

        # Get new priority
        new_priority_input = self.get_user_input(f"Enter new priority (high/medium/low, current: '{task.priority or 'None'}', press Enter to keep current): ")
        if new_priority_input == "":
            # User pressed Enter, don't update priority
            new_priority = task.priority  # Keep current value
        elif new_priority_input.lower() == "none" or new_priority_input.lower() == "null":
            # User explicitly wants to remove priority
            new_priority = None
        elif new_priority_input.lower() not in ['high', 'medium', 'low']:
            print("Invalid priority. Keeping current priority.")
            new_priority = task.priority  # Keep current value
        else:
            new_priority = new_priority_input.lower()

        # Get new tags
        new_tags_input = self.get_user_input(f"Enter new tags (comma-separated, current: '{', '.join(task.tags) if task.tags else 'None'}', press Enter to keep current): ")
        if new_tags_input == "":
            # User pressed Enter, don't update tags
            new_tags = task.tags  # Keep current value
        elif new_tags_input.lower() == "none" or new_tags_input.lower() == "null":
            # User explicitly wants to remove tags
            new_tags = []
        else:
            new_tags = [tag.strip() for tag in new_tags_input.split(',') if tag.strip()]

        # Only update fields that the user explicitly provided
        # For title and description, if empty string was provided, keep current
        # For priority and tags, we've already handled the logic above
        success = self.task_store.update_task(
            task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None,
            priority=new_priority if new_priority != task.priority else None,
            tags=new_tags if new_tags != task.tags else None
        )
        if success:
            print(f"Task {task_id} updated successfully.")
            # Show the new values that were actually updated
            if new_title:
                print(f"New title: {new_title}")
            if new_description:
                print(f"New description: {new_description}")
            if new_priority != task.priority:  # Only print if it actually changed
                print(f"New priority: {new_priority}")
            if new_tags != task.tags:  # Only print if it actually changed
                print(f"New tags: {', '.join(new_tags) if new_tags else '[]'}")
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

    def search_tasks_flow(self):
        """
        Handle the search tasks flow.
        """
        print("\n--- Search Tasks ---")
        keyword = self.get_user_input("Enter search keyword: ")

        if not keyword:
            print("Search keyword cannot be empty.")
            return

        try:
            matching_tasks = self.task_store.search_tasks(keyword)
            if matching_tasks:
                print(f"\nFound {len(matching_tasks)} task(s) matching '{keyword}':")
                for task in matching_tasks:
                    formatted_task = format_task_output(task, self.use_color)
                    print(formatted_task)
            else:
                print(f"No tasks found matching '{keyword}'.")
        except Exception as e:
            print(f"Error during search: {e}")
            print("Please try searching with a different keyword or contact support if the problem persists.")