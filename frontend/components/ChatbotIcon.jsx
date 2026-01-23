/**
 * Chatbot Icon Component
 * Provides an icon to open the AI chatbot panel
 */

import React, { useState } from 'react';
import './ChatbotIcon.css';

const ChatbotIcon = ({ onClick }) => {
  const [isVisible, setIsVisible] = useState(true);

  const handleClick = () => {
    onClick();
    // Hide the icon when chat panel is opened
    setIsVisible(false);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="chatbot-icon-container">
      <button
        className="chatbot-icon-button"
        onClick={handleClick}
        aria-label="Open AI Chatbot"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
          className="chatbot-icon-svg"
        >
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </button>
    </div>
  );
};

export default ChatbotIcon;