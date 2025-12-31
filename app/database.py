"""In-memory database for simplicity"""
from typing import Dict, List, Optional
from datetime import datetime
from app.models import User, Task, UserRole, TaskStatus

class Database:
    """Simple in-memory database"""
    
    def __init__(self):
        self.users: Dict[int, Dict] = {}
        self.tasks: Dict[int, Dict] = {}
        self.user_id_counter = 1
        self.task_id_counter = 1
        self.username_index: Dict[str, int] = {}
        self.email_index: Dict[str, int] = {}
    
    # User operations
    def create_user(self, email: str, username: str, hashed_password: str, role: UserRole = UserRole.USER) -> Dict:
        """Create a new user"""
        user_id = self.user_id_counter
        self.user_id_counter += 1
        
        user = {
            "id": user_id,
            "email": email,
            "username": username,
            "hashed_password": hashed_password,
            "role": role,
            "created_at": datetime.utcnow()
        }
        
        self.users[user_id] = user
        self.username_index[username] = user_id
        self.email_index[email] = user_id
        
        return user
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        user_id = self.username_index.get(username)
        return self.users.get(user_id) if user_id else None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def username_exists(self, username: str) -> bool:
        """Check if username exists"""
        return username in self.username_index
    
    def email_exists(self, email: str) -> bool:
        """Check if email exists"""
        return email in self.email_index
    
    # Task operations
    def create_task(self, user_id: int, title: str, description: Optional[str], status: TaskStatus) -> Dict:
        """Create a new task"""
        task_id = self.task_id_counter
        self.task_id_counter += 1
        
        now = datetime.utcnow()
        task = {
            "id": task_id,
            "user_id": user_id,
            "title": title,
            "description": description,
            "status": status,
            "created_at": now,
            "updated_at": now
        }
        
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get task by ID"""
        return self.tasks.get(task_id)
    
    def get_user_tasks(self, user_id: int, skip: int = 0, limit: int = 100, 
                       status: Optional[TaskStatus] = None, sort_by: str = "created_at") -> List[Dict]:
        """Get tasks for a user with filtering and pagination"""
        user_tasks = [t for t in self.tasks.values() if t["user_id"] == user_id]
        
        # Filter by status
        if status:
            user_tasks = [t for t in user_tasks if t["status"] == status]
        
        # Sort
        reverse = True
        if sort_by.startswith("-"):
            sort_by = sort_by[1:]
            reverse = False
        
        user_tasks.sort(key=lambda x: x.get(sort_by, ""), reverse=reverse)
        
        # Paginate
        return user_tasks[skip:skip + limit]
    
    def count_user_tasks(self, user_id: int, status: Optional[TaskStatus] = None) -> int:
        """Count user tasks"""
        user_tasks = [t for t in self.tasks.values() if t["user_id"] == user_id]
        if status:
            user_tasks = [t for t in user_tasks if t["status"] == status]
        return len(user_tasks)
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Dict]:
        """Update a task"""
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        for key, value in kwargs.items():
            if value is not None:
                task[key] = value
        
        task["updated_at"] = datetime.utcnow()
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks (admin only)"""
        return list(self.tasks.values())

# Global database instance
db = Database()

# Create default admin user
db.create_user(
    email="admin@example.com",
    username="admin",
    hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYG6CJxb4M2",  # "Admin123"
    role=UserRole.ADMIN
)
