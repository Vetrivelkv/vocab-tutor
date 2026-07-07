import streamlit as st
from supabase import create_client, Client
import bcrypt

@st.cache_resource
def init_connection():
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except KeyError:
        return None

supabase: Client = init_connection()

def is_db_connected():
    return supabase is not None

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(username, password):
    if not is_db_connected(): return False, "DB not configured"
    res = supabase.table('users').select('*').eq('username', username).execute()
    if len(res.data) > 0:
        return False, "Username already exists."
    
    hashed = hash_password(password)
    try:
        new_user = supabase.table('users').insert({'username': username, 'password_hash': hashed}).execute()
        return True, new_user.data[0]
    except Exception as e:
        return False, str(e)

def login_user(username, password):
    if not is_db_connected(): return False, "DB not configured"
    res = supabase.table('users').select('*').eq('username', username).execute()
    if len(res.data) == 0:
        return False, "Invalid username or password."
    user = res.data[0]
    if verify_password(password, user['password_hash']):
        return True, user
    return False, "Invalid username or password."

def get_learning_progress(user_id):
    if not is_db_connected(): return []
    res = supabase.table('learning_progress').select('*').eq('user_id', user_id).execute()
    return res.data

def save_learning_progress(user_id, topic_name, subtopic_id, passed, score):
    if not is_db_connected(): return
    res = supabase.table('learning_progress').select('*').eq('user_id', user_id).eq('topic_name', topic_name).eq('subtopic_id', subtopic_id).execute()
    
    if len(res.data) > 0:
        prog = res.data[0]
        new_attempts = prog['attempts'] + 1
        new_high = max(prog['high_score'], score)
        new_passed = prog['passed'] or passed
        supabase.table('learning_progress').update({
            'passed': new_passed,
            'attempts': new_attempts,
            'high_score': new_high,
            'last_attempted_at': 'now()'
        }).eq('id', prog['id']).execute()
    else:
        supabase.table('learning_progress').insert({
            'user_id': user_id,
            'topic_name': topic_name,
            'subtopic_id': subtopic_id,
            'passed': passed,
            'attempts': 1,
            'high_score': score
        }).execute()
