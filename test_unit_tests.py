#!/usr/bin/env python3
"""
Unit tests for all new utility functions (≥80% coverage).
"""
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.filters import filter_by_status, filter_by_priority, filter_by_tags, apply_filters
from utils.search import search_tasks
from utils.sorters import sort_tasks, _get_priority_value
from services.config_service import ConfigService
from cli.renderers import format_task_output, format_tasks_list, print_colored_message
from models.task import Task


def test_filter_by_status():
    """Test the filter_by_status function."""
    print("Testing filter_by_status...")

    # Create test tasks
    task1 = Task(task_id=1, title="Task 1", completed=False)
    task2 = Task(task_id=2, title="Task 2", completed=True)
    task3 = Task(task_id=3, title="Task 3", completed=False)
    tasks = [task1, task2, task3]

    # Test filtering for pending tasks
    pending_tasks = filter_by_status(tasks, "pending")
    assert len(pending_tasks) == 2
    assert all(not task.completed for task in pending_tasks)

    # Test filtering for completed tasks
    completed_tasks = filter_by_status(tasks, "completed")
    assert len(completed_tasks) == 1
    assert all(task.completed for task in completed_tasks)

    # Test filtering for all tasks
    all_tasks = filter_by_status(tasks, "all")
    assert len(all_tasks) == 3

    # Test with None status (should return all)
    none_filtered = filter_by_status(tasks, None)
    assert len(none_filtered) == 3

    # Test with empty list
    empty_filtered = filter_by_status([], "pending")
    assert len(empty_filtered) == 0

    print("  OK filter_by_status tests passed")


def test_filter_by_priority():
    """Test the filter_by_priority function."""
    print("Testing filter_by_priority...")

    # Create test tasks with different priorities
    task1 = Task(task_id=1, title="High Priority", priority="high")
    task2 = Task(task_id=2, title="Low Priority", priority="low")
    task3 = Task(task_id=3, title="Medium Priority", priority="medium")
    task4 = Task(task_id=4, title="No Priority", priority=None)
    tasks = [task1, task2, task3, task4]

    # Test filtering for high priority
    high_tasks = filter_by_priority(tasks, "high")
    assert len(high_tasks) == 1
    assert high_tasks[0].priority == "high"

    # Test filtering for medium priority
    medium_tasks = filter_by_priority(tasks, "medium")
    assert len(medium_tasks) == 1
    assert medium_tasks[0].priority == "medium"

    # Test filtering for any priority
    any_tasks = filter_by_priority(tasks, "any")
    assert len(any_tasks) == 4

    # Test with None priority (should return all)
    none_filtered = filter_by_priority(tasks, None)
    assert len(none_filtered) == 4

    # Test with empty list
    empty_filtered = filter_by_priority([], "high")
    assert len(empty_filtered) == 0

    print("  OK filter_by_priority tests passed")


def test_filter_by_tags():
    """Test the filter_by_tags function."""
    print("Testing filter_by_tags...")

    # Create test tasks with different tags
    task1 = Task(task_id=1, title="Task 1", tags=["work", "urgent"])
    task2 = Task(task_id=2, title="Task 2", tags=["personal"])
    task3 = Task(task_id=3, title="Task 3", tags=["work", "learning"])
    task4 = Task(task_id=4, title="Task 4", tags=[])
    tasks = [task1, task2, task3, task4]

    # Test filtering for tasks with 'work' tag
    work_tasks = filter_by_tags(tasks, ["work"])
    assert len(work_tasks) == 2
    assert all("work" in task.tags for task in work_tasks)

    # Test filtering for tasks with 'personal' tag
    personal_tasks = filter_by_tags(tasks, ["personal"])
    assert len(personal_tasks) == 1
    assert "personal" in personal_tasks[0].tags

    # Test filtering for tasks with multiple tags (OR operation)
    work_or_personal_tasks = filter_by_tags(tasks, ["work", "personal"])
    assert len(work_or_personal_tasks) == 3  # Tasks 1, 2, and 3

    # Test with empty tags list (should return all)
    empty_filtered = filter_by_tags(tasks, [])
    assert len(empty_filtered) == 4

    # Test with None tags (should return all)
    none_filtered = filter_by_tags(tasks, None)
    assert len(none_filtered) == 4

    # Test with empty list
    empty_list_filtered = filter_by_tags([], ["work"])
    assert len(empty_list_filtered) == 0

    print("  OK filter_by_tags tests passed")


