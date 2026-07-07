import streamlit as st
import os

def render():
    class_id = st.session_state.current_class_id
    if not class_id:
        st.session_state.page = 'dashboard'
        st.rerun()
        
    class_data = next(c for c in st.session_state.vocab_data['classes'] if c['id'] == class_id)
    
    st.title(f"📖 Learning: {class_data['title']}")
    
    if 'current_word_idx' not in st.session_state:
        st.session_state.current_word_idx = 0
        
    idx = st.session_state.current_word_idx
    word_data = class_data['words'][idx]
    
    st.write(f"### Word {idx + 1} of {len(class_data['words'])}")
    st.progress((idx + 1) / len(class_data['words']))
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"## **{word_data['word']}** *({word_data['pos']})*")
        st.markdown(f"**Syllables:** {word_data['syllables']}")
        st.markdown(f"**Pronunciation (EN):** {word_data['pronunciation_en']}")
        st.markdown(f"**Pronunciation (TA):** {word_data['pronunciation_ta']}")
        
        st.markdown(f"### Meaning")
        st.info(f"**EN:** {word_data['meaning_en']}")
        st.info(f"**TA:** {word_data['meaning_ta']}")
        
        st.markdown(f"### Example")
        st.success(f"**EN:** {word_data['example_en']}")
        st.success(f"**TA:** {word_data['example_ta']}")
        
    with col2:
        if os.path.exists(word_data['image']):
            st.image(word_data['image'], use_column_width=True)
        else:
            st.warning("Image generation pending...")
            
    st.write("---")
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
    with btn_col1:
        if st.button("⬅️ Previous", disabled=(idx == 0), use_container_width=True):
            st.session_state.current_word_idx -= 1
            st.rerun()
    with btn_col3:
        if idx == len(class_data['words']) - 1:
            if st.button("📝 Take Quiz", use_container_width=True):
                st.session_state.page = 'quiz'
                st.session_state.current_word_idx = 0
                st.rerun()
        else:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_word_idx += 1
                st.rerun()
