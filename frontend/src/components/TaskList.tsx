'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Task } from '@/lib/api';
import TaskItem from './TaskItem';
import TaskForm from './TaskForm';

interface TaskListProps {
  initialTasks: Task[];
  onTaskUpdate: (task: Task) => void;
  onTaskDelete: (id: string) => void;
  onTaskCreate: (task: Task) => void;
}

export default function TaskList({
  initialTasks,
  onTaskUpdate,
  onTaskDelete,
  onTaskCreate
}: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>(initialTasks);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'completed' | 'pending'>('all');
  const [sortBy, setSortBy] = useState<'priority' | 'date' | 'title'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  useEffect(() => {
    setTasks(initialTasks);
  }, [initialTasks]);

  // Filter tasks based on the selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'completed') return task.completed;
    if (filter === 'pending') return !task.completed;
    return true; // 'all'
  });

  // Sort tasks based on the selected sort criteria
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    let comparison = 0;

    switch (sortBy) {
      case 'priority':
        // Define priority order: high > medium > low
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        comparison = priorityOrder[b.priority as 'high' | 'medium' | 'low'] -
                    priorityOrder[a.priority as 'high' | 'medium' | 'low'];
        break;
      case 'title':
        comparison = a.title.localeCompare(b.title);
        break;
      case 'date':
      default:
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
        break;
    }

    return sortOrder === 'asc' ? comparison : -comparison;
  });

  const handleTaskToggle = async (task: Task) => {
    setLoading(true);
    setError(null);
    try {
      const updatedTask = { ...task, completed: !task.completed };
      const result = await onTaskUpdate(updatedTask);
      if (result) {
        setTasks(tasks.map(t => t.id === task.id ? result : t));
      } else {
        setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
      }
    } catch (err) {
      setError('Failed to update task');
      // Revert the UI change if API fails
      setTasks(tasks);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskEdit = async (updatedTask: Task) => {
    setLoading(true);
    setError(null);
    try {
      const result = await onTaskUpdate(updatedTask);
      if (result) {
        setTasks(tasks.map(t => t.id === updatedTask.id ? result : t));
      } else {
        setTasks(tasks.map(t => t.id === updatedTask.id ? updatedTask : t));
      }
    } catch (err) {
      setError('Failed to update task');
      // Revert the UI change if API fails
      setTasks(tasks);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskAdd = async (newTask: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>) => {
    setLoading(true);
    setError(null);
    try {
      const createdTask = await onTaskCreate(newTask as Task);
      if (createdTask) {
        setTasks([...tasks, createdTask]);
        setShowForm(false);
      }
    } catch (err) {
      setError('Failed to create task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full bg-gray-100 p-4 rounded-xl border border-gray-300">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center mb-6 space-y-4 sm:space-y-0">
        <h2 className="text-2xl font-semibold text-gray-800">Your Tasks</h2>
        <div className="flex flex-wrap gap-2">
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setShowForm(!showForm)}
            className="bg-[#6F00FF] text-white px-4 py-2 rounded-xl hover:bg-[#3B0270] focus:outline-none focus:ring-2 focus:ring-[#6F00FF] focus:ring-offset-2 transition-colors duration-200"
            disabled={loading}
          >
            {showForm ? 'Cancel' : 'Add Task'}
          </motion.button>
          <div className="flex space-x-1">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setFilter('all')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                filter === 'all'
                  ? 'bg-[#6F00FF] text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-[#E9B3FB]'
              }`}
            >
              All
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setFilter('pending')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                filter === 'pending'
                  ? 'bg-[#6F00FF] text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-[#E9B3FB]'
              }`}
            >
              Pending
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setFilter('completed')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200 ${
                filter === 'completed'
                  ? 'bg-[#6F00FF] text-white'
                  : 'bg-gray-200 text-gray-800 hover:bg-[#E9B3FB]'
              }`}
            >
              Completed
            </motion.button>
          </div>
          <div className="flex space-x-1">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as 'priority' | 'date' | 'title')}
              className="px-3 py-2 rounded-lg text-sm font-medium bg-white text-gray-800 border border-gray-300"
            >
              <option value="date">Date</option>
              <option value="priority">Priority</option>
              <option value="title">Title</option>
            </select>
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="px-3 py-2 rounded-lg text-sm font-medium bg-gray-200 text-gray-800 hover:bg-[#E9B3FB] transition-colors duration-200"
            >
              {sortOrder === 'asc' ? '↑' : '↓'}
            </motion.button>
          </div>
        </div>
      </div>

      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-4 p-3 bg-red-500 text-white rounded-lg"
        >
          {error}
        </motion.div>
      )}

      {loading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mb-4 p-3 bg-gray-300 text-gray-800 rounded-lg"
        >
          Loading...
        </motion.div>
      )}

      {showForm && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="mb-6 p-4 bg-gray-50 rounded-xl border border-gray-300 shadow-sm"
        >
          <TaskForm
            onSubmit={handleTaskAdd}
            onCancel={() => setShowForm(false)}
          />
        </motion.div>
      )}

      <div className="bg-white rounded-xl border border-gray-300 overflow-hidden shadow-sm">
        <AnimatePresence>
          {sortedTasks.length === 0 ? (
            <motion.li
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="px-6 py-12 text-center text-gray-500"
            >
              <div className="animate-pulse">
                {filter === 'completed'
                  ? 'No completed tasks yet.'
                  : filter === 'pending'
                  ? 'No pending tasks yet.'
                  : 'No tasks yet. Add a new task to get started!'}
              </div>
            </motion.li>
          ) : (
            <ul className="divide-y divide-gray-200">
              <AnimatePresence>
                {sortedTasks
                  .filter(task => {
                    // Safe check for task existence and id
                    return task && typeof task === 'object' && 'id' in task && task.id;
                  })
                  .map((task) => (
                    <motion.div
                      key={task.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, height: 0 }}
                      transition={{ duration: 0.15 }}
                    >
                      <TaskItem
                        task={task}
                        onToggle={handleTaskToggle}
                        onEdit={handleTaskEdit}
                        onDelete={onTaskDelete}
                      />
                    </motion.div>
                  ))}
              </AnimatePresence>
            </ul>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}