// API Client for Todo App
// Connects to the backend API with JWT authentication

// Types
export interface User {
  id: string;
  email: string;
  created_at: string;
}

export interface Task {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority?: 'low' | 'medium' | 'high';
  category?: string;
  created_at: string;
  updated_at: string;
}

// Base API configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' && window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000'
    : 'https://khadija222-to-do-app-chatbot-phase.hf.space/');

// Helper function to get auth headers
function getAuthHeaders(): { [key: string]: string } {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

// Authentication functions
export const authAPI = {
  async register(email: string, password: string): Promise<{ user: User; access_token: string } | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Invalid response from server' }));
        throw new Error(errorData.detail || `Registration failed (${response.status})`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Registration error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
      }
      throw error;
    }
  },

  async login(email: string, password: string): Promise<{ user: User; access_token: string } | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Invalid response from server' }));
        throw new Error(errorData.detail || `Login failed (${response.status})`);
      }

      const data = await response.json();

      // Store the token in localStorage
      if (data.access_token) {
        localStorage.setItem('token', data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Login error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
      }
      throw error;
    }
  },

  async logout(): Promise<void> {
    // Remove the token from localStorage
    localStorage.removeItem('token');
  },

  async getProfile(): Promise<User | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/me`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Invalid response from server' }));
        throw new Error(errorData.detail || `Failed to fetch user profile (${response.status})`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Profile fetch error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
      }
      throw error;
    }
  }
};

// Task functions
export const taskAPI = {
  async getAllTasks(completed?: boolean): Promise<Task[]> {
    try {
      let url = `${API_BASE_URL}/api/tasks`;
      if (completed !== undefined) {
        url += `?completed=${completed}`;
      }

      const response = await fetch(url, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Invalid response from server' }));
        throw new Error(errorData.detail || `Failed to fetch tasks (${response.status})`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Get tasks error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
      }
      throw error;
    }
  },

  async createTask(taskData: Omit<Task, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks`, {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Invalid response from server' }));
        throw new Error(errorData.detail || `Failed to create task (${response.status})`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Create task error:', error);
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to connect to the server. Please check your internet connection and try again.');
      }
      throw error;
    }
  },

  async updateTask(id: string, taskData: Partial<Task>): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'PUT',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to update task');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Update task error:', error);
      throw error;
    }
  },

  async deleteTask(id: string): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete task');
      }
    } catch (error) {
      console.error('Delete task error:', error);
      throw error;
    }
  },

  async toggleTaskCompletion(id: string): Promise<Task> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/tasks/${id}/complete`, {
        method: 'PUT',
        headers: getAuthHeaders(),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to toggle task completion');
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Toggle task completion error:', error);
      throw error;
    }
  }
};