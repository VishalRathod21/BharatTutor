from datetime import datetime
from typing import List, Dict, Any, Optional

class ConversationMemory:
    def __init__(self, max_conversations: int = 50):
        """Initialize conversation memory with maximum conversation limit."""
        self.conversations = []
        self.max_conversations = max_conversations
    
    def add_conversation(self, question: str, answer: str, subject: Optional[str] = None, 
                        class_level: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None):
        """Add a new conversation to memory."""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "answer": answer,
            "subject": subject,
            "class": class_level,
            "metadata": metadata or {}
        }
        
        self.conversations.append(conversation)
        
        # Keep only the most recent conversations
        if len(self.conversations) > self.max_conversations:
            self.conversations = self.conversations[-self.max_conversations:]
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get conversation history, optionally limited to recent conversations."""
        if limit:
            return self.conversations[-limit:]
        return self.conversations.copy()
    
    def get_context_for_question(self, current_question: str, max_context: int = 3) -> str:
        """Get relevant context from recent conversations for the current question."""
        if not self.conversations:
            return ""
        
        # Get recent conversations for context
        recent_conversations = self.conversations[-max_context:]
        
        context_parts = []
        for conv in recent_conversations:
            # Check if previous conversation is relevant to current question
            if self._is_related(conv["question"], current_question):
                context_parts.append(f"Previous Q: {conv['question']}\nPrevious A: {conv['answer']}")
        
        return "\n\n".join(context_parts) if context_parts else ""
    
    def _is_related(self, prev_question: str, current_question: str) -> bool:
        """Simple relatedness check based on common words."""
        prev_words = set(prev_question.lower().split())
        current_words = set(current_question.lower().split())
        
        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "is", "are", "was", "were", "what", "how", "why", "when", "where"}
        prev_words -= stop_words
        current_words -= stop_words
        
        # Check if there's significant overlap
        intersection = prev_words.intersection(current_words)
        return len(intersection) >= 2 or (len(intersection) >= 1 and len(current_words) <= 3)
    
    def clear(self):
        """Clear all conversation history."""
        self.conversations = []
    
    def get_subject_history(self, subject: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a specific subject."""
        subject_conversations = [
            conv for conv in self.conversations 
            if conv.get("subject", "").lower() == subject.lower()
        ]
        return subject_conversations[-limit:] if limit else subject_conversations
    
    def get_class_history(self, class_level: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for a specific class level."""
        class_conversations = [
            conv for conv in self.conversations 
            if conv.get("class", "") == class_level
        ]
        return class_conversations[-limit:] if limit else class_conversations
    
    def search_conversations(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search through conversation history for specific terms."""
        query_lower = query.lower()
        matching_conversations = []
        
        for conv in self.conversations:
            if (query_lower in conv["question"].lower() or 
                query_lower in conv["answer"].lower()):
                matching_conversations.append(conv)
        
        return matching_conversations[-limit:] if limit else matching_conversations
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get usage statistics from conversation history."""
        if not self.conversations:
            return {"total_conversations": 0}
        
        subjects = {}
        classes = {}
        
        for conv in self.conversations:
            subject = conv.get("subject", "Unknown")
            class_level = conv.get("class", "Unknown")
            
            subjects[subject] = subjects.get(subject, 0) + 1
            classes[class_level] = classes.get(class_level, 0) + 1
        
        return {
            "total_conversations": len(self.conversations),
            "subjects_used": subjects,
            "classes_used": classes,
            "most_active_subject": max(subjects.items(), key=lambda x: x[1])[0] if subjects else "None",
            "most_active_class": max(classes.items(), key=lambda x: x[1])[0] if classes else "None"
        }
