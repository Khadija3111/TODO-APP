import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Task } from '@/lib/api';
import TaskForm from './TaskForm';

interface TaskItemProps {
  task: Task;
  onToggle: (task: Task) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

export default function TaskItem({ task, onToggle, onEdit, onDelete }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = (updatedTaskData: Partial<Task>) => {
    const updatedTask = { ...task, ...updatedTaskData };
    onEdit(updatedTask);
    setIsEditing(false);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id);
    }
  };

  if (isEditing) {
    return (
      <motion.li
        layout
        initial={{ opacity: 1, height: 'auto' }}
        exit={{ opacity: 0, height: 0 }}
        className="px-4 py-4 sm:px-6 bg-vanilla-custard/50 rounded-lg"
      >
        <TaskForm
          initialData={task}
          onSubmit={handleEdit}
          onCancel={() => setIsEditing(false)}
        />
      </motion.li>
    );
  }

  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, height: 0, scale: 0.98 }}
      whileHover={{ scale: 1.01 }}
      className="px-4 py-4 sm:px-6 transition-all duration-200"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <motion.input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task)}
            whileTap={{ scale: 0.95 }}
            className={`h-5 w-5 rounded border-2 mr-3 ${
              task.completed
                ? 'bg-honey-bronze border-honey-bronze'
                : 'bg-vanilla-custard border-dark-slate'
            }`}
            style={{
              accentColor: task.completed ? '#e09f3e' : undefined
            }}
          />
          <div className="ml-2">
            <motion.p
              animate={{
                color: task.completed ? '#540b0e' : '#335c67',
                textDecoration: task.completed ? 'line-through' : 'none'
              }}
              transition={{ duration: 0.2 }}
              className="text-sm font-medium"
            >
              {task.title}
            </motion.p>
            {task.description && (
              <p className={`text-sm ${task.completed ? 'text-dark-slate/60' : 'text-dark-slate/80'}`}>
                {task.description}
              </p>
            )}
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {task.priority && (
            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              task.priority === 'high'
                ? 'bg-brown-red text-vanilla-custard'
                : task.priority === 'medium'
                ? 'bg-yellow-500 text-dark-slate'
                : 'bg-[#a3c9a8] text-dark-slate'
            }`}>
              {task.priority}
            </span>
          )}
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setIsEditing(true)}
            className="text-gray-600 hover:text-gray-800 font-medium transition-colors duration-200"
          >
            Edit
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleDelete}
            className="w-6 h-6 rounded-full bg-[#9e2a2b] text-white flex items-center justify-center hover:bg-[#8a2325] transition-colors duration-200 text-sm"
          >
            ×
          </motion.button>
        </div>
      </div>
    </motion.li>
  );
}