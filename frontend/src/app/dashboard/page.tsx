'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { taskAPI, Task } from '../../lib/api';


import TaskList from '@/components/TaskList';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function DashboardPage() {
  const { user, loading, isAuthenticated } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [initialLoading, setInitialLoading] = useState(true);
  const router = useRouter();

  // Redirect if not authenticated
  useEffect(() => {
    if (!loading && !isAuthenticated()) {
      router.push('/auth/login');
    }
  }, [loading, isAuthenticated, router]);

  // Load tasks when component mounts
  useEffect(() => {
    const loadTasks = async () => {
      if (isAuthenticated()) {
        try {
          const tasksData = await taskAPI.getAllTasks();
          setTasks(tasksData);
        } catch (error) {
          console.error('Failed to load tasks:', error);
        } finally {
          setInitialLoading(false);
        }
      }
    };

    loadTasks();
  }, [isAuthenticated]);

  const handleTaskUpdate = async (task: Task) => {
    try {
      const updatedTask = await taskAPI.updateTask(task.id, task);
      setTasks(tasks.map(t => t.id === task.id ? updatedTask : t));
      return updatedTask;
    } catch (error) {
      console.error('Failed to update task:', error);
      throw error;
    }
  };

  const handleTaskDelete = async (id: string) => {
    try {
      await taskAPI.deleteTask(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error('Failed to delete task:', error);
      throw error;
    }
  };

  const handleTaskCreate = async (task: Partial<Task>) => {
    try {
      // Ensure required fields are present
      if (!task.title) {
        throw new Error('Title is required');
      }

      const newTask = await taskAPI.createTask({
        title: task.title,
        description: task.description,
        priority: task.priority,
        category: task.category,
        completed: task.completed || false,
      });
      setTasks([...tasks, newTask]);
      return newTask;
    } catch (error) {
      console.error('Failed to create task:', error);
      throw error;
    }
  };

  if (loading || initialLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <p>Loading dashboard...</p>
      </div>
    );
  }

  if (!isAuthenticated()) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="mb-8">
        <motion.h1
          className="text-3xl font-semibold text-gray-100"
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        >
          Welcome back, {user?.email?.split('@')[0]}!
        </motion.h1>
        <motion.p
          className="mt-2 text-gray-200"
          initial={{ x: -100, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5, ease: "easeOut", delay: 0.1 }}
        >
          Manage your tasks efficiently.
        </motion.p>
      </div>

      <motion.div
        className="bg-vanilla-custard rounded-xl shadow-premium p-6 transition-all duration-300"
        initial={{ y: 100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: "easeOut", delay: 0.2 }}
      >
        <TaskList
          initialTasks={tasks}
          onTaskUpdate={handleTaskUpdate}
          onTaskDelete={handleTaskDelete}
          onTaskCreate={handleTaskCreate}
        />
      </motion.div>
    </div>
  );
}