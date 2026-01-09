#!/usr/bin/env python3
"""
Test script to verify filter functionality in the Todo application.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from services.task_store import TaskStore

def test_filter_combinations():
    """Test filter combinations (status + priority, status + tags, etc.)."""
    print("Testing Filter Combinations")
    print("=" * 35)

    # Create a task store instance
    task_store = TaskStore()

    # Add test tasks with different combinations of status, priority, and tags
    print("\n1. Adding test tasks with various combinations...")

    # High priority work task, completed
    task_ids = []
    task_ids.append(task_store.add_task(
        title="Complete project proposal",
        description="Finish the project proposal document",
        priority="high",
        tags=["work", "important"]
    ))
    # Toggle to completed
    task_store.toggle_task_completion(task_ids[0])  # This makes task ID 1 completed
    print(f"   - Added completed high priority work task: 'Complete project proposal'")

    # Medium priority personal task, pending
    task_ids.append(task_store.add_task(
        title="Buy groceries",
        description="Buy weekly groceries",
        priority="medium",
        tags=["personal", "shopping"]
    ))
    print(f"   - Added pending medium priority personal task: 'Buy groceries'")

    # Low priority learning task, pending
    task_ids.append(task_store.add_task(
        title="Read Python documentation",
        description="Read about new Python features",
        priority="low",
        tags=["learning", "python"]
    ))
    print(f"   - Added pending low priority learning task: 'Read Python documentation'")

    # High priority urgent task, pending
    task_ids.append(task_store.add_task(
        title="Fix critical bug",
        description="Fix the critical bug in production",
        priority="high",
        tags=["urgent", "work", "bug"]
    ))
    print(f"   - Added pending high priority urgent task: 'Fix critical bug'")

    # Medium priority work task, completed
    task_ids.append(task_store.add_task(
        title="Review code changes",
        description="Review team's code changes",
        priority="medium",
        tags=["work", "review"]
    ))
    # Toggle to completed
    task_store.toggle_task_completion(task_ids[4])  # This makes the 5th task (which has ID 5) completed
    print(f"   - Added completed medium priority work task: 'Review code changes'")

    # Low priority personal task, pending
    task_ids.append(task_store.add_task(
        title="Plan weekend trip",
        description="Plan the upcoming weekend trip",
        priority="low",
        tags=["personal", "trip"]
    ))
    print(f"   - Added pending low priority personal task: 'Plan weekend trip'")

    # Test 2: Filter by status only (completed)
    print("\n2. Testing filter by status (completed)...")
    completed_tasks = task_store.filter_tasks(status="completed")
    print(f"   - Found {len(completed_tasks)} completed task(s)")
    for task in completed_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Tags: {task.tags}, Status: {'Completed' if task.completed else 'Pending'}")

    assert len(completed_tasks) == 2, f"Expected 2 completed tasks, got {len(completed_tasks)}"
    print("   OK Found correct number of completed tasks")

    # Test 3: Filter by priority only (high)
    print("\n3. Testing filter by priority (high)...")
    high_priority_tasks = task_store.filter_tasks(priority="high")
    print(f"   - Found {len(high_priority_tasks)} high priority task(s)")
    for task in high_priority_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Status: {'Completed' if task.completed else 'Pending'}")

    assert len(high_priority_tasks) == 2, f"Expected 2 high priority tasks, got {len(high_priority_tasks)}"
    print("   OK Found correct number of high priority tasks")

    # Test 4: Filter by tags only (work)
    print("\n4. Testing filter by tags (work)...")
    work_tasks = task_store.filter_tasks(tags=["work"])
    print(f"   - Found {len(work_tasks)} work task(s)")
    for task in work_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Tags: {task.tags}")

    assert len(work_tasks) == 3, f"Expected 3 work tasks, got {len(work_tasks)}"
    print("   OK Found correct number of work tasks")

    # Test 5: Filter by status AND priority (completed + high)
    print("\n5. Testing filter by status AND priority (completed + high)...")
    completed_high_tasks = task_store.filter_tasks(status="completed", priority="high")
    print(f"   - Found {len(completed_high_tasks)} completed high priority task(s)")
    for task in completed_high_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Status: {'Completed' if task.completed else 'Pending'}")

    assert len(completed_high_tasks) == 1, f"Expected 1 completed high priority task, got {len(completed_high_tasks)}"
    print("   OK Found correct number of completed high priority tasks")

    # Test 6: Filter by status AND tags (pending + work)
    print("\n6. Testing filter by status AND tags (pending + work)...")
    pending_work_tasks = task_store.filter_tasks(status="pending", tags=["work"])
    print(f"   - Found {len(pending_work_tasks)} pending work task(s)")
    for task in pending_work_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Tags: {task.tags}, Status: {'Completed' if task.completed else 'Pending'}")

    assert len(pending_work_tasks) == 1, f"Expected 1 pending work task, got {len(pending_work_tasks)}"
    print("   OK Found correct number of pending work tasks")

    # Test 7: Filter by priority AND tags (high + urgent)
    print("\n7. Testing filter by priority AND tags (high + urgent)...")
    high_urgent_tasks = task_store.filter_tasks(priority="high", tags=["urgent"])
    print(f"   - Found {len(high_urgent_tasks)} high priority urgent task(s)")
    for task in high_urgent_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Tags: {task.tags}")

    assert len(high_urgent_tasks) == 1, f"Expected 1 high priority urgent task, got {len(high_urgent_tasks)}"
    print("   OK Found correct number of high priority urgent tasks")

    # Test 8: Filter by status, priority, AND tags (pending + high + work)
    print("\n8. Testing filter by status, priority, AND tags (pending + high + work)...")
    pending_high_work_tasks = task_store.filter_tasks(status="pending", priority="high", tags=["work"])
    print(f"   - Found {len(pending_high_work_tasks)} pending high priority work task(s)")
    for task in pending_high_work_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Priority: {task.priority}, Tags: {task.tags}, Status: {'Completed' if task.completed else 'Pending'}")

    assert len(pending_high_work_tasks) == 1, f"Expected 1 pending high priority work task, got {len(pending_high_work_tasks)}"
    print("   OK Found correct number of pending high priority work tasks")

    # Test 9: Filter by tags with multiple tags (work OR important)
    print("\n9. Testing filter by multiple tags (work OR important)...")
    work_important_tasks = task_store.filter_tasks(tags=["work", "important"])
    print(f"   - Found {len(work_important_tasks)} work OR important task(s)")
    for task in work_important_tasks:
        print(f"   - ID: {task.id}, Title: '{task.title}', Tags: {task.tags}")

    assert len(work_important_tasks) == 3, f"Expected 3 work OR important tasks, got {len(work_important_tasks)}"
    print("   OK Found correct number of work OR important tasks")

    # Test 10: Filter that returns no results
    print("\n10. Testing filter that should return no results (completed + low + urgent)...")
    no_results_tasks = task_store.filter_tasks(status="completed", priority="low", tags=["urgent"])
    print(f"   - Found {len(no_results_tasks)} completed low priority urgent task(s)")

    assert len(no_results_tasks) == 0, f"Expected 0 completed low priority urgent tasks, got {len(no_results_tasks)}"
    print("   OK Correctly found no tasks for impossible combination")

    print("\n" + "=" * 35)
    print("All filter combination tests passed! OK")
    print("=" * 35)

def test_filter_combinations_verification():
    """Verify filters work in any combination as specified."""
    print("\nVerifying Filters Work in Any Combination")
    print("=" * 45)

    # Create a task store instance
    task_store = TaskStore()

    # Add tasks with various combinations
    task_store.add_task(
        title="Urgent high priority work task",
        description="This is urgent work that needs high priority",
        priority="high",
        tags=["work", "urgent", "important"]
    )
    task_store.toggle_task_completion(1)  # Make it completed

    task_store.add_task(
        title="Low priority personal task",
        description="This is a low priority personal task",
        priority="low",
        tags=["personal", "low-priority"]
    )

    task_store.add_task(
        title="Medium priority learning task",
        description="Learning new technology",
        priority="medium",
        tags=["learning", "development"]
    )
    task_store.toggle_task_completion(3)  # Make it completed

    # Test all possible combinations
    combinations = [
        ("all statuses with high priority", {"priority": "high"}),
        ("pending with any priority", {"status": "pending"}),
        ("completed with any priority", {"status": "completed"}),
        ("work tasks with any priority", {"tags": ["work"]}),
        ("completed high priority", {"status": "completed", "priority": "high"}),
        ("pending low priority", {"status": "pending", "priority": "low"}),
        ("work AND urgent", {"tags": ["work", "urgent"]}),
        ("completed work tasks", {"status": "completed", "tags": ["work"]}),
        ("high priority learning", {"priority": "high", "tags": ["learning"]}),  # Should return 0
        ("pending personal tasks", {"status": "pending", "tags": ["personal"]}),
    ]

    for desc, filters in combinations:
        status_filter = filters.get('status')
        priority_filter = filters.get('priority')
        tags_filter = filters.get('tags')

        results = task_store.filter_tasks(
            status=status_filter,
            priority=priority_filter,
            tags=tags_filter
        )
        print(f"   - {desc}: {len(results)} task(s) found")

        # Basic validation - just ensure no errors occur
        assert isinstance(results, list), f"Filter should return a list, got {type(results)}"

    print("   OK All filter combinations work without errors")
    print("Verification completed successfully!")

if __name__ == "__main__":
    test_filter_combinations()
    test_filter_combinations_verification()
    print("\nManual verification of filter combinations completed successfully!")