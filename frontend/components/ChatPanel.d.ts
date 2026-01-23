// Type definition for ChatPanel component
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

export interface ChatPanelProps {
  userId: string;
  isOpen: boolean;
  onClose: () => void;
  onToggleVisibility: () => void;
  onTaskUpdate?: (task: Task) => Promise<Task>;
}

declare const ChatPanel: React.ComponentType<ChatPanelProps>;
export default ChatPanel;