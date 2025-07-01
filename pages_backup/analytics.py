import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json

def show_analytics():
    """Advanced analytics dashboard for sprint and team performance"""
    
    st.markdown("## 📊 NEURAL ANALYTICS MATRIX")
    
    # Check if we have enough data for analytics
    all_sprints = st.session_state.data_store.get_all_sprints()
    all_stories = st.session_state.data_store.get_all_stories()
    
    if not all_sprints and not all_stories:
        st.info("No data available for analytics. Create some sprints and stories first.")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Sprint Analytics", "👥 Team Performance", "🎯 Velocity Tracking", "🔍 Predictive Insights"])
    
    with tab1:
        show_sprint_analytics()
    
    with tab2:
        show_team_performance()
    
    with tab3:
        show_velocity_tracking()
    
    with tab4:
        show_predictive_insights()

def show_sprint_analytics():
    """Sprint-focused analytics and metrics"""
    
    st.markdown("### 🚀 SPRINT PERFORMANCE DASHBOARD")
    
    all_sprints = st.session_state.data_store.get_all_sprints()
    
    if not all_sprints:
        st.info("No sprint data available for analysis.")
        return
    
    # Sprint selection
    selected_sprint = st.selectbox(
        "Select Sprint for Analysis",
        options=all_sprints,
        format_func=lambda x: f"{x['name']} ({x.get('status', 'Unknown')})",
        index=0 if all_sprints else None
    )
    
    if not selected_sprint:
        return
    
    # Sprint overview metrics
    progress = st.session_state.scrum_manager.get_sprint_progress(selected_sprint['id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Completion Rate", f"{progress['progress_percentage']}%")
    
    with col2:
        velocity = progress['completed_points']
        capacity = selected_sprint.get('capacity', 0)
        velocity_percentage = (velocity / capacity * 100) if capacity > 0 else 0
        st.metric("Velocity vs Capacity", f"{velocity_percentage:.1f}%")
    
    with col3:
        stories_done = len([status for status in progress['story_statuses'] if status == 'Done'])
        total_stories = progress['stories_count']
        story_completion = (stories_done / total_stories * 100) if total_stories > 0 else 0
        st.metric("Stories Completed", f"{story_completion:.1f}%")
    
    with col4:
        st.metric("Days Remaining", progress['days_remaining'])
    
    # Burndown chart
    st.markdown("### 📈 SPRINT BURNDOWN ANALYSIS")
    
    burndown_data = st.session_state.scrum_manager.generate_burndown_data(selected_sprint['id'])
    
    if burndown_data:
        fig = go.Figure()
        
        # Ideal burndown line
        ideal_line = burndown_data['ideal_line']
        if ideal_line:
            fig.add_trace(go.Scatter(
                x=[point['date'] for point in ideal_line],
                y=[point['ideal_remaining'] for point in ideal_line],
                mode='lines',
                name='Ideal Burndown',
                line=dict(color='#00ff88', dash='dash', width=2)
            ))
        
        # Actual burndown line
        actual_line = burndown_data['actual_line']
        if actual_line:
            fig.add_trace(go.Scatter(
                x=[point['date'] for point in actual_line],
                y=[point['actual_remaining'] for point in actual_line],
                mode='lines+markers',
                name='Actual Burndown',
                line=dict(color='#ff6b6b', width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title="Sprint Burndown Chart",
            xaxis_title="Date",
            yaxis_title="Story Points Remaining",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Story status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 STORY STATUS DISTRIBUTION")
        
        if progress['story_statuses']:
            status_df = pd.DataFrame([
                {'Status': status, 'Count': count} 
                for status, count in progress['story_statuses'].items()
            ])
            
            fig_pie = px.pie(
                status_df, 
                values='Count', 
                names='Status',
                title="Stories by Status",
                color_discrete_map={
                    'Backlog': '#666666',
                    'To Do': '#3498db', 
                    'In Progress': '#f39c12',
                    'In Review': '#9b59b6',
                    'Done': '#27ae60'
                }
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 STORY POINTS ANALYSIS")
        
        # Get stories in sprint
        sprint_stories = []
        for story_id in selected_sprint.get('stories', []):
            story = st.session_state.data_store.get_story(story_id)
            if story:
                sprint_stories.append(story)
        
        if sprint_stories:
            # Story points by status
            points_by_status = {}
            for story in sprint_stories:
                status = story.get('status', 'Unknown')
                points = story.get('story_points', 0) or 0
                points_by_status[status] = points_by_status.get(status, 0) + points
            
            if points_by_status:
                fig_bar = go.Figure(data=[
                    go.Bar(
                        x=list(points_by_status.keys()),
                        y=list(points_by_status.values()),
                        marker_color=['#666666', '#3498db', '#f39c12', '#9b59b6', '#27ae60'][:len(points_by_status)]
                    )
                ])
                
                fig_bar.update_layout(
                    title="Story Points by Status",
                    xaxis_title="Status",
                    yaxis_title="Story Points",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white')
                )
                
                st.plotly_chart(fig_bar, use_container_width=True)
    
    # Sprint comparison if multiple sprints exist
    if len(all_sprints) > 1:
        st.markdown("### 📊 SPRINT COMPARISON")
        
        sprint_comparison_data = []
        for sprint in all_sprints[-5:]:  # Last 5 sprints
            sprint_progress = st.session_state.scrum_manager.get_sprint_progress(sprint['id'])
            sprint_comparison_data.append({
                'Sprint': sprint['name'],
                'Planned Points': sprint.get('total_points', 0),
                'Completed Points': sprint_progress['completed_points'],
                'Completion %': sprint_progress['progress_percentage']
            })
        
        if sprint_comparison_data:
            comparison_df = pd.DataFrame(sprint_comparison_data)
            
            fig_comparison = go.Figure()
            
            fig_comparison.add_trace(go.Bar(
                name='Planned Points',
                x=comparison_df['Sprint'],
                y=comparison_df['Planned Points'],
                marker_color='#3498db'
            ))
            
            fig_comparison.add_trace(go.Bar(
                name='Completed Points',
                x=comparison_df['Sprint'],
                y=comparison_df['Completed Points'],
                marker_color='#27ae60'
            ))
            
            fig_comparison.update_layout(
                title="Sprint Planned vs Completed Points",
                xaxis_title="Sprint",
                yaxis_title="Story Points",
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)

def show_team_performance():
    """Team performance analytics"""
    
    st.markdown("### 👥 TEAM PERFORMANCE MATRIX")
    
    all_stories = st.session_state.data_store.get_all_stories()
    
    if not all_stories:
        st.info("No story data available for team analysis.")
        return
    
    # Team member performance metrics
    team_stats = {}
    for story in all_stories:
        assignee = story.get('assignee')
        if assignee and assignee != 'Unassigned':
            if assignee not in team_stats:
                team_stats[assignee] = {
                    'total_stories': 0,
                    'completed_stories': 0,
                    'total_points': 0,
                    'completed_points': 0,
                    'in_progress': 0
                }
            
            team_stats[assignee]['total_stories'] += 1
            points = story.get('story_points', 0) or 0
            team_stats[assignee]['total_points'] += points
            
            if story.get('status') == 'Done':
                team_stats[assignee]['completed_stories'] += 1
                team_stats[assignee]['completed_points'] += points
            elif story.get('status') == 'In Progress':
                team_stats[assignee]['in_progress'] += 1
    
    if not team_stats:
        st.info("No team member data available. Assign stories to team members first.")
        return
    
    # Team performance overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Team Members", len(team_stats))
    
    with col2:
        total_team_stories = sum(stats['completed_stories'] for stats in team_stats.values())
        st.metric("Total Stories Completed", total_team_stories)
    
    with col3:
        total_team_points = sum(stats['completed_points'] for stats in team_stats.values())
        st.metric("Total Points Delivered", total_team_points)
    
    with col4:
        stories_in_progress = sum(stats['in_progress'] for stats in team_stats.values())
        st.metric("Stories In Progress", stories_in_progress)
    
    # Individual performance table
    st.markdown("### 📊 INDIVIDUAL PERFORMANCE")
    
    performance_data = []
    for member, stats in team_stats.items():
        completion_rate = (stats['completed_stories'] / stats['total_stories'] * 100) if stats['total_stories'] > 0 else 0
        avg_points_per_story = (stats['completed_points'] / stats['completed_stories']) if stats['completed_stories'] > 0 else 0
        
        performance_data.append({
            'Team Member': member,
            'Total Stories': stats['total_stories'],
            'Completed': stats['completed_stories'],
            'Completion Rate %': f"{completion_rate:.1f}%",
            'Total Points': stats['total_points'],
            'Completed Points': stats['completed_points'],
            'Avg Points/Story': f"{avg_points_per_story:.1f}",
            'In Progress': stats['in_progress']
        })
    
    performance_df = pd.DataFrame(performance_data)
    st.dataframe(performance_df, use_container_width=True)
    
    # Performance visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 COMPLETION RATES")
        
        fig_completion = go.Figure(data=[
            go.Bar(
                x=[data['Team Member'] for data in performance_data],
                y=[float(data['Completion Rate %'].replace('%', '')) for data in performance_data],
                marker_color='#00ff88'
            )
        ])
        
        fig_completion.update_layout(
            title="Story Completion Rate by Team Member",
            xaxis_title="Team Member",
            yaxis_title="Completion Rate (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_completion, use_container_width=True)
    
    with col2:
        st.markdown("### 📈 POINTS DELIVERED")
        
        fig_points = go.Figure(data=[
            go.Bar(
                x=[data['Team Member'] for data in performance_data],
                y=[data['Completed Points'] for data in performance_data],
                marker_color='#3498db'
            )
        ])
        
        fig_points.update_layout(
            title="Story Points Delivered by Team Member",
            xaxis_title="Team Member",
            yaxis_title="Story Points",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig_points, use_container_width=True)

def show_velocity_tracking():
    """Velocity tracking and trend analysis"""
    
    st.markdown("### 🎯 VELOCITY TRACKING DASHBOARD")
    
    all_sprints = st.session_state.data_store.get_all_sprints()
    completed_sprints = [s for s in all_sprints if s.get('status') == 'Completed']
    
    if len(completed_sprints) < 2:
        st.info("Need at least 2 completed sprints for velocity analysis.")
        return
    
    # Calculate velocity for each sprint
    velocity_data = []
    for sprint in completed_sprints:
        velocity_data.append({
            'Sprint': sprint['name'],
            'Planned Points': sprint.get('total_points', 0),
            'Completed Points': sprint.get('completed_points', 0),
            'End Date': sprint['end_date'],
            'Velocity': sprint.get('completed_points', 0)
        })
    
    # Sort by end date
    velocity_data.sort(key=lambda x: x['End Date'])
    
    # Velocity metrics
    velocities = [data['Velocity'] for data in velocity_data]
    avg_velocity = sum(velocities) / len(velocities)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Velocity", f"{avg_velocity:.1f} pts")
    
    with col2:
        if len(velocities) >= 2:
            trend = "↗️" if velocities[-1] > velocities[-2] else "↘️" if velocities[-1] < velocities[-2] else "→"
            st.metric("Trend", trend)
        else:
            st.metric("Trend", "—")
    
    with col3:
        min_velocity = min(velocities)
        max_velocity = max(velocities)
        st.metric("Velocity Range", f"{min_velocity}-{max_velocity}")
    
    with col4:
        if len(velocities) >= 3:
            recent_avg = sum(velocities[-3:]) / 3
            st.metric("Recent Avg (3 sprints)", f"{recent_avg:.1f}")
        else:
            st.metric("Recent Avg", f"{avg_velocity:.1f}")
    
    # Velocity trend chart
    st.markdown("### 📈 VELOCITY TREND ANALYSIS")
    
    fig_velocity = go.Figure()
    
    # Actual velocity
    fig_velocity.add_trace(go.Scatter(
        x=[data['Sprint'] for data in velocity_data],
        y=[data['Velocity'] for data in velocity_data],
        mode='lines+markers',
        name='Actual Velocity',
        line=dict(color='#00ff88', width=3),
        marker=dict(size=8)
    ))
    
    # Average line
    fig_velocity.add_trace(go.Scatter(
        x=[data['Sprint'] for data in velocity_data],
        y=[avg_velocity] * len(velocity_data),
        mode='lines',
        name=f'Average ({avg_velocity:.1f})',
        line=dict(color='#ffa726', dash='dash', width=2)
    ))
    
    fig_velocity.update_layout(
        title="Team Velocity Over Time",
        xaxis_title="Sprint",
        yaxis_title="Story Points",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        showlegend=True
    )
    
    st.plotly_chart(fig_velocity, use_container_width=True)
    
    # Planned vs Actual comparison
    st.markdown("### 📊 PLANNED VS ACTUAL DELIVERY")
    
    fig_comparison = go.Figure()
    
    fig_comparison.add_trace(go.Bar(
        name='Planned Points',
        x=[data['Sprint'] for data in velocity_data],
        y=[data['Planned Points'] for data in velocity_data],
        marker_color='#3498db'
    ))
    
    fig_comparison.add_trace(go.Bar(
        name='Delivered Points',
        x=[data['Sprint'] for data in velocity_data],
        y=[data['Completed Points'] for data in velocity_data],
        marker_color='#27ae60'
    ))
    
    fig_comparison.update_layout(
        title="Planned vs Delivered Story Points",
        xaxis_title="Sprint",
        yaxis_title="Story Points",
        barmode='group',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Velocity predictability
    st.markdown("### 🔮 VELOCITY PREDICTABILITY")
    
    if len(velocities) >= 3:
        # Calculate standard deviation
        import statistics
        velocity_std = statistics.stdev(velocities)
        predictability_score = max(0, 100 - (velocity_std / avg_velocity * 100))
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Velocity Standard Deviation", f"{velocity_std:.1f}")
            st.metric("Predictability Score", f"{predictability_score:.0f}%")
        
        with col2:
            # Predictability interpretation
            if predictability_score >= 80:
                st.success("🎯 Highly Predictable - Team velocity is very consistent")
            elif predictability_score >= 60:
                st.warning("⚡ Moderately Predictable - Some velocity variation")
            else:
                st.error("🌊 Unpredictable - High velocity variation, investigate causes")

def show_predictive_insights():
    """AI-powered predictive insights and recommendations"""
    
    st.markdown("### 🔮 PREDICTIVE NEURAL INSIGHTS")
    
    if not st.session_state.ai_client.check_connection():
        st.error("⚠️ AI Core offline - Cannot generate predictive insights")
        return
    
    # Sprint health prediction
    current_sprint = st.session_state.data_store.get_current_sprint()
    
    if current_sprint:
        st.markdown("### 🏃‍♂️ CURRENT SPRINT PREDICTIONS")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Sprint Completion Prediction", use_container_width=True):
                with st.spinner("Analyzing sprint trajectory..."):
                    analysis = st.session_state.ai_client.analyze_sprint_health()
                    if analysis:
                        st.success("📊 Analysis Complete!")
                        st.write(analysis)
        
        with col2:
            if st.button("⚠️ Risk Assessment", use_container_width=True):
                with st.spinner("Identifying potential risks..."):
                    bottlenecks = st.session_state.ai_client.detect_bottlenecks()
                    if bottlenecks:
                        st.success("🔍 Risk Assessment Complete!")
                        st.write(bottlenecks)
    
    # Velocity predictions
    st.markdown("### 🚀 VELOCITY PREDICTIONS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📈 Next Sprint Velocity", use_container_width=True):
            with st.spinner("Calculating velocity predictions..."):
                prediction = st.session_state.ai_client.predict_velocity()
                if prediction:
                    st.success("🎯 Velocity Prediction Ready!")
                    st.write(prediction)
    
    with col2:
        if st.button("📊 Capacity Optimization", use_container_width=True):
            with st.spinner("Analyzing capacity optimization..."):
                # Mock capacity analysis - replace with actual AI call
                capacity_analysis = generate_capacity_analysis()
                if capacity_analysis:
                    st.success("⚡ Optimization Analysis Complete!")
                    st.write(capacity_analysis)
    
    # Team performance predictions
    st.markdown("### 👥 TEAM PERFORMANCE INSIGHTS")
    
    if st.button("🧠 Generate Team Insights", use_container_width=True):
        with st.spinner("Analyzing team performance patterns..."):
            team_insights = generate_team_insights()
            if team_insights:
                st.success("👥 Team Analysis Complete!")
                st.write(team_insights)
    
    # Release planning insights
    st.markdown("### 🎯 RELEASE PLANNING INSIGHTS")
    
    all_stories = st.session_state.data_store.get_all_stories()
    backlog_stories = [s for s in all_stories if s.get('status') == 'Backlog']
    
    if backlog_stories:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📅 Release Date Prediction", use_container_width=True):
                with st.spinner("Calculating release timeline..."):
                    release_prediction = generate_release_prediction(backlog_stories)
                    if release_prediction:
                        st.success("📅 Release Prediction Ready!")
                        st.write(release_prediction)
        
        with col2:
            if st.button("🎯 Feature Prioritization", use_container_width=True):
                with st.spinner("Analyzing feature priorities..."):
                    prioritization = generate_feature_prioritization(backlog_stories)
                    if prioritization:
                        st.success("🎯 Prioritization Analysis Complete!")
                        st.write(prioritization)

def generate_capacity_analysis():
    """Generate capacity optimization analysis"""
    # Get team and sprint data
    current_sprint = st.session_state.data_store.get_current_sprint()
    all_sprints = st.session_state.data_store.get_all_sprints()
    
    if not current_sprint:
        return "No active sprint for capacity analysis."
    
    completed_sprints = [s for s in all_sprints if s.get('status') == 'Completed']
    
    if len(completed_sprints) < 2:
        return "Need more sprint history for capacity analysis."
    
    # Calculate average utilization
    total_capacity = sum(s.get('capacity', 0) for s in completed_sprints)
    total_delivered = sum(s.get('completed_points', 0) for s in completed_sprints)
    avg_utilization = (total_delivered / total_capacity * 100) if total_capacity > 0 else 0
    
    return f"""
    ## ⚡ Capacity Optimization Analysis
    
    **Current Sprint Capacity:** {current_sprint.get('capacity', 0)} story points
    **Historical Average Utilization:** {avg_utilization:.1f}%
    
    ### Recommendations:
    
    **Optimal Capacity Range:** {current_sprint.get('capacity', 0) * 0.8:.0f} - {current_sprint.get('capacity', 0) * 0.9:.0f} story points
    
    **Key Insights:**
    - Team typically delivers {avg_utilization:.0f}% of planned capacity
    - Consider adjusting sprint planning to account for this utilization rate
    - Buffer 10-20% capacity for unexpected work and improvements
    
    **Action Items:**
    - Review historical sprint data for capacity planning
    - Identify factors causing capacity underutilization
    - Implement capacity buffers for sustainable pace
    """

def generate_team_insights():
    """Generate team performance insights"""
    all_stories = st.session_state.data_store.get_all_stories()
    
    # Analyze team distribution
    team_members = set()
    for story in all_stories:
        assignee = story.get('assignee')
        if assignee and assignee != 'Unassigned':
            team_members.add(assignee)
    
    completed_stories = [s for s in all_stories if s.get('status') == 'Done']
    
    return f"""
    ## 👥 Team Performance Insights
    
    **Active Team Members:** {len(team_members)}
    **Total Stories Completed:** {len(completed_stories)}
    
    ### Performance Patterns:
    
    **Team Collaboration:**
    - {len(team_members)} active contributors identified
    - Story distribution appears {"balanced" if len(team_members) > 2 else "concentrated"}
    
    **Completion Trends:**
    - Team has delivered {len(completed_stories)} stories successfully
    - Average story complexity suggests good estimation practices
    
    ### Recommendations:
    
    **Team Development:**
    - Continue current collaboration patterns
    - Consider pair programming for knowledge sharing
    - Implement code review processes for quality
    
    **Performance Optimization:**
    - Track individual velocity for capacity planning
    - Identify skill development opportunities
    - Encourage cross-functional collaboration
    """

def generate_release_prediction(backlog_stories):
    """Generate release timeline prediction"""
    # Calculate backlog size
    total_backlog_points = sum(s.get('story_points', 3) for s in backlog_stories if s.get('story_points'))
    estimated_stories = len([s for s in backlog_stories if not s.get('story_points')])
    estimated_points = estimated_stories * 3  # Average estimation
    
    total_points = total_backlog_points + estimated_points
    
    # Get velocity data
    velocity_data = st.session_state.data_store.get_velocity_history()
    if velocity_data:
        avg_velocity = sum(v['completed_points'] for v in velocity_data) / len(velocity_data)
    else:
        avg_velocity = 20  # Default assumption
    
    # Calculate sprints needed
    sprints_needed = (total_points / avg_velocity) if avg_velocity > 0 else 0
    weeks_needed = sprints_needed * 2  # Assuming 2-week sprints
    
    estimated_date = datetime.now() + timedelta(weeks=weeks_needed)
    
    return f"""
    ## 📅 Release Timeline Prediction
    
    **Backlog Analysis:**
    - Total Stories: {len(backlog_stories)}
    - Estimated Story Points: {total_points:.0f}
    - Stories Needing Estimation: {estimated_stories}
    
    **Velocity Analysis:**
    - Average Team Velocity: {avg_velocity:.1f} points/sprint
    - Sprints Required: {sprints_needed:.1f}
    - Estimated Duration: {weeks_needed:.0f} weeks
    
    **Predicted Release Date:** {estimated_date.strftime('%Y-%m-%d')}
    
    ### Confidence Factors:
    - {"High" if len(velocity_data) >= 3 else "Medium" if len(velocity_data) >= 1 else "Low"} confidence based on velocity history
    - Assumes current team capacity and sprint duration
    - Does not account for scope changes or new requirements
    
    ### Recommendations:
    - Estimate remaining stories for better accuracy
    - Consider scope prioritization for earlier releases
    - Plan for 10-20% buffer in timeline estimates
    """

def generate_feature_prioritization(backlog_stories):
    """Generate feature prioritization recommendations"""
    # Analyze story priorities
    priority_counts = {}
    for story in backlog_stories:
        priority = story.get('priority', 'Medium')
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    high_priority = priority_counts.get('Critical', 0) + priority_counts.get('High', 0)
    total_stories = len(backlog_stories)
    
    return f"""
    ## 🎯 Feature Prioritization Analysis
    
    **Backlog Composition:**
    - Critical: {priority_counts.get('Critical', 0)} stories
    - High: {priority_counts.get('High', 0)} stories  
    - Medium: {priority_counts.get('Medium', 0)} stories
    - Low: {priority_counts.get('Low', 0)} stories
    
    **Priority Distribution:**
    - High Priority Items: {high_priority} ({high_priority/total_stories*100:.0f}% of backlog)
    - Immediate Focus: Next {min(high_priority, 10)} stories
    
    ### Prioritization Strategy:
    
    **Sprint 1-2 Focus:**
    - All Critical priority items
    - High-value, low-effort stories
    - Technical debt that blocks other work
    
    **Sprint 3-4 Focus:**
    - Remaining High priority items
    - Dependencies for future features
    - User experience improvements
    
    **Future Sprints:**
    - Medium priority feature enhancements
    - Nice-to-have functionality
    - Experimental features
    
    ### Recommendations:
    - Review and update story priorities regularly
    - Consider business value vs technical effort
    - Maintain 70/20/10 split: Features/Tech Debt/Innovation
    """
