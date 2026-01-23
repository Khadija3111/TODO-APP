/**
 * API Utilities for Chatbot Integration
 * Handles communication with the backend chat API
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

class ApiClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  /**
   * Send a message to the chat endpoint
   */
  async sendChatMessage(userId, message, conversationId = null) {
    try {
      const response = await fetch(`${this.baseURL}/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication headers if needed
          // 'Authorization': `Bearer ${authToken}`,
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          message: message
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending chat message:', error);
      throw error;
    }
  }

  /**
   * Get user's conversations
   */
  async getUserConversations(userId) {
    try {
      const response = await fetch(`${this.baseURL}/${userId}/conversations`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication headers if needed
          // 'Authorization': `Bearer ${authToken}`,
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching user conversations:', error);
      throw error;
    }
  }

  /**
   * Get messages for a specific conversation
   */
  async getConversationMessages(userId, conversationId) {
    try {
      const response = await fetch(`${this.baseURL}/${userId}/conversations/${conversationId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // Add authentication headers if needed
          // 'Authorization': `Bearer ${authToken}`,
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching conversation messages:', error);
      throw error;
    }
  }
}

// Create a singleton instance
const apiClient = new ApiClient();

export default apiClient;

// Export individual functions for convenience
export const sendChatMessage = apiClient.sendChatMessage.bind(apiClient);
export const getUserConversations = apiClient.getUserConversations.bind(apiClient);
export const getConversationMessages = apiClient.getConversationMessages.bind(apiClient);

