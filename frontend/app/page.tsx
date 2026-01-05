'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function HomePage() {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // This would come from your auth context

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <header className="mb-12 text-center">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">Todo App - Phase II</h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Full-Stack Web Application with User Authentication and Task Management
          </p>
        </header>

        <main className="max-w-4xl mx-auto">
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">Welcome to the Todo App</h2>

            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-blue-50 p-6 rounded-lg">
                <h3 className="text-xl font-medium text-blue-800 mb-3">Features</h3>
                <ul className="space-y-2 text-gray-700">
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>User Authentication (Register/Login)</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>Create, Read, Update, Delete Tasks</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>Task Prioritization</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>Due Dates & Reminders</span>
                  </li>
                  <li className="flex items-start">
                    <span className="text-green-500 mr-2">✓</span>
                    <span>Responsive Design</span>
                  </li>
                </ul>
              </div>

              <div className="bg-indigo-50 p-6 rounded-lg">
                <h3 className="text-xl font-medium text-indigo-800 mb-3">Get Started</h3>
                <div className="space-y-4">
                  {isLoggedIn ? (
                    <div>
                      <p className="text-gray-700 mb-4">You are logged in. Go to your dashboard to manage tasks.</p>
                      <Link
                        href="/dashboard"
                        className="inline-block bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors"
                      >
                        Go to Dashboard
                      </Link>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      <Link
                        href="/login"
                        className="block bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition-colors text-center"
                      >
                        Login to Your Account
                      </Link>
                      <p className="text-center text-gray-600">or</p>
                      <Link
                        href="/register"
                        className="block bg-white text-indigo-600 border border-indigo-600 px-6 py-3 rounded-lg hover:bg-indigo-50 transition-colors text-center"
                      >
                        Create New Account
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-8">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">About This Project</h2>
            <p className="text-gray-700 mb-4">
              This Todo App is part of Hackathon II: "The Evolution of Todo – Mastering Spec-Driven Development & Cloud Native AI".
            </p>
            <p className="text-gray-700">
              Phase II focuses on building a full-stack web application with modern technologies,
              demonstrating spec-driven development principles using Claude Code and Spec-Kit Plus.
            </p>
          </div>
        </main>

        <footer className="mt-12 text-center text-gray-600">
          <p>© {new Date().getFullYear()} Todo App - Phase II. Built with Next.js, FastAPI, and SQLModel.</p>
        </footer>
      </div>
    </div>
  );
}