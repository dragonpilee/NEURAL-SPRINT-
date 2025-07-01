import streamlit as st
from datetime import datetime
import pandas as pd

def show_backlog_management():
    """Backlog management interface"""
    
    st.markdown("## 📝 BACKLOG NEURAL NETWORK")
    
    tab1, tab2, tab3 = st.tabs(["📋 Product Backlog", "➕ Create Story", "🔧 Bulk Operations"])
    
    with tab1:
        show_product_backlog()
    
    with tab2:
        show_story_creation()
    
    with tab3:
        show_bulk_operations()

def show_product_backlog():
    """Display and manage product backlog"""
    
    # Filters and controls
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox("Filter by Status", 
                                   ["All"] + st.session_state.scrum_manager.story_statuses)
    
    with col2:
        priority_filter = st.selectbox("Filter by Priority", 
                                     ["All"] + st.session_state.scrum_manager.priority_levels)
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Priority", "Created Date", "Story Points", "Title"])
    
    with col4:
        view_mode = st.selectbox("View Mode", ["Card View", "Table View"])
    
    # Get and filter stories
    all_stories = st.session_state.data_store.get_all_stories()
    
    # Apply filters
    filtered_stories = all_stories
    if status_filter != "All":
        filtered_stories = [s for s in filtered_stories if s.get('status') == status_filter]
    if priority_filter != "All":
        filtered_stories = [s for s in filtered_stories if s.get('priority') == priority_filter]
    
    # Sort stories
    if sort_by == "Priority":
        priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        filtered_stories.sort(key=lambda x: priority_order.get(x.get('priority', 'Medium'), 2))
    elif sort_by == "Created Date":
        filtered_stories.sort(key=lambda x: x.get('created_date', ''), reverse=True)
    elif sort_by == "Story Points":
        filtered_stories.sort(key=lambda x: x.get('story_points', 0) or 0, reverse=True)
    elif sort_by == "Title":
        filtered_stories.sort(key=lambda x: x.get('title', '').lower())
    
    st.markdown(f"### 📊 STORIES FOUND: {len(filtered_stories)}")
    
    if not filtered_stories:
        st.info("No stories match the current filters.")
        return
    
    if view_mode == "Card View":
        show_card_view(filtered_stories)
    else:
        show_table_view(filtered_stories)

def show_card_view(stories):
    """Display stories in card view"""
    
    for story in stories:
        with st.container():
            # Story card styling
            priority_colors = {
                "Critical": "#ff4757",
                "High": "#ff6b35", 
                "Medium": "#ffa726",
                "Low": "#66bb6a"
            }
            
            status_colors = {
                "Backlog": "#666",
                "To Do": "#3498db",
                "In Progress": "#f39c12",
                "In Review": "#9b59b6",
                "Done": "#27ae60"
            }
            
            priority_color = priority_colors.get(story.get('priority', 'Medium'), '#ffa726')
            status_color = status_colors.get(story.get('status', 'Backlog'), '#666')
            
            # Card header
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"### {story['title']}")
            
            with col2:
                st.markdown(f"<span style='color: {priority_color}; font-weight: bold;'>{story.get('priority', 'Medium')}</span>", 
                          unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"<span style='color: {status_color}; font-weight: bold;'>{story.get('status', 'Backlog')}</span>", 
                          unsafe_allow_html=True)
            
            with col4:
                points = story.get('story_points')
                if points:
                    st.markdown(f"**{points} pts**")
                else:
                    st.markdown("*Not estimated*")
            
            # Story details
            if story.get('description'):
                st.write(f"**Description:** {story['description']}")
            
            if story.get('acceptance_criteria'):
                with st.expander("📋 Acceptance Criteria"):
                    st.write(story['acceptance_criteria'])
            
            # Labels
            if story.get('labels'):
                st.markdown("**Labels:** " + ", ".join([f"`{label}`" for label in story['labels']]))
            
            # Actions
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("✏️ Edit", key=f"edit_{story['id']}"):
                    st.session_state.editing_story = story
                    st.rerun()
            
            with col2:
                if not story.get('story_points') and st.button("🎯 Estimate", key=f"estimate_{story['id']}"):
                    estimate_story_points(story)
            
            with col3:
                new_status = st.selectbox("Status", 
                                        st.session_state.scrum_manager.story_statuses,
                                        index=st.session_state.scrum_manager.story_statuses.index(story.get('status', 'Backlog')),
                                        key=f"status_{story['id']}")
                if new_status != story.get('status'):
                    st.session_state.scrum_manager.update_story_status(story['id'], new_status)
                    st.rerun()
            
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{story['id']}"):
                    if st.session_state.data_store.delete_story(story['id']):
                        st.success("Story deleted!")
                        st.rerun()
            
            st.markdown("---")

