import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import streamlit as st

class DataStore:
    """Simple file-based data storage for NeuralSprint"""
    
    def __init__(self):
        self.data_dir = "data"
        self.ensure_data_directory()
        
        # File paths
        self.stories_file = os.path.join(self.data_dir, "stories.json")
        self.sprints_file = os.path.join(self.data_dir, "sprints.json")
        self.activities_file = os.path.join(self.data_dir, "activities.json")
        self.team_file = os.path.join(self.data_dir, "team.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def _load_json(self, file_path: str, default: any = None) -> any:
        """Load JSON data from file"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default or []
        except Exception as e:
            st.error(f"Error loading {file_path}: {str(e)}")
            return default or []
    
    def _save_json(self, file_path: str, data: any) -> bool:
        """Save JSON data to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            st.error(f"Error saving {file_path}: {str(e)}")
            return False
    
    # Story management
    def save_story(self, story: Dict) -> bool:
        """Save a user story"""
        stories = self._load_json(self.stories_file, [])
        
        # Update existing or add new
        updated = False
        for i, existing_story in enumerate(stories):
            if existing_story['id'] == story['id']:
                stories[i] = story
                updated = True
                break
        
        if not updated:
            stories.append(story)
        
        success = self._save_json(self.stories_file, stories)
        if success:
            self._log_activity("Story", f"{'Updated' if updated else 'Created'} story: {story['title']}")
        return success
    
    def get_story(self, story_id: str) -> Optional[Dict]:
        """Get a specific story by ID"""
        stories = self._load_json(self.stories_file, [])
        for story in stories:
            if story['id'] == story_id:
                return story
        return None
    
    def get_all_stories(self) -> List[Dict]:
        """Get all stories"""
        return self._load_json(self.stories_file, [])
    
    def update_story(self, story_id: str, updated_story: Dict) -> bool:
        """Update an existing story"""
        return self.save_story(updated_story)
    
    def delete_story(self, story_id: str) -> bool:
        """Delete a story"""
        stories = self._load_json(self.stories_file, [])
        stories = [s for s in stories if s['id'] != story_id]
        success = self._save_json(self.stories_file, stories)
        if success:
            self._log_activity("Story", f"Deleted story: {story_id}")
        return success
    
    # Sprint management
    def save_sprint(self, sprint: Dict) -> bool:
        """Save a sprint"""
        sprints = self._load_json(self.sprints_file, [])
        
        # Update existing or add new
        updated = False
        for i, existing_sprint in enumerate(sprints):
            if existing_sprint['id'] == sprint['id']:
                sprints[i] = sprint
                updated = True
                break
        
        if not updated:
            sprints.append(sprint)
        
        success = self._save_json(self.sprints_file, sprints)
        if success:
            self._log_activity("Sprint", f"{'Updated' if updated else 'Created'} sprint: {sprint['name']}")
        return success
    
    def get_sprint(self, sprint_id: str) -> Optional[Dict]:
        """Get a specific sprint by ID"""
        sprints = self._load_json(self.sprints_file, [])
        for sprint in sprints:
            if sprint['id'] == sprint_id:
                return sprint
        return None
    
    def get_all_sprints(self) -> List[Dict]:
        """Get all sprints"""
        return self._load_json(self.sprints_file, [])
    
    def get_current_sprint(self) -> Optional[Dict]:
        """Get the currently active sprint"""
        sprints = self._load_json(self.sprints_file, [])
        for sprint in sprints:
            if sprint.get('status') == 'Active':
                return sprint
        return None
    
    def update_sprint(self, sprint_id: str, updated_sprint: Dict) -> bool:
        """Update an existing sprint"""
        return self.save_sprint(updated_sprint)
    
    # Activity logging
    def _log_activity(self, activity_type: str, description: str):
        """Log an activity"""
        activities = self._load_json(self.activities_file, [])
        
        activity = {
            "id": self._generate_id(),
            "type": activity_type,
            "description": description,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        activities.insert(0, activity)  # Add to beginning
        
        # Keep only last 100 activities
        activities = activities[:100]
        
        self._save_json(self.activities_file, activities)
    
    def get_recent_activities(self, limit: int = 10) -> List[Dict]:
        """Get recent activities"""
        activities = self._load_json(self.activities_file, [])
        return activities[:limit]
    
    # Quick stats and analytics
    def get_quick_stats(self) -> Dict:
        """Get quick statistics for dashboard"""
        stories = self._load_json(self.stories_file, [])
        current_sprint = self.get_current_sprint()
        
        active_stories = len([s for s in stories if s.get('status') not in ['Done', 'Cancelled']])
        completed_stories = len([s for s in stories if s.get('status') == 'Done'])
        
        sprint_days_left = 0
        velocity = 0
        
        if current_sprint:
            end_date = datetime.strptime(current_sprint['end_date'], "%Y-%m-%d")
            sprint_days_left = max(0, (end_date - datetime.now()).days)
            velocity = current_sprint.get('completed_points', 0)
        
        return {
            "active_stories": active_stories,
            "completed_stories": completed_stories,
            "sprint_days_left": sprint_days_left,
            "velocity": velocity
        }
    
    def get_current_sprint_data(self) -> Dict:
        """Get comprehensive current sprint data for AI analysis"""
        current_sprint = self.get_current_sprint()
        if not current_sprint:
            return {}
        
        stories = []
        for story_id in current_sprint.get('stories', []):
            story = self.get_story(story_id)
            if story:
                stories.append(story)
        
        return {
            "sprint": current_sprint,
            "stories": stories,
            "total_stories": len(stories),
            "progress": current_sprint.get('completed_points', 0) / max(1, current_sprint.get('total_points', 1)) * 100
        }
    
    def get_today_tasks(self) -> List[Dict]:
        """Get tasks scheduled for today"""
        # For demo purposes, return stories in progress
        stories = self._load_json(self.stories_file, [])
        return [s for s in stories if s.get('status') == 'In Progress'][:5]
    
    def get_recent_updates(self) -> List[Dict]:
        """Get recent team updates for standup"""
        # Return mock team updates - in real implementation, this would come from team input
        return [
            {
                "member": "Alice",
                "yesterday": "Completed user authentication module",
                "today": "Working on API integration tests",
                "blockers": "Waiting for test environment setup"
            },
            {
                "member": "Bob",
                "yesterday": "Fixed database connection issues",
                "today": "Implementing payment gateway",
                "blockers": "None"
            }
        ]
    
    def get_velocity_history(self) -> List[Dict]:
        """Get historical velocity data"""
        sprints = self._load_json(self.sprints_file, [])
        completed_sprints = [s for s in sprints if s.get('status') == 'Completed']
        
        return [
            {
                "sprint_name": sprint['name'],
                "completed_points": sprint.get('completed_points', 0),
                "planned_points": sprint.get('total_points', 0),
                "end_date": sprint['end_date']
            }
            for sprint in completed_sprints
        ]
    
    def get_workflow_data(self) -> Dict:
        """Get workflow data for bottleneck analysis"""
        stories = self._load_json(self.stories_file, [])
        
        status_counts = {}
        for story in stories:
            status = story.get('status', 'Unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "status_distribution": status_counts,
            "total_stories": len(stories),
            "avg_cycle_time": 5.2,  # Mock data - calculate from actual story history
            "blocked_stories": len([s for s in stories if 'blocked' in s.get('labels', [])])
        }
    
    def get_burndown_history(self, sprint_id: str) -> List[Dict]:
        """Get burndown history for a sprint"""
        # Mock burndown data - in real implementation, this would be tracked daily
        sprint = self.get_sprint(sprint_id)
        if not sprint:
            return []
        
        start_date = datetime.strptime(sprint['start_date'], "%Y-%m-%d")
        total_points = sprint.get('total_points', 0)
        
        # Generate mock actual burndown
        days = min(7, (datetime.now() - start_date).days)
        actual_line = []
        
        for i in range(days + 1):
            # Mock actual progress with some variance
            actual_remaining = total_points - (total_points * i / 10) - (i * 2)
            actual_remaining = max(0, actual_remaining)
            
            actual_line.append({
                "day": i,
                "actual_remaining": round(actual_remaining, 1),
                "date": (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            })
        
        return actual_line
    
    def _generate_id(self) -> str:
        """Generate a unique ID"""
        import uuid
        return str(uuid.uuid4())[:8]
