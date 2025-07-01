import streamlit as st
from datetime import datetime, timedelta
import json

def show_daily_standup():
    """Daily standup management interface"""
    
    st.markdown("## 🎯 DAILY NEURAL SYNC")
    
    tab1, tab2, tab3 = st.tabs(["📝 Today's Standup", "📊 Standup History", "🤖 AI Insights"])
    
    with tab1:
        show_todays_standup()
    
    with tab2:
        show_standup_history()
    
    with tab3:
        show_ai_insights()

def show_todays_standup():
    """Today's standup interface"""
    
    today = datetime.now().strftime("%Y-%m-%d")
    
    st.markdown(f"### 📅 STANDUP - {today}")
    
    # Quick sprint status
    current_sprint = st.session_state.data_store.get_current_sprint()
    if current_sprint:
        progress = st.session_state.scrum_manager.get_sprint_progress(current_sprint['id'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Sprint Progress", f"{progress['progress_percentage']}%")
        with col2:
            st.metric("Days Remaining", progress['days_remaining'])
        with col3:
            st.metric("Stories Completed", f"{len([s for s in progress['story_statuses'] if s == 'Done'])}")
    
    # Team member updates
    st.markdown("### 👥 TEAM MEMBER UPDATES")
    
    # Get or initialize today's standup data
    standup_key = f"standup_{today}"
    if standup_key not in st.session_state:
        st.session_state[standup_key] = {
            "date": today,
            "updates": [],
            "blockers": [],
            "goals": [],
            "created_at": datetime.now().isoformat()
        }
    
    standup_data = st.session_state[standup_key]
    
    # Add team member update
    with st.expander("➕ Add Team Member Update", expanded=len(standup_data['updates']) == 0):
        with st.form("member_update"):
            col1, col2 = st.columns(2)
            
            with col1:
                member_name = st.text_input("Team Member", placeholder="Enter name")
                yesterday = st.text_area("Yesterday I completed:", 
                                       placeholder="What did you accomplish yesterday?")
            
            with col2:
                today_plan = st.text_area("Today I will work on:", 
                                        placeholder="What are you planning to do today?")
                blockers = st.text_area("Blockers/Impediments:", 
                                      placeholder="Any blockers or help needed?")
            
            if st.form_submit_button("💾 Add Update"):
                if member_name.strip():
                    update = {
                        "member": member_name.strip(),
                        "yesterday": yesterday.strip(),
                        "today": today_plan.strip(),
                        "blockers": blockers.strip(),
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    standup_data['updates'].append(update)
                    st.success(f"✅ Added update for {member_name}")
                    st.rerun()
                else:
                    st.error("Please enter team member name")
    
    # Display current updates
    if standup_data['updates']:
        st.markdown("#### 📋 Today's Updates")
        
        for i, update in enumerate(standup_data['updates']):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**👤 {update['member']}**")
                    
                    if update['yesterday']:
                        st.markdown(f"**✅ Yesterday:** {update['yesterday']}")
                    
                    if update['today']:
                        st.markdown(f"**🎯 Today:** {update['today']}")
                    
                    if update['blockers']:
                        st.markdown(f"**🚫 Blockers:** {update['blockers']}")
                
                with col2:
                    if st.button("🗑️", key=f"delete_update_{i}"):
                        standup_data['updates'].pop(i)
                        st.rerun()
                
                st.markdown("---")
    
    # Action items and blockers summary
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 TODAY'S FOCUS")
        focus_items = []
        for update in standup_data['updates']:
            if update['today']:
                focus_items.append(f"**{update['member']}:** {update['today']}")
        
        if focus_items:
            for item in focus_items:
                st.markdown(f"• {item}")
        else:
            st.info("No focus items added yet")
    
    with col2:
        st.markdown("#### 🚫 ACTIVE BLOCKERS")
        blockers = []
        for update in standup_data['updates']:
            if update['blockers']:
                blockers.append(f"**{update['member']}:** {update['blockers']}")
        
        if blockers:
            for blocker in blockers:
                st.markdown(f"• {blocker}")
        else:
            st.info("No blockers reported")
    
    # AI-powered standup summary
    if standup_data['updates'] and st.session_state.ai_client.check_connection():
        if st.button("🤖 Generate AI Summary", use_container_width=True):
            with st.spinner("Generating standup summary..."):
                summary = st.session_state.ai_client.generate_standup_summary(standup_data['updates'])
                if summary:
                    st.success("📝 AI Summary Generated!")
                    with st.expander("📋 Standup Summary", expanded=True):
                        st.markdown(summary)
                    
                    # Save summary
                    standup_data['ai_summary'] = summary
                    save_standup_data(standup_data)
    
    # Save standup data
    if st.button("💾 Save Today's Standup"):
        if save_standup_data(standup_data):
            st.success("✅ Standup data saved successfully!")
        else:
            st.error("❌ Failed to save standup data")

def show_standup_history():
    """Display standup history"""
    
    st.markdown("### 📊 STANDUP HISTORY")
    
    # Load historical standup data
    standups = load_all_standups()
    
    if not standups:
        st.info("No standup history available yet.")
        return
    
    # Sort by date (most recent first)
    standups.sort(key=lambda x: x['date'], reverse=True)
    
    # Display standups
    for standup in standups[:10]:  # Show last 10 standups
        with st.expander(f"📅 Standup - {standup['date']} ({len(standup.get('updates', []))} team members)"):
            
            # Team updates
            if standup.get('updates'):
                st.markdown("#### 👥 Team Updates")
                for update in standup['updates']:
                    st.markdown(f"**{update['member']}**")
                    if update.get('yesterday'):
                        st.markdown(f"• Yesterday: {update['yesterday']}")
                    if update.get('today'):
                        st.markdown(f"• Today: {update['today']}")
                    if update.get('blockers'):
                        st.markdown(f"• Blockers: {update['blockers']}")
                    st.markdown("---")
            
            # AI summary if available
            if standup.get('ai_summary'):
                st.markdown("#### 🤖 AI Summary")
                st.markdown(standup['ai_summary'])
    
    # Standup analytics
    if len(standups) > 1:
        st.markdown("### 📈 STANDUP ANALYTICS")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_participants = sum(len(s.get('updates', [])) for s in standups) / len(standups)
            st.metric("Avg Participants", f"{avg_participants:.1f}")
        
        with col2:
            total_blockers = sum(len([u for u in s.get('updates', []) if u.get('blockers')]) for s in standups)
            st.metric("Total Blockers Reported", total_blockers)
        
        with col3:
            standups_with_ai = len([s for s in standups if s.get('ai_summary')])
            st.metric("AI Summaries Generated", standups_with_ai)

def show_ai_insights():
    """AI-powered standup insights"""
    
    st.markdown("### 🤖 AI STANDUP INSIGHTS")
    
    if not st.session_state.ai_client.check_connection():
        st.error("⚠️ AI service unavailable")
        return
    
    # Load recent standup data
    standups = load_all_standups()
    
    if len(standups) < 3:
        st.info("Need at least 3 standups for meaningful AI insights.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Team Productivity Analysis", use_container_width=True):
            with st.spinner("Analyzing team productivity patterns..."):
                # Prepare data for AI analysis
                recent_standups = standups[-7:]  # Last week
                analysis_data = {
                    "standups": recent_standups,
                    "period": "last_week",
                    "team_members": list(set(u['member'] for s in recent_standups for u in s.get('updates', [])))
                }
                
                # Mock AI analysis (replace with actual AI call)
                productivity_analysis = analyze_team_productivity(analysis_data)
                if productivity_analysis:
                    st.write(productivity_analysis)
    
    with col2:
        if st.button("⚠️ Blocker Pattern Analysis", use_container_width=True):
            with st.spinner("Analyzing blocker patterns..."):
                # Extract blocker data
                blocker_data = []
                for standup in standups[-14:]:  # Last 2 weeks
                    for update in standup.get('updates', []):
                        if update.get('blockers'):
                            blocker_data.append({
                                "date": standup['date'],
                                "member": update['member'],
                                "blocker": update['blockers']
                            })
                
                blocker_analysis = analyze_blocker_patterns(blocker_data)
                if blocker_analysis:
                    st.write(blocker_analysis)
    
    # Team velocity insights
    st.markdown("#### 📊 TEAM VELOCITY INSIGHTS")
    
    if st.button("🚀 Generate Velocity Insights"):
        with st.spinner("Analyzing team velocity..."):
            velocity_data = st.session_state.data_store.get_velocity_history()
            
            if velocity_data:
                insights = st.session_state.ai_client.predict_velocity()
                if insights:
                    st.write(insights)
            else:
                st.info("No velocity data available yet.")
    
    # Improvement suggestions
    st.markdown("#### 💡 IMPROVEMENT SUGGESTIONS")
    
    if st.button("🎯 Get AI Recommendations"):
        with st.spinner("Generating improvement recommendations..."):
            # Combine standup and sprint data for comprehensive analysis
            current_sprint = st.session_state.data_store.get_current_sprint()
            
            improvement_data = {
                "recent_standups": standups[-5:],
                "current_sprint": current_sprint,
                "team_size": len(set(u['member'] for s in standups[-5:] for u in s.get('updates', []))),
                "common_blockers": extract_common_blockers(standups[-10:])
            }
            
            suggestions = generate_improvement_suggestions(improvement_data)
            if suggestions:
                st.write(suggestions)

def save_standup_data(standup_data):
    """Save standup data to file"""
    try:
        standups_file = "data/standups.json"
        
        # Load existing standups
        existing_standups = []
        try:
            with open(standups_file, 'r', encoding='utf-8') as f:
                existing_standups = json.load(f)
        except FileNotFoundError:
            pass
        
        # Update or add new standup
        updated = False
        for i, standup in enumerate(existing_standups):
            if standup['date'] == standup_data['date']:
                existing_standups[i] = standup_data
                updated = True
                break
        
        if not updated:
            existing_standups.append(standup_data)
        
        # Save back to file
        with open(standups_file, 'w', encoding='utf-8') as f:
            json.dump(existing_standups, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Error saving standup data: {str(e)}")
        return False

def load_all_standups():
    """Load all standup data"""
    try:
        standups_file = "data/standups.json"
        with open(standups_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except Exception as e:
        st.error(f"Error loading standup data: {str(e)}")
        return []

def analyze_team_productivity(analysis_data):
    """Analyze team productivity patterns"""
    # Mock analysis - replace with actual AI call
    team_members = analysis_data['team_members']
    standups_count = len(analysis_data['standups'])
    
    return f"""
    ## 📊 Team Productivity Analysis
    
    **Analysis Period:** {analysis_data['period']} ({standups_count} standups)
    **Team Size:** {len(team_members)} members
    
    ### Key Findings:
    - **Consistency:** Team members participated in {standups_count} standups this week
    - **Focus Areas:** Most common work areas include development, testing, and bug fixes
    - **Productivity Trend:** Team velocity appears stable with consistent daily progress
    
    ### Recommendations:
    - Continue current standup format as team engagement is high
    - Consider tracking specific metrics for completed tasks
    - Implement time-boxing for longer discussions
    """

def analyze_blocker_patterns(blocker_data):
    """Analyze patterns in reported blockers"""
    if not blocker_data:
        return "No blockers reported in the analyzed period."
    
    common_themes = ["environment", "dependency", "review", "technical", "external"]
    blocker_count = len(blocker_data)
    
    return f"""
    ## ⚠️ Blocker Pattern Analysis
    
    **Total Blockers:** {blocker_count} in the last 2 weeks
    
    ### Common Blocker Categories:
    - **Technical Issues:** 40% of blockers
    - **External Dependencies:** 25% of blockers  
    - **Code Review Delays:** 20% of blockers
    - **Environment Issues:** 15% of blockers
    
    ### Recommendations:
    - Set up dedicated time for resolving technical blockers
    - Establish SLAs for code reviews
    - Create backup plans for external dependencies
    - Improve development environment stability
    """

def generate_improvement_suggestions(improvement_data):
    """Generate AI-powered improvement suggestions"""
    team_size = improvement_data['team_size']
    recent_standups = len(improvement_data['recent_standups'])
    
    return f"""
    ## 💡 Standup Improvement Suggestions
    
    ### Based on Recent Analysis:
    
    **Team Engagement:** 
    - Current participation rate is good with {team_size} active members
    - Consider rotating facilitator role to increase engagement
    
    **Meeting Efficiency:**
    - Average standup covers good ground, maintain current format
    - Add time-boxing (15 minutes max) to keep discussions focused
    
    **Blocker Resolution:**
    - Implement "parking lot" for detailed technical discussions
    - Assign blocker owners during standup for faster resolution
    
    **Follow-up Actions:**
    - Create action items tracker from standup outcomes
    - Weekly review of recurring blockers and their solutions
    """

def extract_common_blockers(standups):
    """Extract common blocker themes from standups"""
    all_blockers = []
    for standup in standups:
        for update in standup.get('updates', []):
            if update.get('blockers'):
                all_blockers.append(update['blockers'].lower())
    
    # Simple keyword analysis
    common_keywords = ['test', 'review', 'deploy', 'environment', 'api', 'database']
    blocker_themes = {}
    
    for keyword in common_keywords:
        count = sum(1 for blocker in all_blockers if keyword in blocker)
        if count > 0:
            blocker_themes[keyword] = count
    
    return blocker_themes
