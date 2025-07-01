"""
Utility helper functions for NeuralSprint application
"""

import streamlit as st
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import uuid

def generate_unique_id(prefix: str = "") -> str:
    """Generate a unique identifier with optional prefix"""
    unique_id = str(uuid.uuid4())[:8]
    return f"{prefix}_{unique_id}" if prefix else unique_id

def format_date(date_string: str, format_type: str = "display") -> str:
    """Format date string for display or storage"""
    try:
        if not date_string:
            return "Not set"
        
        date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        
        if format_type == "display":
            return date_obj.strftime("%B %d, %Y")
        elif format_type == "short":
            return date_obj.strftime("%m/%d/%Y")
        elif format_type == "iso":
            return date_obj.isoformat()
        else:
            return date_obj.strftime("%Y-%m-%d")
    except (ValueError, AttributeError):
        return date_string

def calculate_days_between(start_date: str, end_date: str) -> int:
    """Calculate number of days between two dates"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        return (end - start).days
    except (ValueError, AttributeError):
        return 0

def get_sprint_status_color(status: str) -> str:
    """Get color code for sprint status"""
    status_colors = {
        "Planning": "#ffa726",
        "Active": "#66bb6a",
        "Completed": "#42a5f5",
        "Cancelled": "#ef5350"
    }
    return status_colors.get(status, "#9e9e9e")

def get_story_status_color(status: str) -> str:
    """Get color code for story status"""
    status_colors = {
        "Backlog": "#9e9e9e",
        "To Do": "#2196f3",
        "In Progress": "#ff9800",
        "In Review": "#9c27b0",
        "Done": "#4caf50",
        "Cancelled": "#f44336"
    }
    return status_colors.get(status, "#9e9e9e")

def get_priority_color(priority: str) -> str:
    """Get color code for priority level"""
    priority_colors = {
        "Critical": "#d32f2f",
        "High": "#f57c00",
        "Medium": "#1976d2",
        "Low": "#388e3c"
    }
    return priority_colors.get(priority, "#1976d2")

def validate_story_data(story_data: Dict) -> tuple[bool, List[str]]:
    """Validate story data and return validation result with errors"""
    errors = []
    
    # Required fields validation
    if not story_data.get('title', '').strip():
        errors.append("Story title is required")
    
    if not story_data.get('description', '').strip():
        errors.append("Story description is required")
    
    # Story points validation
    story_points = story_data.get('story_points')
    if story_points is not None:
        try:
            points = float(story_points)
            if points < 0 or points > 100:
                errors.append("Story points must be between 0 and 100")
        except (ValueError, TypeError):
            errors.append("Story points must be a valid number")
    
    # Priority validation
    valid_priorities = ["Critical", "High", "Medium", "Low"]
    if story_data.get('priority') not in valid_priorities:
        errors.append(f"Priority must be one of: {', '.join(valid_priorities)}")
    
    return len(errors) == 0, errors

def validate_sprint_data(sprint_data: Dict) -> tuple[bool, List[str]]:
    """Validate sprint data and return validation result with errors"""
    errors = []
    
    # Required fields validation
    if not sprint_data.get('name', '').strip():
        errors.append("Sprint name is required")
    
    # Date validation
    start_date = sprint_data.get('start_date')
    end_date = sprint_data.get('end_date')
    
    if not start_date:
        errors.append("Sprint start date is required")
    
    if not end_date:
        errors.append("Sprint end date is required")
    
    if start_date and end_date:
        try:
            start = datetime.fromisoformat(start_date)
            end = datetime.fromisoformat(end_date)
            if start >= end:
                errors.append("Sprint end date must be after start date")
        except ValueError:
            errors.append("Invalid date format")
    
    # Capacity validation
    capacity = sprint_data.get('capacity')
    if capacity is not None:
        try:
            cap = int(capacity)
            if cap <= 0:
                errors.append("Sprint capacity must be positive")
        except (ValueError, TypeError):
            errors.append("Sprint capacity must be a valid number")
    
    return len(errors) == 0, errors

def sanitize_text_input(text: str, max_length: int = None) -> str:
    """Sanitize text input by removing harmful characters and limiting length"""
    if not text:
        return ""
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\'\&]', '', text.strip())
    
    # Limit length if specified
    if max_length and len(sanitized) > max_length:
        sanitized = sanitized[:max_length] + "..."
    
    return sanitized

def parse_labels(labels_string: str) -> List[str]:
    """Parse comma-separated labels string into list"""
    if not labels_string:
        return []
    
    labels = [label.strip() for label in labels_string.split(',')]
    return [label for label in labels if label]  # Remove empty strings

def format_story_points(points: Optional[float]) -> str:
    """Format story points for display"""
    if points is None:
        return "Not estimated"
    
    if points == int(points):
        return str(int(points))
    else:
        return f"{points:.1f}"

def calculate_completion_percentage(completed: int, total: int) -> float:
    """Calculate completion percentage with safe division"""
    if total == 0:
        return 0.0
    return (completed / total) * 100

def get_sprint_days_remaining(end_date: str) -> int:
    """Calculate days remaining in sprint"""
    try:
        end = datetime.fromisoformat(end_date)
        now = datetime.now()
        days_remaining = (end - now).days
        return max(0, days_remaining)  # Don't return negative days
    except (ValueError, AttributeError):
        return 0

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def safe_json_load(file_path: str, default: Any = None) -> Any:
    """Safely load JSON file with error handling"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, UnicodeDecodeError):
        return default if default is not None else {}

