import streamlit as st

def require_role(allowed_roles):
    def decorator(func):
        def wrapper(*args, **kwargs):
            role = st.session_state.get("role", None)
            if role not in allowed_roles:
                st.error("No tienes permisos.")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