def show_table_view(stories):
    """Display stories in table view"""
    
    # Prepare data for table
    table_data = []
    for story in stories:
        table_data.append({
            "ID": story['id'][:8],
            "Title": story['title'],
            "Priority": story.get('priority', 'Medium'),
            "Status": story.get('status', 'Backlog'),
            "Points": story.get('story_points', 'Not estimated'),
            "Assignee": story.get('assignee', 'Unassigned'),
            "Created": story.get('created_date', '')[:10] if story.get('created_date') else ''
        })
    
    df = pd.DataFrame(table_data)
    
    # Make table interactive
    edited_df = st.data_editor(
        df,
        column_config={
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=st.session_state.scrum_manager.priority_levels,
                required=True
            ),
            "Status": st.column_config.SelectboxColumn(
                "Status", 
                options=st.session_state.scrum_manager.story_statuses,
                required=True
            ),
            "Points": st.column_config.NumberColumn(
                "Points",
                min_value=0,
                max_value=100,
                step=0.5
            )
        },
        disabled=["ID", "Title", "Created"],
        hide_index=True,
        use_container_width=True
    )
    
    # Apply changes
    if st.button("💾 Save Changes"):
        for index, row in edited_df.iterrows():
            story_id = None
            # Find the full story ID
            for story in stories:
                if story['id'].startswith(row['ID']):
                    story_id = story['id']
                    break
            
            if story_id:
                story = st.session_state.data_store.get_story(story_id)
                if story:
                    story['priority'] = row['Priority']
                    story['status'] = row['Status']
                    if row['Points'] != 'Not estimated':
                        story['story_points'] = float(row['Points'])
                    story['assignee'] = row['Assignee'] if row['Assignee'] != 'Unassigned' else None
                    
                    st.session_state.data_store.update_story(story_id, story)
        
        st.success("Changes saved successfully!")
        st.rerun()