def safe_json_save(file_path: str, data: Any) -> bool:
    """Safely save data to JSON file with error handling"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        return True
    except Exception as e:
        st.error(f"Error saving file {file_path}: {str(e)}")
        return False

def extract_keywords(text: str, min_length: int = 3) -> List[str]:
    """Extract keywords from text for search and analysis"""
    if not text:
        return []
    
    # Convert to lowercase and split into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out short words and common stop words
    stop_words = {'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'are', 'as', 'was', 'will', 'be'}
    keywords = [word for word in words if len(word) >= min_length and word not in stop_words]
    
    return list(set(keywords))  # Remove duplicates

def calculate_velocity_trend(velocities: List[float]) -> str:
    """Calculate velocity trend from historical data"""
    if len(velocities) < 2:
        return "Insufficient data"
    
    if len(velocities) < 4:
        # Simple comparison for small datasets
        recent = velocities[-1]
        previous = velocities[-2]
        if recent > previous * 1.1:
            return "Improving"
        elif recent < previous * 0.9:
            return "Declining"
        else:
            return "Stable"
    
    # More sophisticated trend analysis for larger datasets
    recent_avg = sum(velocities[-3:]) / 3
    older_avg = sum(velocities[:-3]) / len(velocities[:-3])
    
    difference_pct = (recent_avg - older_avg) / older_avg * 100
    
    if difference_pct > 10:
        return "Improving"
    elif difference_pct < -10:
        return "Declining"
    else:
        return "Stable"

def format_duration(hours: float) -> str:
    """Format duration in hours to human readable format"""
    if hours < 1:
        minutes = int(hours * 60)
        return f"{minutes} minutes"
    elif hours < 24:
        return f"{hours:.1f} hours"
    else:
        days = hours / 24
        return f"{days:.1f} days"

def get_team_member_initials(name: str) -> str:
    """Get initials from team member name"""
    if not name:
        return "?"
    
    words = name.split()
    if len(words) == 1:
        return words[0][:2].upper()
    else:
        return ''.join(word[0] for word in words[:2]).upper()

def calculate_business_days(start_date: str, end_date: str) -> int:
    """Calculate business days between two dates (excluding weekends)"""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        
        business_days = 0
        current_date = start
        
        while current_date <= end:
            if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
                business_days += 1
            current_date += timedelta(days=1)
        
        return business_days
    except (ValueError, AttributeError):
        return 0

def create_backup_filename(base_name: str) -> str:
    """Create backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name_parts = base_name.split('.')
    if len(name_parts) > 1:
        return f"{'.'.join(name_parts[:-1])}_backup_{timestamp}.{name_parts[-1]}"
    else:
        return f"{base_name}_backup_{timestamp}"

def validate_email(email: str) -> bool:
    """Validate email address format"""
    if not email:
        return False
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def truncate_text(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def get_time_ago(timestamp: str) -> str:
    """Get human readable time ago from timestamp"""
    try:
        past_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.now()
        
        if past_time.tzinfo:
            now = now.replace(tzinfo=past_time.tzinfo)
        
        diff = now - past_time
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    except (ValueError, AttributeError):
        return "Unknown time"

def create_export_data(data: List[Dict], fields: List[str]) -> str:
    """Create CSV export data from list of dictionaries"""
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fields)
    
    writer.writeheader()
    for row in data:
        # Only include specified fields
        filtered_row = {field: row.get(field, '') for field in fields}
        writer.writerow(filtered_row)
    
    return output.getvalue()

def show_success_message(message: str, icon: str = "✅"):
    """Show success message with custom styling"""
    st.success(f"{icon} {message}")

def show_error_message(message: str, icon: str = "❌"):
    """Show error message with custom styling"""
    st.error(f"{icon} {message}")

def show_warning_message(message: str, icon: str = "⚠️"):
    """Show warning message with custom styling"""
    st.warning(f"{icon} {message}")

def show_info_message(message: str, icon: str = "ℹ️"):
    """Show info message with custom styling"""
    st.info(f"{icon} {message}")

class SessionStateManager:
    """Utility class for managing Streamlit session state"""
    
    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get value from session state with default"""
        return st.session_state.get(key, default)
    
    @staticmethod
    def set(key: str, value: Any) -> None:
        """Set value in session state"""
        st.session_state[key] = value
    
    @staticmethod
    def delete(key: str) -> None:
        """Delete key from session state if it exists"""
        if key in st.session_state:
            del st.session_state[key]
    
    @staticmethod
    def clear_prefix(prefix: str) -> None:
        """Clear all session state keys with given prefix"""
        keys_to_delete = [key for key in st.session_state.keys() if key.startswith(prefix)]
        for key in keys_to_delete:
            del st.session_state[key]
    
    @staticmethod
    def initialize_if_missing(key: str, default: Any) -> Any:
        """Initialize session state key if missing and return value"""
        if key not in st.session_state:
            st.session_state[key] = default
        return st.session_state[key]

def debounce_input(key: str, value: Any, delay_seconds: float = 0.5) -> bool:
    """Debounce input changes to prevent excessive updates"""
    current_time = datetime.now()
    last_update_key = f"{key}_last_update"
    
    if last_update_key not in st.session_state:
        st.session_state[last_update_key] = current_time
        st.session_state[key] = value
        return True
    
    time_diff = (current_time - st.session_state[last_update_key]).total_seconds()
    
    if time_diff >= delay_seconds:
        st.session_state[last_update_key] = current_time
        st.session_state[key] = value
        return True
    
    return False
