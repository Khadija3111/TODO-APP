'use client';

import Link from 'next/link';
import { motion } from 'framer-motion';

export default function Home() {
  return (
    <div className="min-h-[80vh] flex items-center justify-center">
      <div className="max-w-md w-full space-y-6">
        <div>
          <motion.h2
            className="mt-2 text-center text-3xl font-bold text-gray-100"
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut" }}
          >
            Welcome to Todo App
          </motion.h2>
          <motion.p
            className="mt-2 text-center text-sm text-gray-200"
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut", delay: 0.1 }}
          >
            Sign in to manage your tasks
          </motion.p>
        </div>
        <div className="mt-6 space-y-3">
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut", delay: 0.2 }}
          >
            <Link
              href="/auth/login"
              className="w-full flex justify-center py-2.5 px-4 border border-transparent text-sm font-semibold rounded-lg text-white bg-gradient-to-r from-[#3B0270] to-[#6F00FF] hover:from-[#6F00FF] hover:to-[#3B0270] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#6F00FF] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Sign In
            </Link>
          </motion.div>
          <motion.div
            initial={{ x: -100, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5, ease: "easeOut", delay: 0.3 }}
          >
            <Link
              href="/auth/register"
              className="w-full flex justify-center py-2.5 px-4 border border-transparent text-sm font-semibold rounded-lg text-white bg-gradient-to-r from-[#3B0270] to-[#6F00FF] hover:from-[#6F00FF] hover:to-[#3B0270] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#6F00FF] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
            >
              Sign Up
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  );
}