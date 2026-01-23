/**
 * Chat Panel Component
 * Implements the ChatKit panel for AI chatbot interaction
 */

import React, { useState, useEffect } from 'react';
import { sendChatMessage } from '../utils/api';
import './ChatPanel.css';

const ChatPanel = ({ userId, isOpen, onClose, onToggleVisibility, onTaskUpdate }) => {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentConversationId, setCurrentConversationId] = useState(null);

  const sendMessageToBackend = async (message, conversationId = null) => {
    try {
      // Call the actual backend API
      const response = await sendChatMessage(userId, message, conversationId);
      return response;
    } catch (error) {
      console.error('Error sending message to backend:', error);
      return {
        conversation_id: conversationId,
        response: "Sorry, I encountered an error processing your request. Please try again.",
        tool_calls: [],
        error: error.message
      };
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: inputValue,
      timestamp: new Date().toISOString()
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    const tempInputValue = inputValue;
    setInputValue('');

    setIsLoading(true);

    try {
      // Send message to backend
      const response = await sendMessageToBackend(tempInputValue, currentConversationId);

      // Update conversation ID if it's the first message
      if (!currentConversationId && response.conversation_id) {
        setCurrentConversationId(response.conversation_id);
      }

      // Add assistant response to the chat
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls || [],  // Include tool calls in the message
        tool_results: response.tool_results || [],  // Include tool results in the message
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, assistantMessage]);

      // Check if any task-related tools were executed and trigger refresh
      if (response.tool_calls && response.tool_calls.length > 0) {
        const hasTaskOperations = response.tool_calls.some(call =>
          call.name &&
          (call.name.includes('task') ||
           ['add_task', 'delete_task', 'complete_task', 'update_task'].includes(call.name))
        );

        if (hasTaskOperations) {
          // Small delay to ensure the backend operations are complete
          setTimeout(() => {
            // Dispatch a custom event to notify other parts of the app
            window.dispatchEvent(new CustomEvent('taskUpdate'));
          }, 500);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to the chat
      const errorMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const formatMessageContent = (content, tool_calls = [], tool_results = []) => {
    // Split content by lines
    const lines = content.split('\n');
    const elements = [];

    // Add content lines, with special formatting for task lists
    lines.forEach((line, i) => {
      // Check if line looks like a task (e.g., starts with a number followed by a dot)
      const taskRegex = /^\d+\.\s*(.*?)\((pending|completed)\)$/;
      const taskMatch = line.match(taskRegex);

      if (taskMatch) {
        // This is a task line - format it specially
        const taskDescription = taskMatch[1].trim();
        const taskStatus = taskMatch[2];

        elements.push(
          <div key={`task-${i}`} className={`task-item ${taskStatus}`}>
            <span className="task-number">#{i + 1}</span>
            <span className="task-description">{taskDescription}</span>
            <span className={`task-status ${taskStatus}`}>{taskStatus}</span>
          </div>
        );
      } else {
        // Regular line - add as before
        elements.push(
          <React.Fragment key={`content-${i}`}>
            {line}
            <br />
          </React.Fragment>
        );
      }
    });

    // Add tool calls visualization if present
    if (tool_calls && tool_calls.length > 0) {
      elements.push(
        <div key="tool-calls" className="tool-calls-info">
          <details className="tool-calls-details">
            <summary>🔧 Tool Calls Executed</summary>
            <ul className="tool-calls-list">
              {tool_calls.map((call, idx) => (
                <li key={`tool-call-${idx}`} className="tool-call-item">
                  <strong>{call.name || call.function?.name || 'Unknown'}</strong>:
                  {JSON.stringify(call.arguments || call.function?.arguments || call.parameters || {})}
                </li>
              ))}
            </ul>
          </details>
        </div>
      );
    }

    // Add tool results visualization if present
    if (tool_results && tool_results.length > 0) {
      elements.push(
        <div key="tool-results" className="tool-results-info">
          <details className="tool-results-details">
            <summary>✅ Tool Results</summary>
            <ul className="tool-results-list">
              {tool_results.map((result, idx) => (
                <li key={`tool-result-${idx}`} className="tool-result-item">
                  {typeof result === 'string' ? result : JSON.stringify(result)}
                </li>
              ))}
            </ul>
          </details>
        </div>
      );
    }

    return elements;
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="chat-panel-overlay">
      <div className="chat-panel">
        <div className="chat-panel-header">
          <h3>AI Task Assistant</h3>
          <button
            className="close-button"
            onClick={onClose}
            aria-label="Close chat panel"
          >
            ×
          </button>
        </div>

        <div className="chat-messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <p>Hello! I'm your AI task assistant.</p>
              <p>You can ask me to:</p>
              <ul>
                <li>Add tasks (e.g., "Add a task to buy groceries")</li>
                <li>List tasks (e.g., "Show me my tasks")</li>
                <li>Complete tasks (e.g., "Mark task 1 as complete")</li>
                <li>Delete tasks (e.g., "Delete the meeting task")</li>
                <li>Update tasks (e.g., "Change task 1 to 'Call mom tonight'")</li>
              </ul>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`message ${message.role}`}
              >
                <div className="message-content">
                  {formatMessageContent(message.content, message.tool_calls, message.tool_results)}
                </div>
                <div className="message-timestamp">
                  {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="chat-input-area">
          <textarea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message here..."
            rows="1"
            className="chat-input"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            className="send-button"
            disabled={!inputValue.trim() || isLoading}
            aria-label="Send message"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;