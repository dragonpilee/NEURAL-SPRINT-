import streamlit as st
import os
from datetime import datetime
from core.ai_client import AIClient
from core.scrum_manager import ScrumManager
from core.data_store import DataStore
from assets.cyber_styles import apply_cyber_theme
import time

# Configure page
st.set_page_config(
    page_title="NeuralSprint - AI Scrum Master",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)



# Apply cyberpunk theme
apply_cyber_theme()

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    st.session_state.ai_client = AIClient()
    st.session_state.scrum_manager = ScrumManager()
    st.session_state.data_store = DataStore()

def main():
    # Header with cyberpunk styling
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #00ff88; font-size: 3em; text-shadow: 0 0 10px #00ff88;'>
            🤖 NEURAL SPRINT
        </h1>
        <p style='color: #888; font-size: 1.2em;'>
            Autonomous Scrum Management
        </p>
        <p style='color: #666; font-size: 0.9em; margin-top: 10px;'>
            Designed and developed by Alan Cyril Sunny
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### 🔗 NEURAL INTERFACE")
        
                # Connection status
        connection_status = st.session_state.ai_client.check_connection()
        status_color = "#00ff88" if connection_status else "#ff4444"
        status_text = "ONLINE" if connection_status else "OFFLINE"
        
        st.markdown(f"""
        <div style='padding: 10px; border: 1px solid {status_color}; border-radius: 5px; margin: 10px 0;'>
            <span style='color: {status_color};'>🔮 AI CORE: {status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation menu
        page = st.selectbox(
            "SELECT MODULE",
            ["🏠 Dashboard", "📋 Sprint Planning", "📝 Backlog Management", 
             "🎯 Daily Standup", "🔄 Retrospective", "📊 Analytics"],
            key="navigation"
        )
        
        # Quick stats
        stats = st.session_state.data_store.get_quick_stats()
        st.markdown("### 📈 QUICK STATS")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Active Stories", stats.get('active_stories', 0))
            st.metric("Completed", stats.get('completed_stories', 0))
        with col2:
            st.metric("Sprint Days", stats.get('sprint_days_left', 0))
            st.metric("Velocity", stats.get('velocity', 0))

    # Main content area
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📋 Sprint Planning":
        from pages.sprint_planning import show_sprint_planning
        show_sprint_planning()
    elif page == "📝 Backlog Management":
        from pages.backlog_management import show_backlog_management
        show_backlog_management()
    elif page == "🎯 Daily Standup":
        from pages.daily_standup import show_daily_standup
        show_daily_standup()
    elif page == "🔄 Retrospective":
        from pages.retrospective import show_retrospective
        show_retrospective()
    elif page == "📊 Analytics":
        from pages.analytics import show_analytics
        show_analytics()

def show_dashboard():
    """Main dashboard with overview and quick actions"""
    
    # Welcome message with time-based greeting
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning, Scrum Master"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon, Scrum Master"
    else:
        greeting = "Good Evening, Scrum Master"
    
    st.markdown(f"## 🌟 {greeting}")
    
    # Check AI connection
    if not st.session_state.ai_client.check_connection():
        st.error("⚠️ AI Core disconnected. Please ensure LM Studio is running on localhost:1234")
        return
    
    # Main dashboard grid
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🚀 CURRENT SPRINT")
        current_sprint = st.session_state.data_store.get_current_sprint()
        if current_sprint:
            st.write(f"**{current_sprint['name']}**")
            st.write(f"📅 {current_sprint['start_date']} - {current_sprint['end_date']}")
            progress = current_sprint.get('progress', 0)
            st.progress(progress / 100)
            st.write(f"Progress: {progress}%")
        else:
            st.info("No active sprint. Start a new sprint in Sprint Planning.")
    
    with col2:
        st.markdown("### 📋 TODAY'S FOCUS")
        today_tasks = st.session_state.data_store.get_today_tasks()
        if today_tasks:
            for task in today_tasks[:3]:  # Show top 3
                st.write(f"• {task['title']}")
        else:
            st.info("No tasks scheduled for today.")
    
    with col3:
        st.markdown("### 🎯 QUICK ACTIONS")
        if st.button("🤖 AI Sprint Analysis", use_container_width=True):
            with st.spinner("Analyzing sprint data..."):
                analysis = st.session_state.ai_client.analyze_sprint_health()
                if analysis:
                    st.success("Analysis complete!")
                    st.write(analysis)
        
        if st.button("📝 Generate Standup", use_container_width=True):
            with st.spinner("Generating standup summary..."):
                standup = st.session_state.ai_client.generate_standup_summary()
                if standup:
                    st.success("Standup ready!")
                    st.write(standup)
    
    # Recent activity feed
    st.markdown("### 📡 RECENT ACTIVITY")
    activities = st.session_state.data_store.get_recent_activities()
    
    if activities:
        for activity in activities[:5]:  # Show last 5 activities
            with st.expander(f"🔸 {activity['timestamp']} - {activity['type']}"):
                st.write(activity['description'])
    else:
        st.info("No recent activities to display.")
    
    # Quick team insights
    st.markdown("### 🧠 AI INSIGHTS")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔮 Team Velocity Prediction"):
            with st.spinner("Calculating velocity trends..."):
                prediction = st.session_state.ai_client.predict_velocity()
                if prediction:
                    st.write(prediction)
    
    with col2:
        if st.button("⚡ Bottleneck Detection"):
            with st.spinner("Scanning for bottlenecks..."):
                bottlenecks = st.session_state.ai_client.detect_bottlenecks()
                if bottlenecks:
                    st.write(bottlenecks)

if __name__ == "__main__":
    main()
