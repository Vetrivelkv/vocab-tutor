import streamlit as st
import database as db

def render():
    class_id = st.session_state.current_class_id
    if not class_id:
        st.session_state.page = 'dashboard'
        st.rerun()
        
    class_data = next(c for c in st.session_state.vocab_data['classes'] if c['id'] == class_id)
    quiz_data = class_data['quiz']
    
    st.title(f"📝 Quiz: {class_data['title']}")
    st.write("You must score 20/20 to unlock the next class. Good luck!")
    
    with st.form("quiz_form"):
        st.subheader("Part 1: Meaning (Multiple Choice)")
        mcq_answers = []
        for i, q in enumerate(quiz_data['meaning_mcq']):
            st.write(f"**{i+1}. {q['question']}**")
            ans = st.radio(f"Select meaning for Q{i+1}", q['options'], key=f"mcq_{i}", label_visibility="collapsed")
            mcq_answers.append(ans)
            st.write("")
            
        st.write("---")
        
        st.subheader("Part 2: Sentence Fill-in-the-Blanks")
        fill_answers = []
        for i, q in enumerate(quiz_data['sentence_fill']):
            st.write(f"**{i+11}. {q['question']}**")
            ans = st.selectbox(f"Select word for Q{i+11}", ["Select..."] + q['options'], key=f"fill_{i}", label_visibility="collapsed")
            fill_answers.append(ans)
            st.write("")
            
        submitted = st.form_submit_button("Submit Quiz", use_container_width=True)
        
    if submitted:
        score = 0
        total = len(quiz_data['meaning_mcq']) + len(quiz_data['sentence_fill'])
        
        for i, q in enumerate(quiz_data['meaning_mcq']):
            if mcq_answers[i] == q['answer']:
                score += 1
                
        for i, q in enumerate(quiz_data['sentence_fill']):
            if fill_answers[i] == q['answer']:
                score += 1
                
        passed = (score == total)
        
        # Save to Supabase
        user_id = st.session_state.user['id']
        subtopic_id = f"Class {class_id}"
        db.save_learning_progress(user_id, "Vocabulary", subtopic_id, passed, score)
        
        st.write("---")
        st.header(f"Your Score: {score} / {total}")
        
        if passed:
            st.balloons()
            st.success("🎉 Perfect Score! You have unlocked the next class. Progress saved to database!")
            if st.button("Return to Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
        else:
            st.error("You need a perfect score to unlock the next class. Your attempt has been recorded. Please try again.")