def show_story_creation():
    """Story creation form"""
    
    st.markdown("### ➕ CREATE NEW USER STORY")
    
    # Check if editing existing story
    editing_story = st.session_state.get('editing_story')
    
    if editing_story:
        st.info(f"Editing story: {editing_story['title']}")
        if st.button("❌ Cancel Edit"):
            del st.session_state.editing_story
            st.rerun()
    
    with st.form("story_form", clear_on_submit=not editing_story):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            title = st.text_input("Story Title", 
                                value=editing_story.get('title', '') if editing_story else '',
                                placeholder="As a user, I want to...")
            
            description = st.text_area("Description", 
                                     value=editing_story.get('description', '') if editing_story else '',
                                     placeholder="Detailed description of the story...")
            
            acceptance_criteria = st.text_area("Acceptance Criteria", 
                                             value=editing_story.get('acceptance_criteria', '') if editing_story else '',
                                             placeholder="Given... When... Then...")
        
        with col2:
            priority = st.selectbox("Priority", 
                                  st.session_state.scrum_manager.priority_levels,
                                  index=st.session_state.scrum_manager.priority_levels.index(
                                      editing_story.get('priority', 'Medium')) if editing_story else 1)
            
            labels_input = st.text_input("Labels (comma-separated)", 
                                       value=', '.join(editing_story.get('labels', [])) if editing_story else '',
                                       placeholder="frontend, api, bug")
            
            assignee = st.text_input("Assignee", 
                                   value=editing_story.get('assignee', '') if editing_story else '',
                                   placeholder="Developer name")
            
            story_points = st.number_input("Story Points", 
                                         min_value=0.0, max_value=100.0, step=0.5,
                                         value=float(editing_story.get('story_points', 0)) if editing_story and editing_story.get('story_points') else 0.0)
        
        # AI estimation option
        col1, col2 = st.columns(2)
        with col1:
            use_ai_estimation = st.checkbox("🤖 Use AI for story point estimation", 
                                          disabled=not st.session_state.ai_client.check_connection())
        
        with col2:
            submit_button = st.form_submit_button("💾 Save Story" if editing_story else "➕ Create Story", 
                                                use_container_width=True)
        
        if submit_button and title.strip():
            # Parse labels
            labels = [label.strip() for label in labels_input.split(',') if label.strip()]
            
            if editing_story:
                # Update existing story
                story = editing_story.copy()
                story.update({
                    'title': title,
                    'description': description,
                    'acceptance_criteria': acceptance_criteria,
                    'priority': priority,
                    'labels': labels,
                    'assignee': assignee if assignee.strip() else None,
                    'updated_date': datetime.now().isoformat()
                })
                
                if story_points > 0:
                    story['story_points'] = story_points
                
                story_id = story['id']
            else:
                # Create new story
                story = st.session_state.scrum_manager.create_user_story(
                    title=title,
                    description=description,
                    acceptance_criteria=acceptance_criteria,
                    priority=priority,
                    labels=labels
                )
                
                if assignee.strip():
                    story['assignee'] = assignee.strip()
                
                if story_points > 0:
                    story['story_points'] = story_points
                
                story_id = story['id']
            
            # AI estimation
            if use_ai_estimation and not story.get('story_points'):
                with st.spinner("🤖 AI is analyzing story complexity..."):
                    estimation_result = st.session_state.ai_client.estimate_story_points(
                        title, description, acceptance_criteria
                    )
                    
                    if estimation_result:
                        story['story_points'] = estimation_result['estimated_points']
                        story['estimation_reasoning'] = estimation_result['reasoning']
                        story['complexity_factors'] = estimation_result['complexity_factors']
                        
                        st.success(f"🎯 AI estimated {estimation_result['estimated_points']} story points")
                        with st.expander("🧠 AI Reasoning"):
                            st.write(estimation_result['reasoning'])
            
            # Save story
            if st.session_state.data_store.save_story(story):
                if editing_story:
                    st.success("✅ Story updated successfully!")
                    del st.session_state.editing_story
                else:
                    st.success("✅ Story created successfully!")
                st.rerun()
            else:
                st.error("❌ Failed to save story")

