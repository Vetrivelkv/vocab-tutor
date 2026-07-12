import streamlit as st
import database as db

def render():
    st.title("📚 Vocabulary Learning Dashboard")
    st.write("Welcome to the Ultimate English Vocabulary Tutor! Select a class below to start learning. You must score 100% on the quiz to unlock the next class.")
    
    classes = sorted(st.session_state.vocab_data.get('classes', []), key=lambda x: x.get('id', 0))
    
    # Sync unlocked classes from database
    user_id = st.session_state.user['id']
    progress_data = db.get_learning_progress(user_id)
    
    unlocked = [1] # Class 1 is always unlocked
    
    # If a class is passed, unlock the next one
    for p in progress_data:
        if p['topic_name'] == 'Vocabulary' and p['passed']:
            class_id = int(p['subtopic_id'].split()[1])
            if class_id + 1 not in unlocked:
                unlocked.append(class_id + 1)
                
    st.session_state.unlocked_classes = unlocked
    
    # We will display classes in a grid
    cols = st.columns(3)
    
    for idx, c in enumerate(classes):
        col = cols[idx % 3]
        with col:
            date_str = c.get('created_at', '')
            date_display = f" *(Created: {date_str})*" if date_str else ""
            st.write(f"### {c['title']}{date_display}")
            is_unlocked = c['id'] in unlocked
            
            if is_unlocked:
                st.success("🔓 Unlocked")
                
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    if st.button(f"📖 Learn", key=f"learn_{c['id']}", use_container_width=True):
                        st.session_state.current_class_id = c['id']
                        st.session_state.page = 'learn'
                        st.rerun()
                with subcol2:
                    if st.button(f"📝 Quiz", key=f"quiz_{c['id']}", use_container_width=True):
                        st.session_state.current_class_id = c['id']
                        st.session_state.page = 'quiz'
                        st.rerun()
            else:
                st.error("🔒 Locked")
                st.write("*Complete previous class quiz to unlock.*")
            
            st.write("---")
