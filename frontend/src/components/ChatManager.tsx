'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import ChatPanel from '../../components/ChatPanel';
import ChatbotIcon from '../../components/ChatbotIcon';

export default function ChatManager() {
  const { user } = useAuth();
  const [isChatPanelOpen, setIsChatPanelOpen] = useState(false);

  // Close chat panel when user logs out
  useEffect(() => {
    if (!user) {
      setIsChatPanelOpen(false);
    }
  }, [user]);

  const toggleChatPanel = () => {
    setIsChatPanelOpen(!isChatPanelOpen);
  };

  const closeChatPanel = () => {
    setIsChatPanelOpen(false);
  };

  // Only show chat functionality if user is logged in
  if (!user) {
    return null;
  }

  return (
    <>
      {isChatPanelOpen && (
        <ChatPanel
          userId={user.id}
          isOpen={isChatPanelOpen}
          onClose={closeChatPanel}
          onToggleVisibility={toggleChatPanel}
        />
      )}
      {!isChatPanelOpen && (
        <ChatbotIcon onClick={toggleChatPanel} />
      )}
    </>
  );
}