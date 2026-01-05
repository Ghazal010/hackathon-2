'use client';

import { useState, useEffect } from 'react';
import { taskAPI } from '@/lib/api';
import { Task, TaskCreate } from '@/lib/types';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [newTask, setNewTask] = useState<TaskCreate>({ title: '', description: '', priority: 'medium' });
  const [error, setError] = useState<string | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  // Fetch tasks on component mount
  useEffect(() => {
    fetchTasks();
  }, []);

  // Fetch tasks from API
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await taskAPI.getAll();
      setTasks(response.data);
    } catch (err) {
      setError('Failed to load tasks');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  };

  // Handle form input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setNewTask(prev => ({ ...prev, [name]: value }));
  };

  // Create a new task
  const handleCreateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await taskAPI.create(newTask);
      setTasks(prev => [response.data, ...prev]);
      setNewTask({ title: '', description: '', priority: 'medium' });
    } catch (err) {
      setError('Failed to create task');
      console.error('Error creating task:', err);
    }
  };

  // Toggle task completion
  const toggleTaskCompletion = async (id: number) => {
    try {
      const task = tasks.find(t => t.id === id);
      if (!task) return;

      const response = await taskAPI.toggleComplete(id);
      setTasks(prev =>
        prev.map(t =>
          t.id === id ? { ...t, completed: response.data.completed } : t
        )
      );
    } catch (err) {
      setError('Failed to update task');
      console.error('Error updating task:', err);
    }
  };

  // Delete a task
  const deleteTask = async (id: number) => {
    if (!confirm('Are you sure you want to delete this task?')) return;

    try {
      await taskAPI.delete(id);
      setTasks(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      setError('Failed to delete task');
      console.error('Error deleting task:', err);
    }
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all'
  });

  // Format date for display
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="container mx-auto max-w-6xl">
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-gray-800">My Tasks</h1>
          <p className="text-gray-600">Manage your todo items efficiently</p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Task Creation */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Create New Task</h2>

              {error && (
                <div className="bg-red-50 text-red-700 p-3 rounded-lg mb-4">
                  {error}
                </div>
              )}

              <form onSubmit={handleCreateTask} className="space-y-4">
                <div>
                  <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
                    Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={newTask.title}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="What needs to be done?"
                  />
                </div>

                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
                    Description
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    value={newTask.description}
                    onChange={handleInputChange}
                    rows={3}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="Add details..."
                  />
                </div>

                <div>
                  <label htmlFor="priority" className="block text-sm font-medium text-gray-700 mb-1">
                    Priority
                  </label>
                  <select
                    id="priority"
                    name="priority"
                    value={newTask.priority}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>

                <button
                  type="submit"
                  className="w-full bg-indigo-600 text-white py-3 px-4 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Add Task
                </button>
              </form>
            </div>
          </div>

          {/* Right Column - Task List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>

                <div className="flex space-x-2">
                  <button
                    onClick={() => setFilter('all')}
                    className={`px-4 py-2 rounded-lg text-sm ${
                      filter === 'all'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    All
                  </button>
                  <button
                    onClick={() => setFilter('active')}
                    className={`px-4 py-2 rounded-lg text-sm ${
                      filter === 'active'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Active
                  </button>
                  <button
                    onClick={() => setFilter('completed')}
                    className={`px-4 py-2 rounded-lg text-sm ${
                      filter === 'completed'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }`}
                  >
                    Completed
                  </button>
                </div>
              </div>

              {loading ? (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-600"></div>
                  <p className="mt-2 text-gray-600">Loading tasks...</p>
                </div>
              ) : filteredTasks.length === 0 ? (
                <div className="text-center py-8">
                  <p className="text-gray-600">No tasks found. Create your first task!</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredTasks.map(task => (
                    <div
                      key={task.id}
                      className={`p-4 rounded-lg border ${
                        task.completed
                          ? 'bg-green-50 border-green-200'
                          : 'bg-white border-gray-200'
                      }`}
                    >
                      <div className="flex items-start">
                        <input
                          type="checkbox"
                          checked={task.completed}
                          onChange={() => toggleTaskCompletion(task.id)}
                          className="mt-1 h-5 w-5 text-indigo-600 rounded focus:ring-indigo-500"
                        />
                        <div className="ml-4 flex-1">
                          <div className="flex justify-between">
                            <h3 className={`font-medium ${
                              task.completed ? 'text-gray-500 line-through' : 'text-gray-800'
                            }`}>
                              {task.title}
                            </h3>
                            <span className={`text-xs px-2 py-1 rounded-full ${
                              task.priority === 'high'
                                ? 'bg-red-100 text-red-800'
                                : task.priority === 'medium'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-green-100 text-green-800'
                            }`}>
                              {task.priority}
                            </span>
                          </div>

                          {task.description && (
                            <p className="text-gray-600 mt-1 text-sm">{task.description}</p>
                          )}

                          <div className="flex justify-between items-center mt-2">
                            <span className="text-xs text-gray-500">
                              Created: {formatDate(task.created_at)}
                            </span>
                            {task.due_date && (
                              <span className="text-xs text-gray-500">
                                Due: {formatDate(task.due_date)}
                              </span>
                            )}
                          </div>
                        </div>

                        <button
                          onClick={() => deleteTask(task.id)}
                          className="ml-4 text-red-500 hover:text-red-700"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                          </svg>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}