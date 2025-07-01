import requests
import json
import streamlit as st
import os
from typing import Dict, List, Optional
from utils.prompts import SCRUM_PROMPTS
import time

class AIClient:
    """Client for communicating with local Qwen3 4B model via LM Studio"""
    
    def __init__(self):
        self.base_url = os.getenv("LM_STUDIO_URL", "http://localhost:1234")
        self.api_endpoint = f"{self.base_url}/v1/chat/completions"
        self.model_name = os.getenv("MODEL_NAME", "qwen2.5-3b-instruct")
        self.max_tokens = 2048
        self.temperature = 0.7
        
    def check_connection(self) -> bool:
        """Check if LM Studio is available"""
        try:
            response = requests.get(f"{self.base_url}/v1/models", timeout=5)
            return response.status_code == 200
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")
            return False
    
    def _make_request(self, messages: List[Dict], temperature: float = None) -> Optional[str]:
        """Make a request to the local AI model"""
        try:
            payload = {
                "model": self.model_name,
                "messages": messages,
                "max_tokens": self.max_tokens,
                "temperature": temperature or self.temperature,
                "stream": False
            }
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                # Clean up thinking content
                cleaned_content = self._clean_thinking_content(content)
                return cleaned_content
            else:
                st.error(f"AI request failed: {response.status_code}")
                return None
                
        except Exception as e:
            st.error(f"AI communication error: {str(e)}")
            return None
    
    def estimate_story_points(self, story_title: str, description: str, acceptance_criteria: str) -> Optional[Dict]:
        """Estimate story points using AI analysis"""
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["story_estimation"]},
            {"role": "user", "content": f"""
            Story Title: {story_title}
            Description: {description}
            Acceptance Criteria: {acceptance_criteria}
            
            Please provide a detailed story point estimation with reasoning.
            """}
        ]
        
        response = self._make_request(messages, temperature=0.3)
        if response:
            try:
                # Parse AI response for story points and reasoning
                lines = response.strip().split('\n')
                points = None
                reasoning = response
                
                # Try to extract numeric value
                for line in lines:
                    if 'point' in line.lower() or 'estimate' in line.lower():
                        words = line.split()
                        for word in words:
                            if word.replace('.', '').isdigit():
                                points = float(word)
                                break
                
                return {
                    "estimated_points": points or 3,  # Default to 3 if can't parse
                    "reasoning": reasoning,
                    "complexity_factors": self._extract_complexity_factors(response)
                }
            except Exception as e:
                st.error(f"Error parsing estimation: {str(e)}")
                return None
        return None
    
    def generate_standup_summary(self, team_updates: List[Dict] = None) -> Optional[str]:
        """Generate daily standup summary"""
        if not team_updates:
            team_updates = st.session_state.data_store.get_recent_updates()
        
        updates_text = "\n".join([
            f"Team Member: {update.get('member', 'Unknown')}\n"
            f"Yesterday: {update.get('yesterday', 'No updates')}\n"
            f"Today: {update.get('today', 'No plans')}\n"
            f"Blockers: {update.get('blockers', 'None')}\n"
            for update in team_updates
        ])
        
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["standup_summary"]},
            {"role": "user", "content": f"Team Updates:\n{updates_text}"}
        ]
        
        return self._make_request(messages)
    
    def analyze_sprint_health(self) -> Optional[str]:
        """Analyze current sprint health and provide insights"""
        sprint_data = st.session_state.data_store.get_current_sprint_data()
        
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["sprint_analysis"]},
            {"role": "user", "content": f"Sprint Data: {json.dumps(sprint_data, indent=2)}"}
        ]
        
        return self._make_request(messages)
    
    def generate_retrospective_insights(self, retrospective_data: Dict) -> Optional[str]:
        """Generate retrospective insights and action items"""
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["retrospective"]},
            {"role": "user", "content": f"Retrospective Data: {json.dumps(retrospective_data, indent=2)}"}
        ]
        
        return self._make_request(messages)
    
    def predict_velocity(self) -> Optional[str]:
        """Predict team velocity based on historical data"""
        velocity_data = st.session_state.data_store.get_velocity_history()
        
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["velocity_prediction"]},
            {"role": "user", "content": f"Historical Velocity Data: {json.dumps(velocity_data, indent=2)}"}
        ]
        
        return self._make_request(messages)
    
    def detect_bottlenecks(self) -> Optional[str]:
        """Detect potential bottlenecks in the workflow"""
        workflow_data = st.session_state.data_store.get_workflow_data()
        
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["bottleneck_detection"]},
            {"role": "user", "content": f"Workflow Data: {json.dumps(workflow_data, indent=2)}"}
        ]
        
        return self._make_request(messages)
    
    def generate_sprint_plan(self, backlog_items: List[Dict], team_capacity: int) -> Optional[str]:
        """Generate optimal sprint plan based on backlog and capacity"""
        messages = [
            {"role": "system", "content": SCRUM_PROMPTS["sprint_planning"]},
            {"role": "user", "content": f"""
            Backlog Items: {json.dumps(backlog_items, indent=2)}
            Team Capacity: {team_capacity} story points
            
            Please create an optimal sprint plan.
            """}
        ]
        
        return self._make_request(messages)
    
    def _clean_thinking_content(self, content: str) -> str:
        """Remove thinking content from AI responses"""
        # Remove <think>...</think> blocks
        import re
        
        # Remove thinking blocks
        content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
        
        # Remove thinking patterns
        thinking_patterns = [
            r'<think>.*?</think>',
            r'Let me think about this.*?(?=\n\n|\n[A-Z]|$)',
            r'Okay, let\'s tackle this.*?(?=\n\n|\n[A-Z]|$)',
            r'I need to analyze.*?(?=\n\n|\n[A-Z]|$)',
            r'First, I\'ll.*?(?=\n\n|\n[A-Z]|$)',
            r'Let me structure.*?(?=\n\n|\n[A-Z]|$)',
            r'Wait,.*?(?=\n\n|\n[A-Z]|$)',
        ]
        
        for pattern in thinking_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        # Clean up extra whitespace
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
        content = content.strip()
        
        return content

    def _extract_complexity_factors(self, response: str) -> List[str]:
        """Extract complexity factors from AI response"""
        factors = []
        keywords = ['complex', 'dependency', 'integration', 'unknown', 'risk', 'technical']
        
        for keyword in keywords:
            if keyword in response.lower():
                factors.append(keyword.title())
        
        return factors or ["Standard Complexity"]
