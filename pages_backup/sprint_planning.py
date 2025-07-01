import streamlit as st
from datetime import datetime, timedelta
from core.scrum_manager import ScrumManager
import plotly.graph_objects as go
import plotly.express as px

def show_sprint_planning():
    """Sprint planning interface"""
    
    st.markdown("## 🚀 SPRINT PLANNING MATRIX")
    
    # Check AI connection
    if not st.session_state.ai_client.check_connection():
        st.warning("⚠️ AI assistance unavailable. Manual planning mode active.")
    
    tab1, tab2, tab3 = st.tabs(["📋 Plan Sprint", "📊 Sprint Overview", "🎯 Sprint Goals"])
    
    with tab1:
        show_sprint_creation()
    
    with tab2:
        show_sprint_overview()
    
    with tab3:
        show_sprint_goals()

def show_sprint_creation():
    """Sprint creation and story selection interface"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔧 CREATE NEW SPRINT")
        
        # Sprint details form
        with st.form("create_sprint"):
            sprint_name = st.text_input("Sprint Name", placeholder="Sprint 2024-Q1-01")
            
            col_start, col_duration = st.columns(2)
            with col_start:
                start_date = st.date_input("Start Date", value=datetime.now().date())
            with col_duration:
                duration = st.selectbox("Duration (weeks)", [1, 2, 3, 4], index=1)
            
            team_capacity = st.number_input("Team Capacity (Story Points)", 
                                          min_value=1, max_value=200, value=40)
            
            sprint_goals = st.text_area("Sprint Goals", 
                                      placeholder="What are the main objectives for this sprint?")
            
            if st.form_submit_button("🚀 Create Sprint", use_container_width=True):
                if sprint_name:
                    end_date = start_date + timedelta(weeks=duration)
                    
                    sprint = st.session_state.scrum_manager.create_sprint(
                        name=sprint_name,
                        duration_weeks=duration,
                        start_date=start_date.isoformat(),
                        capacity=team_capacity
                    )
                    
                    sprint['goals'] = [goal.strip() for goal in sprint_goals.split('\n') if goal.strip()]
                    
                    if st.session_state.data_store.save_sprint(sprint):
                        st.success(f"✅ Sprint '{sprint_name}' created successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create sprint")
                else:
                    st.error("Please provide a sprint name")
        
        # Story selection for active sprint
        current_sprint = st.session_state.data_store.get_current_sprint()
        if current_sprint:
            st.markdown("### 📝 MANAGE SPRINT BACKLOG")
            
            # Get all stories not in current sprint
            all_stories = st.session_state.data_store.get_all_stories()
            available_stories = [s for s in all_stories 
                               if s['id'] not in current_sprint.get('stories', []) 
                               and s.get('status') != 'Done']
            
            if available_stories:
                selected_stories = st.multiselect(
                    "Add Stories to Sprint",
                    options=[s['id'] for s in available_stories],
                    format_func=lambda x: f"{next(s['title'] for s in available_stories if s['id'] == x)} "
                                         f"({next(s.get('story_points', 'Not estimated') for s in available_stories if s['id'] == x)} pts)"
                )
                
                if st.button("➕ Add Selected Stories"):
                    added_count = 0
                    for story_id in selected_stories:
                        if st.session_state.scrum_manager.add_story_to_sprint(current_sprint['id'], story_id):
                            added_count += 1
                    
                    if added_count > 0:
                        st.success(f"✅ Added {added_count} stories to sprint")
                        st.rerun()
            else:
                st.info("No available stories to add to sprint")
    
    with col2:
        st.markdown("### 🤖 AI ASSISTANCE")
        
        # AI-powered sprint planning
        if st.button("🧠 Generate Sprint Plan", use_container_width=True):
            if st.session_state.ai_client.check_connection():
                with st.spinner("Analyzing backlog and generating optimal sprint plan..."):
                    backlog_items = st.session_state.data_store.get_all_stories()
                    available_items = [s for s in backlog_items if s.get('status') == 'Backlog']
                    
                    current_sprint = st.session_state.data_store.get_current_sprint()
                    capacity = current_sprint.get('capacity', 40) if current_sprint else 40
                    
                    sprint_plan = st.session_state.ai_client.generate_sprint_plan(
                        available_items, capacity
                    )
                    
                    if sprint_plan:
                        st.success("🎯 AI Sprint Plan Generated!")
                        st.write(sprint_plan)
                    else:
                        st.error("Failed to generate sprint plan")
            else:
                st.error("AI service unavailable")
        
        # Quick actions
        st.markdown("### ⚡ QUICK ACTIONS")
        
        if st.button("📊 Capacity Analysis", use_container_width=True):
            current_sprint = st.session_state.data_store.get_current_sprint()
            if current_sprint:
                total_capacity = current_sprint.get('capacity', 0)
                used_capacity = current_sprint.get('total_points', 0)
                remaining_capacity = total_capacity - used_capacity
                
                st.metric("Remaining Capacity", f"{remaining_capacity} pts")
                st.progress(min(used_capacity / total_capacity, 1.0))
            else:
                st.info("No active sprint")

def show_sprint_overview():
    """Sprint overview with progress tracking"""
    
    current_sprint = st.session_state.data_store.get_current_sprint()
    
    if not current_sprint:
        st.info("No active sprint. Create a sprint to see overview.")
        return
    
    st.markdown(f"### 📊 {current_sprint['name']} OVERVIEW")
    
    # Progress metrics
    progress_data = st.session_state.scrum_manager.get_sprint_progress(current_sprint['id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Progress", f"{progress_data['progress_percentage']}%")
    with col2:
        st.metric("Completed Points", progress_data['completed_points'])
    with col3:
        st.metric("Remaining Points", progress_data['remaining_points'])
    with col4:
        st.metric("Days Left", progress_data['days_remaining'])
    
    # Progress bar
    progress_value = progress_data['progress_percentage'] / 100
    st.progress(progress_value)
    
    # Burndown chart
    st.markdown("### 📈 BURNDOWN ANALYSIS")
    
    burndown_data = st.session_state.scrum_manager.generate_burndown_data(current_sprint['id'])
    
    if burndown_data:
        fig = go.Figure()
        
        # Ideal line
        ideal_line = burndown_data['ideal_line']
        fig.add_trace(go.Scatter(
            x=[point['date'] for point in ideal_line],
            y=[point['ideal_remaining'] for point in ideal_line],
            mode='lines',
            name='Ideal Burndown',
            line=dict(color='#00ff88', dash='dash')
        ))
        
        # Actual line
        actual_line = burndown_data['actual_line']
        if actual_line:
            fig.add_trace(go.Scatter(
                x=[point['date'] for point in actual_line],
                y=[point['actual_remaining'] for point in actual_line],
                mode='lines+markers',
                name='Actual Burndown',
                line=dict(color='#ff6b6b')
            ))
        
        fig.update_layout(
            title="Sprint Burndown Chart",
            xaxis_title="Date",
            yaxis_title="Story Points Remaining",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Story status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 STORY STATUS")
        status_counts = progress_data['story_statuses']
        
        if status_counts:
            fig_pie = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Story Distribution by Status"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 SPRINT STORIES")
        
        # List stories in sprint
        for story_id in current_sprint.get('stories', []):
            story = st.session_state.data_store.get_story(story_id)
            if story:
                status_color = {
                    'Backlog': '#888',
                    'To Do': '#ffd43b',
                    'In Progress': '#339af0',
                    'In Review': '#fd7e14',
                    'Done': '#51cf66'
                }.get(story['status'], '#888')
                
                st.markdown(f"""
                <div style='padding: 8px; margin: 4px 0; border-left: 4px solid {status_color}; background: rgba(255,255,255,0.05); border-radius: 4px;'>
                    <strong>{story['title']}</strong><br>
                    <small>Status: {story['status']} | Points: {story.get('story_points', 'Not estimated')}</small>
                </div>
                """, unsafe_allow_html=True)

def show_sprint_goals():
    """Sprint goals management"""
    
    current_sprint = st.session_state.data_store.get_current_sprint()
    
    if not current_sprint:
        st.info("No active sprint. Create a sprint to set goals.")
        return
    
    st.markdown(f"### 🎯 {current_sprint['name']} GOALS")
    
    # Display current goals
    goals = current_sprint.get('goals', [])
    
    if goals:
        st.markdown("#### Current Goals:")
        for i, goal in enumerate(goals):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"• {goal}")
            with col2:
                if st.button("❌", key=f"remove_goal_{i}"):
                    goals.remove(goal)
                    current_sprint['goals'] = goals
                    st.session_state.data_store.update_sprint(current_sprint['id'], current_sprint)
                    st.rerun()
    else:
        st.info("No goals set for this sprint.")
    
    # Add new goal
    with st.form("add_goal"):
        new_goal = st.text_input("Add New Goal")
        if st.form_submit_button("➕ Add Goal"):
            if new_goal.strip():
                if 'goals' not in current_sprint:
                    current_sprint['goals'] = []
                current_sprint['goals'].append(new_goal.strip())
                st.session_state.data_store.update_sprint(current_sprint['id'], current_sprint)
                st.success("Goal added successfully!")
                st.rerun()
    
    # Sprint retrospective preview
    if current_sprint.get('status') == 'Completed':
        st.markdown("### 🔄 RETROSPECTIVE INSIGHTS")
        if st.button("🧠 Generate AI Insights"):
            with st.spinner("Analyzing sprint performance..."):
                retrospective_data = {
                    "sprint": current_sprint,
                    "goals_achieved": len([g for g in goals if "completed" in g.lower()]),
                    "total_goals": len(goals),
                    "velocity": current_sprint.get('completed_points', 0)
                }
                
                insights = st.session_state.ai_client.generate_retrospective_insights(retrospective_data)
                if insights:
                    st.write(insights)
