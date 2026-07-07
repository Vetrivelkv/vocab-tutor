import streamlit as st
import database as db

def render():
    st.title("Vocab Tutor Login 📖")
    
    if not db.is_db_connected():
        st.error("🚨 Supabase is not configured! Please set up your secrets.toml.")
        st.stop()
        
    if 'auth_mode' not in st.session_state:
        st.session_state.auth_mode = 'Login'
        
    mode = st.radio("Select Mode", ['Login', 'Register'], horizontal=True, key="auth_radio", 
                    index=0 if st.session_state.auth_mode == 'Login' else 1)
    st.session_state.auth_mode = mode
    
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.auth_mode == 'Login':
            st.subheader("🔑 Login to your account")
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
                if submitted:
                    if username and password:
                        success, result = db.login_user(username, password)
                        if success:
                            st.session_state.user = result
                            st.session_state.page = "dashboard"
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.warning("Please fill in both fields.")
        else:
            st.subheader("✨ Create a new account")
            with st.form("register_form"):
                new_username = st.text_input("Username")
                new_password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Register", use_container_width=True, type="primary")
                if submitted:
                    if new_username and new_password:
                        success, result = db.register_user(new_username, new_password)
                        if success:
                            st.success("Registration successful! Switching to login...")
                            st.session_state.auth_mode = 'Login'
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.warning("Please fill in both fields.")
