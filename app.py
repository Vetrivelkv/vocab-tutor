import streamlit as st
import json
import os

st.set_page_config(page_title="Vocab Tutor", page_icon="📖", layout="wide")

import auth
import dashboard
import learn
import quiz
import profile
import database as db

# Load Data
@st.cache_data
def load_data():
    with open('vocab_data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user' not in st.session_state:
    st.session_state.user = None
if 'current_class_id' not in st.session_state:
    st.session_state.current_class_id = None
if 'unlocked_classes' not in st.session_state:
    st.session_state.unlocked_classes = [1]

data = load_data()
st.session_state.vocab_data = data

# Top bar navigation
if st.session_state.user:
    col1, col2, col3 = st.columns([10, 1, 1])
    with col2:
        if st.session_state.page != 'dashboard':
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
    with col3:
        if st.session_state.page != 'profile':
            if st.button("👤 Profile", use_container_width=True):
                st.session_state.page = 'profile'
                st.rerun()

# Routing
if st.session_state.page == 'login':
    auth.render()
elif st.session_state.page == 'dashboard':
    if st.session_state.user:
        dashboard.render()
    else:
        st.session_state.page = 'login'
        st.rerun()
elif st.session_state.page == 'learn':
    if st.session_state.user:
        learn.render()
    else:
        st.session_state.page = 'login'
        st.rerun()
elif st.session_state.page == 'quiz':
    if st.session_state.user:
        quiz.render()
    else:
        st.session_state.page = 'login'
        st.rerun()
elif st.session_state.page == 'profile':
    if st.session_state.user:
        profile.render()
    else:
        st.session_state.page = 'login'
        st.rerun()
