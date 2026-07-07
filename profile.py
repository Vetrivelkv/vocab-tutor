import streamlit as st
import database as db

def render():
    st.button("🔙 Back to Dashboard", on_click=lambda: st.session_state.update({'page': 'dashboard'}))
    st.title("👤 User Profile")
    st.markdown(f"### Hello, {st.session_state.user['username']}!")
    
    l_prog = db.get_learning_progress(st.session_state.user['id'])
    
    st.divider()
    
    # --- LEARNING PROGRESS ---
    st.subheader("📖 Vocabulary Journey Progress")
    if not l_prog:
        st.info("You haven't started your vocabulary journey yet.")
    else:
        l_topics = list(set([p['topic_name'] for p in l_prog]))
        for topic in l_topics:
            with st.expander(f"📚 {topic} Modules", expanded=True):
                t_data = [p for p in l_prog if p['topic_name'] == topic]
                
                # Sort by class ID string (e.g. 'Class 1')
                t_data = sorted(t_data, key=lambda x: int(x['subtopic_id'].split()[1]) if len(x['subtopic_id'].split()) > 1 else x['subtopic_id'])
                
                table_data = []
                for p in t_data:
                    table_data.append({
                        "Class": p['subtopic_id'],
                        "Status": "✅ Unlocked" if p['passed'] else "❌ Attempting",
                        "High Score": f"{p['high_score']} / 20",
                        "Attempts": p['attempts']
                    })
                st.table(table_data)
                
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()
