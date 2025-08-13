'use client';

import { useEffect, useState } from 'react';
import { ToDo } from '../types/ToDo';

const TodoListing = () => {
  const [todos, setTodos] = useState<ToDo[]>([]);
  
  useEffect(() => {
    // Simulating loading data from a JSON file
    const sampleTodos: ToDo[] = [
      { task: "Complete project documentation", completed: false },
      { task: "Review code changes", completed: true },
      { task: "Update dependencies", completed: false },
      { task: "Write unit tests", completed: true },
      { task: "Deploy to staging", completed: false }
    ];
    setTodos(sampleTodos);
  }, []);

  

  const Check = 'X';

  const toggleTodo = (task: string) => {
    setTodos(todos.map(todo => 
      todo.task === task ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  return (
    <div className="max-w-md mx-auto mt-8 p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Todo List</h2>
      
      <div className="space-y-3">
        {todos.map(todo => (
          <div 
            key={todo.task}
            className={`flex items-center p-3 rounded-lg border transition-colors ${
              todo.completed 
                ? 'bg-green-50 border-green-200' 
                : 'bg-gray-50 border-gray-200'
            }`}
          >
            <button
              onClick={() => toggleTodo(todo.task)}
              className={`flex items-center justify-center w-6 h-6 rounded-full border-2 mr-3 transition-colors ${
                todo.completed
                  ? 'bg-green-500 border-green-500 text-white'
                  : 'border-gray-300 hover:border-green-500'
              }`}
            >
              {todo.completed && Check}
            </button>
            
            <span 
              className={`flex-1 ${
                todo.completed 
                  ? 'text-gray-500 line-through' 
                  : 'text-gray-800'
              }`}
            >
              {todo.task}
            </span>
            
            <div className={`w-3 h-3 rounded-full ${
              todo.completed ? 'bg-green-500' : 'bg-yellow-500'
            }`} />
          </div>
        ))}
      </div>
      
      {todos.length === 0 && (
        <p className="text-gray-500 text-center py-8">No todos found</p>
      )}
      
      <div className="mt-6 text-sm text-gray-600">
        <p>Total: {todos.length} | Completed: {todos.filter(t => t.completed).length}</p>
      </div>
    </div>
  );
};

export default TodoListing;