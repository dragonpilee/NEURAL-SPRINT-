import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import json

def show_retrospective():
    """Sprint retrospective interface"""
    
    st.markdown("## 🔄 NEURAL RETROSPECTIVE MATRIX")
    
    tab1, tab2, tab3 = st.tabs(["🔍 Current Retrospective", "📊 Historical Analysis", "🎯 Action Tracking"])
    
    with tab1:
        show_current_retrospective()
    
    with tab2:
        show_historical_analysis()
    
    with tab3:
        show_action_tracking()

def show_current_retrospective():
    """Current sprint retrospective"""
    
    # Get completed or current sprint for retrospective
    current_sprint = st.session_state.data_store.get_current_sprint()
    all_sprints = st.session_state.data_store.get_all_sprints()
    
    # Sprint selection
    completed_sprints = [s for s in all_sprints if s.get('status') == 'Completed']
    
    if current_sprint:
        sprint_options = [current_sprint] + completed_sprints
    else:
        sprint_options = completed_sprints
    
    if not sprint_options:
        st.info("No sprints available for retrospective. Complete a sprint first.")
        return
    
    selected_sprint = st.selectbox(
        "Select Sprint for Retrospective",
        options=sprint_options,
        format_func=lambda x: f"{x['name']} ({x.get('status', 'Unknown')})",
        index=0
    )
    
    if not selected_sprint:
        return
    
    st.markdown(f"### 🔍 Retrospective: {selected_sprint['name']}")
    
    # Sprint summary
    progress = st.session_state.scrum_manager.get_sprint_progress(selected_sprint['id'])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Sprint Progress", f"{progress['progress_percentage']}%")
    with col2:
        st.metric("Completed Points", progress['completed_points'])
    with col3:
        st.metric("Total Stories", progress['stories_count'])
    with col4:
        st.metric("Sprint Duration", f"{selected_sprint.get('duration_weeks', 2)} weeks")
    
    # Retrospective data collection
    retro_key = f"retro_{selected_sprint['id']}"
    if retro_key not in st.session_state:
        st.session_state[retro_key] = {
            "sprint_id": selected_sprint['id'],
            "sprint_name": selected_sprint['name'],
            "what_went_well": [],
            "what_could_improve": [],
            "action_items": [],
            "team_mood": 3,
            "created_date": datetime.now().isoformat()
        }
    
    retro_data = st.session_state[retro_key]
    
    # Three columns retrospective format
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 😊 WHAT WENT WELL")
        
        # Add new positive item
        new_positive = st.text_input("Add positive feedback", key="new_positive")
        if st.button("➕ Add", key="add_positive") and new_positive.strip():
            retro_data['what_went_well'].append({
                "text": new_positive.strip(),
                "votes": 0,
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()
        
        # Display positive items
        for i, item in enumerate(retro_data['what_went_well']):
            with st.container():
                col_text, col_vote, col_delete = st.columns([3, 1, 1])
                with col_text:
                    st.write(f"• {item['text']}")
                with col_vote:
                    if st.button("👍", key=f"vote_pos_{i}"):
                        retro_data['what_went_well'][i]['votes'] += 1
                        st.rerun()
                    st.write(f"{item['votes']}")
                with col_delete:
                    if st.button("🗑️", key=f"del_pos_{i}"):
                        retro_data['what_went_well'].pop(i)
                        st.rerun()
    
    with col2:
        st.markdown("#### 🤔 WHAT COULD IMPROVE")
        
        # Add new improvement item
        new_improvement = st.text_input("Add improvement suggestion", key="new_improvement")
        if st.button("➕ Add", key="add_improvement") and new_improvement.strip():
            retro_data['what_could_improve'].append({
                "text": new_improvement.strip(),
                "votes": 0,
                "timestamp": datetime.now().isoformat()
            })
            st.rerun()
        
        # Display improvement items
        for i, item in enumerate(retro_data['what_could_improve']):
            with st.container():
                col_text, col_vote, col_delete = st.columns([3, 1, 1])
                with col_text:
                    st.write(f"• {item['text']}")
                with col_vote:
                    if st.button("👍", key=f"vote_imp_{i}"):
                        retro_data['what_could_improve'][i]['votes'] += 1
                        st.rerun()
                    st.write(f"{item['votes']}")
                with col_delete:
                    if st.button("🗑️", key=f"del_imp_{i}"):
                        retro_data['what_could_improve'].pop(i)
                        st.rerun()
    
    with col3:
        st.markdown("#### 🎯 ACTION ITEMS")
        
        # Add new action item
        new_action = st.text_input("Add action item", key="new_action")
        action_owner = st.text_input("Assign to", key="action_owner")
        
        if st.button("➕ Add Action", key="add_action") and new_action.strip():
            retro_data['action_items'].append({
                "text": new_action.strip(),
                "owner": action_owner.strip() if action_owner.strip() else "Unassigned",
                "status": "Open",
                "created_date": datetime.now().isoformat()
            })
            st.rerun()
        
        # Display action items
        for i, item in enumerate(retro_data['action_items']):
            with st.container():
                col_text, col_status, col_delete = st.columns([2, 1, 1])
                with col_text:
                    st.write(f"• {item['text']}")
                    st.caption(f"Owner: {item['owner']}")
                with col_status:
                    new_status = st.selectbox("", 
                                            ["Open", "In Progress", "Done"], 
                                            index=["Open", "In Progress", "Done"].index(item['status']),
                                            key=f"status_{i}")
                    if new_status != item['status']:
                        retro_data['action_items'][i]['status'] = new_status
                        st.rerun()
                with col_delete:
                    if st.button("🗑️", key=f"del_action_{i}"):
                        retro_data['action_items'].pop(i)
                        st.rerun()
    
    # Team mood and additional feedback
    st.markdown("### 🌡️ TEAM SENTIMENT")
    
    col1, col2 = st.columns(2)
    
    with col1:
        team_mood = st.slider("Overall Team Mood", 
                            min_value=1, max_value=5, 
                            value=retro_data['team_mood'],
                            help="1 = Very Dissatisfied, 5 = Very Satisfied")
        if team_mood != retro_data['team_mood']:
            retro_data['team_mood'] = team_mood
    
    with col2:
        mood_emoji = ["😞", "😕", "😐", "😊", "😄"][team_mood - 1]
        mood_text = ["Very Dissatisfied", "Dissatisfied", "Neutral", "Satisfied", "Very Satisfied"][team_mood - 1]
        st.markdown(f"### {mood_emoji} {mood_text}")
    
    # AI-powered insights
    if st.session_state.ai_client.check_connection():
        st.markdown("### 🤖 AI RETROSPECTIVE INSIGHTS")
        
        if st.button("🧠 Generate AI Analysis", use_container_width=True):
            with st.spinner("Analyzing retrospective data..."):
                # Prepare data for AI analysis
                analysis_data = {
                    "sprint": selected_sprint,
                    "retrospective": retro_data,
                    "sprint_progress": progress
                }
                
                insights = st.session_state.ai_client.generate_retrospective_insights(analysis_data)
                if insights:
                    st.success("🎯 AI Analysis Complete!")
                    with st.expander("📋 AI Insights", expanded=True):
                        st.markdown(insights)
                    
                    # Save insights
                    retro_data['ai_insights'] = insights
    
    # Save retrospective
    if st.button("💾 Save Retrospective", use_container_width=True):
        if save_retrospective_data(retro_data):
            st.success("✅ Retrospective saved successfully!")
        else:
            st.error("❌ Failed to save retrospective")

def show_historical_analysis():
    """Historical retrospective analysis"""
    
    st.markdown("### 📊 HISTORICAL RETROSPECTIVE ANALYSIS")
    
    # Load all retrospectives
    retrospectives = load_all_retrospectives()
    
    if not retrospectives:
        st.info("No retrospective data available yet.")
        return
    
    # Sort by date
    retrospectives.sort(key=lambda x: x.get('created_date', ''), reverse=True)
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Retrospectives", len(retrospectives))
    
    with col2:
        avg_mood = sum(r.get('team_mood', 3) for r in retrospectives) / len(retrospectives)
        st.metric("Average Team Mood", f"{avg_mood:.1f}/5")
    
    with col3:
        total_actions = sum(len(r.get('action_items', [])) for r in retrospectives)
        st.metric("Total Action Items", total_actions)
    
    with col4:
        completed_actions = sum(len([a for a in r.get('action_items', []) if a.get('status') == 'Done']) 
                               for r in retrospectives)
        completion_rate = (completed_actions / total_actions * 100) if total_actions > 0 else 0
        st.metric("Action Completion Rate", f"{completion_rate:.1f}%")
    
    # Team mood trend
    if len(retrospectives) > 1:
        st.markdown("### 📈 TEAM MOOD TREND")
        
        mood_data = []
        for retro in reversed(retrospectives[-10:]):  # Last 10 retrospectives
            mood_data.append({
                "Sprint": retro['sprint_name'],
                "Team Mood": retro.get('team_mood', 3),
                "Date": retro.get('created_date', '')[:10]
            })
        
        if mood_data:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[d['Sprint'] for d in mood_data],
                y=[d['Team Mood'] for d in mood_data],
                mode='lines+markers',
                name='Team Mood',
                line=dict(color='#00ff88', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Team Mood Over Time",
                xaxis_title="Sprint",
                yaxis_title="Team Mood (1-5)",
                yaxis=dict(range=[1, 5]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Common themes analysis
    st.markdown("### 🔍 COMMON THEMES")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 😊 Top Positive Themes")
        positive_themes = extract_themes([item['text'] for retro in retrospectives 
                                        for item in retro.get('what_went_well', [])])
        for theme, count in positive_themes[:5]:
            st.write(f"• {theme} ({count} mentions)")
    
    with col2:
        st.markdown("#### 🤔 Top Improvement Areas")
        improvement_themes = extract_themes([item['text'] for retro in retrospectives 
                                           for item in retro.get('what_could_improve', [])])
        for theme, count in improvement_themes[:5]:
            st.write(f"• {theme} ({count} mentions)")
    
    # Retrospective details
    st.markdown("### 📋 RETROSPECTIVE HISTORY")
    
    for retro in retrospectives[:5]:  # Show last 5
        with st.expander(f"🔍 {retro['sprint_name']} - {retro.get('created_date', '')[:10]}"):
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**What Went Well:**")
                for item in retro.get('what_went_well', []):
                    st.write(f"• {item['text']} ({item.get('votes', 0)} votes)")
            
            with col2:
                st.markdown("**What Could Improve:**")
                for item in retro.get('what_could_improve', []):
                    st.write(f"• {item['text']} ({item.get('votes', 0)} votes)")
            
            with col3:
                st.markdown("**Action Items:**")
                for item in retro.get('action_items', []):
                    status_emoji = {"Open": "🔵", "In Progress": "🟡", "Done": "✅"}
                    emoji = status_emoji.get(item['status'], "🔵")
                    st.write(f"{emoji} {item['text']} ({item['owner']})")
            
            # AI insights if available
            if retro.get('ai_insights'):
                st.markdown("**AI Insights:**")
                st.write(retro['ai_insights'][:200] + "..." if len(retro['ai_insights']) > 200 else retro['ai_insights'])

def show_action_tracking():
    """Action item tracking across retrospectives"""
    
    st.markdown("### 🎯 ACTION ITEM TRACKING")
    
    # Load all retrospectives
    retrospectives = load_all_retrospectives()
    
    if not retrospectives:
        st.info("No action items to track yet.")
        return
    
    # Collect all action items
    all_actions = []
    for retro in retrospectives:
        for action in retro.get('action_items', []):
            all_actions.append({
                **action,
                "sprint_name": retro['sprint_name'],
                "sprint_id": retro['sprint_id'],
                "retro_date": retro.get('created_date', '')[:10]
            })
    
    if not all_actions:
        st.info("No action items found.")
        return
    
    # Action status summary
    col1, col2, col3 = st.columns(3)
    
    open_actions = [a for a in all_actions if a['status'] == 'Open']
    in_progress_actions = [a for a in all_actions if a['status'] == 'In Progress']
    done_actions = [a for a in all_actions if a['status'] == 'Done']
    
    with col1:
        st.metric("🔵 Open Actions", len(open_actions))
    with col2:
        st.metric("🟡 In Progress", len(in_progress_actions))
    with col3:
        st.metric("✅ Completed", len(done_actions))
    
    # Action status distribution
    if all_actions:
        status_counts = {"Open": len(open_actions), "In Progress": len(in_progress_actions), "Done": len(done_actions)}
        
        fig = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Action Items Status Distribution",
            color_discrete_map={"Open": "#3498db", "In Progress": "#f39c12", "Done": "#27ae60"}
        )
        
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Filter and display actions
    col1, col2 = st.columns(2)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", ["All", "Open", "In Progress", "Done"])
    
    with col2:
        owner_filter = st.selectbox("Filter by Owner", 
                                   ["All"] + list(set(a['owner'] for a in all_actions if a['owner'] != 'Unassigned')))
    
    # Apply filters
    filtered_actions = all_actions
    if status_filter != "All":
        filtered_actions = [a for a in filtered_actions if a['status'] == status_filter]
    if owner_filter != "All":
        filtered_actions = [a for a in filtered_actions if a['owner'] == owner_filter]
    
    # Display filtered actions
    st.markdown(f"### 📋 ACTION ITEMS ({len(filtered_actions)} items)")
    
    for action in filtered_actions:
        status_color = {"Open": "#3498db", "In Progress": "#f39c12", "Done": "#27ae60"}.get(action['status'], "#666")
        
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{action['text']}**")
                st.caption(f"From: {action['sprint_name']} ({action['retro_date']})")
            
            with col2:
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{action['status']}</span>", 
                          unsafe_allow_html=True)
            
            with col3:
                st.write(f"👤 {action['owner']}")
            
            with col4:
                # Quick status update
                new_status = st.selectbox("", 
                                        ["Open", "In Progress", "Done"],
                                        index=["Open", "In Progress", "Done"].index(action['status']),
                                        key=f"update_status_{action['text'][:10]}")
                if new_status != action['status']:
                    update_action_status(action, new_status)
                    st.rerun()
            
            st.markdown("---")
    
    # Action item analytics
    if len(all_actions) > 5:
        st.markdown("### 📊 ACTION ITEM ANALYTICS")
        
        # Owner performance
        owner_stats = {}
        for action in all_actions:
            owner = action['owner']
            if owner not in owner_stats:
                owner_stats[owner] = {"total": 0, "completed": 0}
            owner_stats[owner]["total"] += 1
            if action['status'] == "Done":
                owner_stats[owner]["completed"] += 1
        
        st.markdown("#### 👥 Owner Performance")
        for owner, stats in owner_stats.items():
            if stats["total"] > 0:
                completion_rate = stats["completed"] / stats["total"] * 100
                st.write(f"**{owner}:** {stats['completed']}/{stats['total']} completed ({completion_rate:.0f}%)")

def save_retrospective_data(retro_data):
    """Save retrospective data to file"""
    try:
        retros_file = "data/retrospectives.json"
        
        # Load existing retrospectives
        existing_retros = []
        try:
            with open(retros_file, 'r', encoding='utf-8') as f:
                existing_retros = json.load(f)
        except FileNotFoundError:
            pass
        
        # Update or add new retrospective
        updated = False
        for i, retro in enumerate(existing_retros):
            if retro['sprint_id'] == retro_data['sprint_id']:
                existing_retros[i] = retro_data
                updated = True
                break
        
        if not updated:
            existing_retros.append(retro_data)
        
        # Save back to file
        with open(retros_file, 'w', encoding='utf-8') as f:
            json.dump(existing_retros, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving retrospective data: {str(e)}")
        return False

def load_all_retrospectives():
    """Load all retrospective data"""
    try:
        retros_file = "data/retrospectives.json"
        with open(retros_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        st.error(f"Error loading retrospective data: {str(e)}")
        return []

def extract_themes(texts):
    """Extract common themes from text list"""
    # Simple keyword-based theme extraction
    keywords = ['communication', 'testing', 'deployment', 'planning', 'collaboration', 
                'documentation', 'process', 'tools', 'quality', 'velocity', 'blockers']
    
    theme_counts = {}
    for text in texts:
        text_lower = text.lower()
        for keyword in keywords:
            if keyword in text_lower:
                theme_counts[keyword] = theme_counts.get(keyword, 0) + 1
    
    # Sort by frequency
    return sorted(theme_counts.items(), key=lambda x: x[1], reverse=True)

def update_action_status(action, new_status):
    """Update action item status in stored data"""
    # This would update the action status in the stored retrospective data
    # Implementation depends on how the data is structured and stored
    pass