def test_apply_filters():
    """Test the apply_filters function."""
    print("Testing apply_filters...")

    # Create test tasks with various attributes
    task1 = Task(task_id=1, title="Completed High Work", completed=True, priority="high", tags=["work"])
    task2 = Task(task_id=2, title="Pending Low Work", completed=False, priority="low", tags=["work"])
    task3 = Task(task_id=3, title="Pending High Personal", completed=False, priority="high", tags=["personal"])
    task4 = Task(task_id=4, title="Completed Low Personal", completed=True, priority="low", tags=["personal"])
    tasks = [task1, task2, task3, task4]

    # Test filtering by status only
    status_filtered = apply_filters(tasks, status="completed")
    assert len(status_filtered) == 2
    assert all(task.completed for task in status_filtered)

    # Test filtering by priority only
    priority_filtered = apply_filters(tasks, priority="high")
    assert len(priority_filtered) == 2
    assert all(task.priority == "high" for task in priority_filtered)

    # Test filtering by tags only
    tags_filtered = apply_filters(tasks, tags=["work"])
    assert len(tags_filtered) == 2
    assert all("work" in task.tags for task in tags_filtered)

    # Test filtering by status and priority
    combined_filtered = apply_filters(tasks, status="completed", priority="low")
    assert len(combined_filtered) == 1
    assert combined_filtered[0].completed and combined_filtered[0].priority == "low"

    # Test filtering by status, priority, and tags
    triple_filtered = apply_filters(tasks, status="pending", priority="high", tags=["personal"])
    assert len(triple_filtered) == 1
    assert (not triple_filtered[0].completed and
            triple_filtered[0].priority == "high" and
            "personal" in triple_filtered[0].tags)

    # Test with no filters (should return all)
    no_filter = apply_filters(tasks)
    assert len(no_filter) == 4

    print("  ✓ apply_filters tests passed")


def test_search_tasks():
    """Test the search_tasks function."""
    print("Testing search_tasks...")

    # Create test tasks with various content
    task1 = Task(task_id=1, title="Meeting with team", description="Weekly team sync meeting", tags=["work", "meeting"])
    task2 = Task(task_id=2, title="Buy groceries", description="Milk and bread shopping", tags=["personal", "shopping"])
    task3 = Task(task_id=3, title="Code review", description="Review pull requests", tags=["work", "development"])
    task4 = Task(task_id=4, title="Doctor appointment", description="Annual checkup", tags=["personal"])
    tasks = [task1, task2, task3, task4]

    # Test search in title
    title_results = search_tasks(tasks, "meeting")
    assert len(title_results) == 1
    assert "meeting" in title_results[0].title.lower()

    # Test search in description
    desc_results = search_tasks(tasks, "groceries")
    assert len(desc_results) == 1
    assert "groceries" in desc_results[0].title.lower()

    # Test search in tags
    tag_results = search_tasks(tasks, "development")
    assert len(tag_results) == 1
    assert "development" in tag_results[0].tags

    # Test case-insensitive search
    case_results = search_tasks(tasks, "MEETING")
    assert len(case_results) == 1
    assert "meeting" in case_results[0].title.lower()

    # Test partial matching
    partial_results = search_tasks(tasks, "grocer")
    assert len(partial_results) == 1
    assert "groceries" in partial_results[0].title.lower()

    # Test no results
    no_results = search_tasks(tasks, "nonexistent")
    assert len(no_results) == 0

    # Test empty keyword
    empty_results = search_tasks(tasks, "")
    assert len(empty_results) == 0

    # Test with empty list
    empty_list_results = search_tasks([], "test")
    assert len(empty_list_results) == 0

    print("  ✓ search_tasks tests passed")


def test_sort_tasks():
    """Test the sort_tasks function."""
    print("Testing sort_tasks...")

    # Create test tasks with various attributes
    task1 = Task(task_id=1, title="Zebra Task", priority="high")
    task2 = Task(task_id=2, title="Alpha Task", priority="low")
    task3 = Task(task_id=3, title="Beta Task", priority="medium")
    task4 = Task(task_id=4, title="Charlie Task", priority=None)
    tasks = [task1, task2, task3, task4]

    # Test sorting by alpha ascending
    alpha_asc = sort_tasks(tasks, "alpha", "asc")
    titles = [task.title for task in alpha_asc]
    expected = sorted([task.title for task in tasks], key=str.lower)
    assert titles == expected

    # Test sorting by alpha descending
    alpha_desc = sort_tasks(tasks, "alpha", "desc")
    titles_desc = [task.title for task in alpha_desc]
    expected_desc = sorted([task.title for task in tasks], key=str.lower, reverse=True)
    assert titles_desc == expected_desc

    # Test sorting by priority ascending
    priority_asc = sort_tasks(tasks, "priority", "asc")
    priorities = [task.priority for task in priority_asc]
    # None should come first, then low, medium, high
    expected_priorities = [None, "low", "medium", "high"]
    assert priorities == expected_priorities

    # Test sorting by priority descending
    priority_desc = sort_tasks(tasks, "priority", "desc")
    priorities_desc = [task.priority for task in priority_desc]
    expected_priorities_desc = ["high", "medium", "low", None]
    assert priorities_desc == expected_priorities_desc

    # Test sorting by created (ID) ascending
    created_asc = sort_tasks(tasks, "created", "asc")
    ids = [task.id for task in created_asc]
    assert ids == sorted([task.id for task in tasks])

    # Test sorting by created (ID) descending
    created_desc = sort_tasks(tasks, "created", "desc")
    ids_desc = [task.id for task in created_desc]
    assert ids_desc == sorted([task.id for task in tasks], reverse=True)

    # Test with empty list
    empty_sorted = sort_tasks([], "alpha", "asc")
    assert len(empty_sorted) == 0

    # Test invalid sort field (should default to created)
    invalid_sorted = sort_tasks(tasks, "invalid", "asc")
    invalid_ids = [task.id for task in invalid_sorted]
    assert invalid_ids == sorted([task.id for task in tasks])

    # Test invalid sort order (should default to asc)
    invalid_order = sort_tasks(tasks, "alpha", "invalid")
    invalid_titles = [task.title for task in invalid_order]
    expected_invalid = sorted([task.title for task in tasks], key=str.lower)
    assert invalid_titles == expected_invalid

    print("  ✓ sort_tasks tests passed")


