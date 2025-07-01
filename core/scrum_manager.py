from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class ScrumManager:
    """Core Scrum management functionality"""
    
    def __init__(self):
        self.story_statuses = ["Backlog", "To Do", "In Progress", "In Review", "Done"]
        self.priority_levels = ["Low", "Medium", "High", "Critical"]
    
    def create_user_story(self, title: str, description: str, acceptance_criteria: str, 
                         priority: str = "Medium", labels: List[str] = None) -> Dict:
        """Create a new user story"""
        return {
            "id": self._generate_id(),
            "title": title,
            "description": description,
            "acceptance_criteria": acceptance_criteria,
            "priority": priority,
            "labels": labels or [],
            "status": "Backlog",
            "story_points": None,
            "assignee": None,
            "created_date": datetime.now().isoformat(),
            "updated_date": datetime.now().isoformat(),
            "comments": [],
            "subtasks": [],
            "dependencies": []
        }
    
    def create_sprint(self, name: str, duration_weeks: int = 2, 
                     start_date: str = None, capacity: int = None) -> Dict:
        """Create a new sprint"""
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start = datetime.now()
        
        end = start + timedelta(weeks=duration_weeks)
        
        return {
            "id": self._generate_id(),
            "name": name,
            "start_date": start.strftime("%Y-%m-%d"),
            "end_date": end.strftime("%Y-%m-%d"),
            "duration_weeks": duration_weeks,
            "capacity": capacity or 40,  # Default capacity
            "status": "Planning",
            "stories": [],
            "goals": [],
            "created_date": datetime.now().isoformat(),
            "completed_points": 0,
            "total_points": 0
        }
    
    def add_story_to_sprint(self, sprint_id: str, story_id: str) -> bool:
        """Add a story to a sprint"""
        from core.data_store import DataStore
        data_store = DataStore()
        
        sprint = data_store.get_sprint(sprint_id)
        story = data_store.get_story(story_id)
        
        if sprint and story:
            if story_id not in sprint.get('stories', []):
                sprint['stories'].append(story_id)
                sprint['total_points'] += story.get('story_points', 0)
                data_store.update_sprint(sprint_id, sprint)
                return True
        return False
    
    def update_story_status(self, story_id: str, new_status: str) -> bool:
        """Update story status and handle sprint point tracking"""
        from core.data_store import DataStore
        data_store = DataStore()
        
        story = data_store.get_story(story_id)
        if not story:
            return False
        
        old_status = story.get('status')
        story['status'] = new_status
        story['updated_date'] = datetime.now().isoformat()
        
        # Update sprint points if story is in a sprint
        current_sprint = data_store.get_current_sprint()
        if current_sprint and story_id in current_sprint.get('stories', []):
            story_points = story.get('story_points', 0)
            
            # Remove points from old status
            if old_status == "Done":
                current_sprint['completed_points'] -= story_points
            
            # Add points to new status
            if new_status == "Done":
                current_sprint['completed_points'] += story_points
            
            data_store.update_sprint(current_sprint['id'], current_sprint)
        
        data_store.update_story(story_id, story)
        return True
    
    def calculate_velocity(self, sprint_ids: List[str]) -> Dict:
        """Calculate team velocity based on completed sprints"""
        from core.data_store import DataStore
        data_store = DataStore()
        
        velocities = []
        total_points = 0
        
        for sprint_id in sprint_ids:
            sprint = data_store.get_sprint(sprint_id)
            if sprint and sprint.get('status') == 'Completed':
                completed_points = sprint.get('completed_points', 0)
                velocities.append(completed_points)
                total_points += completed_points
        
        if not velocities:
            return {"average": 0, "trend": "No data", "sprints_analyzed": 0}
        
        average_velocity = total_points / len(velocities)
        
        # Calculate trend
        if len(velocities) >= 2:
            recent_avg = sum(velocities[-2:]) / 2
            older_avg = sum(velocities[:-2]) / max(1, len(velocities) - 2)
            trend = "Improving" if recent_avg > older_avg else "Declining" if recent_avg < older_avg else "Stable"
        else:
            trend = "Insufficient data"
        
        return {
            "average": round(average_velocity, 1),
            "trend": trend,
            "sprints_analyzed": len(velocities),
            "velocities": velocities
        }
    
    def generate_burndown_data(self, sprint_id: str) -> Dict:
        """Generate burndown chart data for a sprint"""
        from core.data_store import DataStore
        data_store = DataStore()
        
        sprint = data_store.get_sprint(sprint_id)
        if not sprint:
            return {}
        
        start_date = datetime.fromisoformat(sprint['start_date'])
        end_date = datetime.fromisoformat(sprint['end_date'])
        total_points = sprint.get('total_points', 0)
        
        # Generate ideal burndown line
        days = (end_date - start_date).days
        ideal_line = []
        for i in range(days + 1):
            remaining = total_points - (total_points * i / days)
            ideal_line.append({
                "day": i,
                "ideal_remaining": round(remaining, 1),
                "date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            })
        
        # Get actual burndown data
        actual_line = data_store.get_burndown_history(sprint_id)
        
        return {
            "ideal_line": ideal_line,
            "actual_line": actual_line,
            "total_points": total_points,
            "days_in_sprint": days
        }
    
    def get_sprint_progress(self, sprint_id: str) -> Dict:
        """Get detailed sprint progress information"""
        from core.data_store import DataStore
        data_store = DataStore()
        
        sprint = data_store.get_sprint(sprint_id)
        if not sprint:
            return {}
        
        total_points = sprint.get('total_points', 0)
        completed_points = sprint.get('completed_points', 0)
        
        progress_percentage = (completed_points / total_points * 100) if total_points > 0 else 0
        
        # Get story status distribution
        story_statuses = {}
        for story_id in sprint.get('stories', []):
            story = data_store.get_story(story_id)
            if story:
                status = story.get('status', 'Unknown')
                story_statuses[status] = story_statuses.get(status, 0) + 1
        
        # Calculate days remaining
        end_date = datetime.fromisoformat(sprint['end_date'])
        days_remaining = max(0, (end_date - datetime.now()).days)
        
        return {
            "progress_percentage": round(progress_percentage, 1),
            "completed_points": completed_points,
            "total_points": total_points,
            "remaining_points": total_points - completed_points,
            "story_statuses": story_statuses,
            "days_remaining": days_remaining,
            "stories_count": len(sprint.get('stories', []))
        }
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())[:8]
