'use client';

import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-black shadow-sm">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link href="/" className="text-xl font-bold text-white">
            Todo App
          </Link>
          <nav>
            <ul className="flex space-x-6">
              <li>
                <Link href="/" className="text-white hover:text-gray-300 transition-colors duration-200">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/auth/login" className="text-white hover:text-gray-300 transition-colors duration-200">
                  Login
                </Link>
              </li>
              <li>
                <Link href="/auth/register" className="text-white hover:text-gray-300 transition-colors duration-200">
                  Register
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </header>
  );
}