def show_bulk_operations():
    """Bulk operations on stories"""
    
    st.markdown("### 🔧 BULK OPERATIONS")
    
    all_stories = st.session_state.data_store.get_all_stories()
    
    if not all_stories:
        st.info("No stories available for bulk operations.")
        return
    
    # Story selection
    selected_stories = st.multiselect(
        "Select Stories for Bulk Operations",
        options=[s['id'] for s in all_stories],
        format_func=lambda x: f"{next(s['title'] for s in all_stories if s['id'] == x)} "
                             f"({next(s.get('status', 'Unknown') for s in all_stories if s['id'] == x)})"
    )
    
    if not selected_stories:
        st.info("Select stories to perform bulk operations.")
        return
    
    st.markdown(f"**Selected {len(selected_stories)} stories**")
    
    # Bulk operations
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📊 Bulk Status Update")
        new_status = st.selectbox("New Status", st.session_state.scrum_manager.story_statuses)
        if st.button("📊 Update Status", use_container_width=True):
            updated_count = 0
            for story_id in selected_stories:
                if st.session_state.scrum_manager.update_story_status(story_id, new_status):
                    updated_count += 1
            st.success(f"✅ Updated {updated_count} stories to '{new_status}'")
            st.rerun()
    
    with col2:
        st.markdown("#### 🏷️ Bulk Label Update")
        new_labels = st.text_input("Add Labels (comma-separated)", placeholder="bug, urgent, frontend")
        if st.button("🏷️ Add Labels", use_container_width=True) and new_labels.strip():
            labels_to_add = [label.strip() for label in new_labels.split(',') if label.strip()]
            updated_count = 0
            
            for story_id in selected_stories:
                story = st.session_state.data_store.get_story(story_id)
                if story:
                    existing_labels = set(story.get('labels', []))
                    existing_labels.update(labels_to_add)
                    story['labels'] = list(existing_labels)
                    story['updated_date'] = datetime.now().isoformat()
                    
                    if st.session_state.data_store.update_story(story_id, story):
                        updated_count += 1
            
            st.success(f"✅ Added labels to {updated_count} stories")
            st.rerun()
    
    with col3:
        st.markdown("#### 🤖 Bulk AI Estimation")
        if st.button("🎯 Estimate All", use_container_width=True):
            if st.session_state.ai_client.check_connection():
                estimated_count = 0
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                for i, story_id in enumerate(selected_stories):
                    story = st.session_state.data_store.get_story(story_id)
                    if story and not story.get('story_points'):
                        status_text.text(f"Estimating: {story['title'][:30]}...")
                        
                        estimation_result = st.session_state.ai_client.estimate_story_points(
                            story['title'], 
                            story.get('description', ''), 
                            story.get('acceptance_criteria', '')
                        )
                        
                        if estimation_result:
                            story['story_points'] = estimation_result['estimated_points']
                            story['estimation_reasoning'] = estimation_result['reasoning']
                            story['updated_date'] = datetime.now().isoformat()
                            
                            if st.session_state.data_store.update_story(story_id, story):
                                estimated_count += 1
                    
                    progress_bar.progress((i + 1) / len(selected_stories))
                
                status_text.text("")
                progress_bar.empty()
                st.success(f"✅ Estimated {estimated_count} stories")
                st.rerun()
            else:
                st.error("AI service unavailable")
    
    # Bulk export
    st.markdown("#### 📤 EXPORT SELECTED STORIES")
    if st.button("📋 Export to CSV", use_container_width=True):
        export_data = []
        for story_id in selected_stories:
            story = st.session_state.data_store.get_story(story_id)
            if story:
                export_data.append({
                    "ID": story['id'],
                    "Title": story['title'],
                    "Description": story.get('description', ''),
                    "Acceptance Criteria": story.get('acceptance_criteria', ''),
                    "Priority": story.get('priority', ''),
                    "Status": story.get('status', ''),
                    "Story Points": story.get('story_points', ''),
                    "Assignee": story.get('assignee', ''),
                    "Labels": ', '.join(story.get('labels', [])),
                    "Created Date": story.get('created_date', '')
                })
        
        df = pd.DataFrame(export_data)
        csv = df.to_csv(index=False)
        
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"stories_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def estimate_story_points(story):
    """Estimate story points using AI"""
    if not st.session_state.ai_client.check_connection():
        st.error("AI service unavailable for estimation")
        return
    
    with st.spinner(f"🤖 Estimating story points for: {story['title'][:30]}..."):
        estimation_result = st.session_state.ai_client.estimate_story_points(
            story['title'],
            story.get('description', ''),
            story.get('acceptance_criteria', '')
        )
        
        if estimation_result:
            story['story_points'] = estimation_result['estimated_points']
            story['estimation_reasoning'] = estimation_result['reasoning']
            story['complexity_factors'] = estimation_result['complexity_factors']
            story['updated_date'] = datetime.now().isoformat()
            
            if st.session_state.data_store.update_story(story['id'], story):
                st.success(f"✅ Estimated {estimation_result['estimated_points']} story points")
                
                with st.expander("🧠 AI Reasoning"):
                    st.write(estimation_result['reasoning'])
                    
                    if estimation_result['complexity_factors']:
                        st.write("**Complexity Factors:**")
                        for factor in estimation_result['complexity_factors']:
                            st.write(f"• {factor}")
                
                st.rerun()
            else:
                st.error("Failed to save estimation")
        else:
            st.error("Failed to get AI estimation")
