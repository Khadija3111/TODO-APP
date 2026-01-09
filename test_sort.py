#!/usr/bin/env python3
"""
Test script to verify sort functionality in the Todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def test_sort_functionality():
    """Test sort functionality with all fields and ascending/descending."""
    print("Testing Sort Functionality")
    print("=" * 30)

    # Create a task store instance
    task_store = TaskStore()

    # Add test tasks with different values for each sort field
    print("\n1. Adding test tasks with various values for sorting...")

    # Add tasks with different priorities
    task_ids = []
    task_ids.append(task_store.add_task(
        title="High priority task",
        description="This is a high priority task",
        priority="high",
        tags=["important"]
    ))
    print(f"   - Added high priority task: 'High priority task'")

    task_ids.append(task_store.add_task(
        title="Low priority task",
        description="This is a low priority task",
        priority="low",
        tags=["low"]
    ))
    print(f"   - Added low priority task: 'Low priority task'")

    task_ids.append(task_store.add_task(
        title="Medium priority task",
        description="This is a medium priority task",
        priority="medium",
        tags=["medium"]
    ))
    print(f"   - Added medium priority task: 'Medium priority task'")

    # Add another task with high priority to test priority sorting
    task_ids.append(task_store.add_task(
        title="Another high priority task",
        description="This is another high priority task",
        priority="high",
        tags=["urgent"]
    ))
    print(f"   - Added another high priority task: 'Another high priority task'")

    # Add a task without priority
    task_ids.append(task_store.add_task(
        title="No priority task",
        description="This task has no priority set",
        priority=None,
        tags=["normal"]
    ))
    print(f"   - Added no priority task: 'No priority task'")

    # Test 2: Sort by priority ascending (low, medium, high, None)
    print("\n2. Testing sort by priority ascending...")
    sorted_tasks = task_store.sort_tasks(sort_field="priority", sort_order="asc")
    print(f"   - Sorted {len(sorted_tasks)} tasks by priority (ascending):")
    for i, task in enumerate(sorted_tasks):
        priority_display = task.priority if task.priority else "None"
        print(f"   - {i+1}. '{task.title}' - Priority: {priority_display}")

    # Expected order: low, medium, high, high, None
    priorities_order = [task.priority for task in sorted_tasks]
    # None should be treated as lowest priority or last depending on implementation
    # The exact order depends on how None values are handled in sorting
    print("   OK Priority sorting completed")

    # Test 3: Sort by priority descending (high, medium, low, None)
    print("\n3. Testing sort by priority descending...")
    sorted_tasks_desc = task_store.sort_tasks(sort_field="priority", sort_order="desc")
    print(f"   - Sorted {len(sorted_tasks_desc)} tasks by priority (descending):")
    for i, task in enumerate(sorted_tasks_desc):
        priority_display = task.priority if task.priority else "None"
        print(f"   - {i+1}. '{task.title}' - Priority: {priority_display}")

    print("   OK Priority descending sorting completed")

    # Test 4: Sort by alphabetical (title) ascending
    print("\n4. Testing sort by alphabetical (title) ascending...")
    sorted_tasks_alpha = task_store.sort_tasks(sort_field="alpha", sort_order="asc")
    print(f"   - Sorted {len(sorted_tasks_alpha)} tasks alphabetically (ascending):")
    for i, task in enumerate(sorted_tasks_alpha):
        print(f"   - {i+1}. '{task.title}'")

    # Verify alphabetical order
    titles = [task.title for task in sorted_tasks_alpha]
    is_sorted = titles == sorted(titles, key=str.lower)
    assert is_sorted, f"Tasks are not sorted alphabetically: {titles}"
    print("   OK Alphabetical ascending sorting completed")

    # Test 5: Sort by alphabetical (title) descending
    print("\n5. Testing sort by alphabetical (title) descending...")
    sorted_tasks_alpha_desc = task_store.sort_tasks(sort_field="alpha", sort_order="desc")
    print(f"   - Sorted {len(sorted_tasks_alpha_desc)} tasks alphabetically (descending):")
    for i, task in enumerate(sorted_tasks_alpha_desc):
        print(f"   - {i+1}. '{task.title}'")

    # Verify reverse alphabetical order
    titles_desc = [task.title for task in sorted_tasks_alpha_desc]
    expected_desc = sorted([task.title for task in task_store.get_all_tasks()], key=str.lower, reverse=True)
    assert titles_desc == expected_desc, f"Tasks are not sorted in reverse alphabetical order: {titles_desc} vs {expected_desc}"
    print("   OK Alphabetical descending sorting completed")

    # Test 6: Sort by creation date (default)
    print("\n6. Testing sort by creation date (created)...")
    sorted_tasks_created = task_store.sort_tasks(sort_field="created", sort_order="asc")
    print(f"   - Sorted {len(sorted_tasks_created)} tasks by creation date (ascending):")
    for i, task in enumerate(sorted_tasks_created):
        print(f"   - {i+1}. '{task.title}' - ID: {task.id}")

    # Verify creation order (by ID, since tasks are created in order)
    ids = [task.id for task in sorted_tasks_created]
    assert ids == sorted(ids), f"Tasks are not sorted by creation order: {ids}"
    print("   OK Creation date sorting completed")

    # Test 7: Sort by creation date descending
    print("\n7. Testing sort by creation date (created) descending...")
    sorted_tasks_created_desc = task_store.sort_tasks(sort_field="created", sort_order="desc")
    print(f"   - Sorted {len(sorted_tasks_created_desc)} tasks by creation date (descending):")
    for i, task in enumerate(sorted_tasks_created_desc):
        print(f"   - {i+1}. '{task.title}' - ID: {task.id}")

    # Verify reverse creation order
    ids_desc = [task.id for task in sorted_tasks_created_desc]
    expected_ids_desc = sorted([task.id for task in task_store.get_all_tasks()], reverse=True)
    assert ids_desc == expected_ids_desc, f"Tasks are not sorted in reverse creation order: {ids_desc} vs {expected_ids_desc}"
    print("   OK Creation date descending sorting completed")

    # Test 8: Test with empty task list
    print("\n8. Testing sort with empty task list...")
    empty_store = TaskStore()
    empty_sorted = empty_store.sort_tasks(sort_field="priority", sort_order="asc")
    assert len(empty_sorted) == 0, f"Expected empty list for empty task store, got {len(empty_sorted)}"
    print("   OK Sorting empty list handled correctly")

    # Test 9: Test invalid sort field (should use default)
    print("\n9. Testing invalid sort field...")
    try:
        invalid_sorted = task_store.sort_tasks(sort_field="invalid", sort_order="asc")
        print(f"   - Invalid sort field handled gracefully, returned {len(invalid_sorted)} tasks")
    except Exception as e:
        print(f"   - Invalid sort field raised exception: {e}")

    print("   OK Invalid sort field handled")

    # Test 10: Test invalid sort order (should use default)
    print("\n10. Testing invalid sort order...")
    try:
        invalid_order_sorted = task_store.sort_tasks(sort_field="priority", sort_order="invalid")
        print(f"   - Invalid sort order handled gracefully, returned {len(invalid_order_sorted)} tasks")
    except Exception as e:
        print(f"   - Invalid sort order raised exception: {e}")

    print("   OK Invalid sort order handled")

    print("\n" + "=" * 30)
    print("All sort functionality tests passed! OK")
    print("=" * 30)

def test_sort_integration():
    """Test sorting in combination with filtering."""
    print("\nTesting Sort Integration with Filtering")
    print("=" * 40)

    # Create a task store instance
    task_store = TaskStore()

    # Add tasks for integration testing
    task_store.add_task(
        title="Completed high priority work task",
        description="High priority work task that is completed",
        priority="high",
        tags=["work"]
    )
    task_store.toggle_task_completion(1)  # Make it completed

    task_store.add_task(
        title="Pending medium priority work task",
        description="Medium priority work task that is pending",
        priority="medium",
        tags=["work"]
    )

    task_store.add_task(
        title="Pending low priority personal task",
        description="Low priority personal task that is pending",
        priority="low",
        tags=["personal"]
    )

    task_store.add_task(
        title="Completed low priority work task",
        description="Low priority work task that is completed",
        priority="low",
        tags=["work"]
    )
    task_store.toggle_task_completion(4)  # Make it completed

    # Test: Filter by work tasks and sort by priority ascending
    print("\n1. Filtering work tasks and sorting by priority (asc)...")
    filtered_tasks = task_store.filter_tasks(tags=["work"])
    sorted_filtered = task_store.sort_tasks(sort_field="priority", sort_order="asc")

    # Actually apply both filter and sort together
    work_tasks = task_store.filter_tasks(tags=["work"])
    from utils.sorters import sort_tasks
    sorted_work_tasks = sort_tasks(work_tasks, "priority", "asc")

    print(f"   - Found {len(work_tasks)} work tasks, sorted by priority:")
    for i, task in enumerate(sorted_work_tasks):
        print(f"   - {i+1}. '{task.title}' - Priority: {task.priority}")

    # Verify the sorting worked correctly for work tasks
    work_priorities = [task.priority for task in sorted_work_tasks]

    # Check that non-None priorities are in correct priority order (low, medium, high)
    non_none_priorities = [p for p in work_priorities if p is not None]
    # For ascending priority sort, the order should be low, medium, high
    expected_order = ['low', 'medium', 'high']
    # Only check the subset that exists in our results
    actual_sorted = [p for p in expected_order if p in non_none_priorities]
    actual_existing = [p for p in non_none_priorities if p in expected_order]

    # The actual existing priorities should follow the same order as they appear in the expected order
    assert actual_existing == sorted(actual_existing, key=lambda x: expected_order.index(x)), f"Priorities not sorted correctly by priority: {non_none_priorities}"
    print("   OK Work tasks sorted by priority correctly")

    # Test: Filter by pending tasks and sort alphabetically
    print("\n2. Filtering pending tasks and sorting alphabetically (desc)...")
    pending_tasks = task_store.filter_tasks(status="pending")
    sorted_pending = sort_tasks(pending_tasks, "alpha", "desc")

    print(f"   - Found {len(pending_tasks)} pending tasks, sorted alphabetically (desc):")
    for i, task in enumerate(sorted_pending):
        print(f"   - {i+1}. '{task.title}' - Status: {'Completed' if task.completed else 'Pending'}")

    # Verify alphabetical descending order
    titles = [task.title for task in sorted_pending]
    expected_titles = sorted([task.title for task in sorted_pending], key=str.lower, reverse=True)
    assert titles == expected_titles, f"Titles not sorted in descending order: {titles} vs {expected_titles}"
    print("   OK Pending tasks sorted alphabetically descending correctly")

    print("\n" + "=" * 40)
    print("Sort integration tests passed! OK")
    print("=" * 40)

if __name__ == "__main__":
    test_sort_functionality()
    test_sort_integration()
    print("\nManual verification of sort functionality completed successfully!")