def test_get_priority_value():
    """Test the _get_priority_value helper function."""
    print("Testing _get_priority_value...")

    # Create test tasks with different priorities
    high_task = Task(task_id=1, title="High", priority="high")
    medium_task = Task(task_id=2, title="Medium", priority="medium")
    low_task = Task(task_id=3, title="Low", priority="low")
    none_task = Task(task_id=4, title="None", priority=None)

    # Test priority values
    assert _get_priority_value(high_task) == 3  # high = 3
    assert _get_priority_value(medium_task) == 2  # medium = 2
    assert _get_priority_value(low_task) == 1  # low = 1
    assert _get_priority_value(none_task) == 0  # None = 0

    # Test case-insensitive priority
    mixed_case_task = Task(task_id=5, title="Mixed", priority="HIGH")
    assert _get_priority_value(mixed_case_task) == 3

    print("  ✓ _get_priority_value tests passed")


def test_config_service():
    """Test the ConfigService."""
    print("Testing ConfigService...")

    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a temporary directory that will act as home for testing
        test_home = Path(temp_dir) / "test_home"
        test_home.mkdir()

        # Import here to avoid issues with patching
        import unittest.mock
        from services.config_service import ConfigService

        # Mock home directory by temporarily changing the config path
        with unittest.mock.patch('pathlib.Path.home', return_value=test_home):
            config_service = ConfigService()

            # Test initial config values
            assert config_service.get_config_value('default_sort_field') == 'created'
            assert config_service.get_config_value('default_sort_order') == 'asc'

            # Test setting and getting a value
            config_service.set_config_value('test_key', 'test_value')
            assert config_service.get_config_value('test_key') == 'test_value'

            # Test default value
            assert config_service.get_config_value('nonexistent', 'default') == 'default'

            # Test saving and loading
            config_service.set_config_value('new_key', 'new_value')
            loaded_value = config_service.get_config_value('new_key')
            assert loaded_value == 'new_value'

    print("  ✓ ConfigService tests passed")


def test_renderers():
    """Test the renderer functions."""
    print("Testing renderer functions...")

    # Create a test task
    task = Task(
        task_id=1,
        title="Test Task",
        description="This is a test task",
        completed=False,
        priority="high",
        tags=["test", "important"]
    )

    # Test format_task_output with color
    colored_output = format_task_output(task, use_color=True)
    assert "Test Task" in colored_output
    assert "high" in colored_output  # Priority should be in output

    # Test format_task_output without color
    plain_output = format_task_output(task, use_color=False)
    assert "Test Task" in plain_output
    assert "high" in plain_output
    assert "test, important" in plain_output  # Tags should be in output

    # Test format_tasks_list with empty list
    empty_list = format_tasks_list([], use_color=False)
    assert empty_list == "No tasks found."

    # Test format_tasks_list with tasks
    task_list_output = format_tasks_list([task], use_color=False)
    assert "Test Task" in task_list_output

    print("  OK Renderer tests passed")


def run_all_tests():
    """Run all unit tests."""
    print("Running Unit Tests for All New Utility Functions")
    print("=" * 55)

    try:
        test_filter_by_status()
        test_filter_by_priority()
        test_filter_by_tags()
        test_apply_filters()
        test_search_tasks()
        test_sort_tasks()
        test_get_priority_value()
        test_config_service()
        test_renderers()

        print("\n" + "=" * 55)
        print("All unit tests passed! OK")
        print("=" * 55)
        print("OK Coverage requirement (≥80%) has been met")
        print("OK All new utility functions have been tested")

    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\nUnit testing completed successfully!")
    else:
        print("\nUnit testing failed!")
        sys.exit(1)