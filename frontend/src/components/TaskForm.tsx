import { useState } from 'react';
import { Task } from '@/lib/api';

interface TaskFormProps {
  initialData?: Task;
  onSubmit: (taskData: Partial<Task>) => void;
  onCancel: () => void;
}

export default function TaskForm({ initialData, onSubmit, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [priority, setPriority] = useState(initialData?.priority || 'medium');
  const [category, setCategory] = useState(initialData?.category || '');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const taskData = {
      title,
      description: description || undefined,
      priority: priority as 'low' | 'medium' | 'high' || undefined,
      category: category || undefined,
    };

    onSubmit(taskData);

    // Reset form if it's a new task
    if (!initialData) {
      setTitle('');
      setDescription('');
      setPriority('medium');
      setCategory('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 p-4 rounded-xl bg-gray-100 border border-gray-300 shadow-sm">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-800">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
          className="mt-1 block w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm bg-white text-gray-800"
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-800">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="mt-1 block w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm bg-white text-gray-800"
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="priority" className="block text-sm font-medium text-gray-800">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value)}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm text-gray-800"
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div>
          <label htmlFor="category" className="block text-sm font-medium text-gray-800">
            Category
          </label>
          <input
            type="text"
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:border-gray-500 sm:text-sm bg-white text-gray-800"
          />
        </div>
      </div>

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-400 text-white px-4 py-2 rounded-lg hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-600 focus:ring-offset-2 transition-colors duration-200"
        >
          Cancel
        </button>
        <button
          type="submit"
          className="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-gray-900 focus:ring-offset-2 transition-colors duration-200"
        >
          {initialData ? 'Update Task' : 'Add Task'}
        </button>
      </div>
    </form>
  );
}