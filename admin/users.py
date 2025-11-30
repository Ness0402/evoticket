import streamlit as st
import bcrypt
from database.connection import SessionLocal
from database.models import User
from auth.roles import require_role
import time

db = SessionLocal()

ROLES = ["Administrador", "Operario", "Gestor de contenido"]

@require_role(["Administrador"])
def admin_users_ui():

    st.title("👤 Gestión de Usuarios")
    current_user = st.session_state.get("user")
    with st.popover("➕ Nuevo usuario"):
        st.subheader("Crear usuario")

        username = st.text_input("Usuario", key="new_user_username")
        name = st.text_input("Nombre completo", key="new_user_name")
        password = st.text_input("Contraseña", type="password", key="new_user_password")
        role = st.selectbox("Rol", ROLES, key="new_user_role")
        active = st.checkbox("Activo", value=True, key="new_user_active")

        if st.button("Guardar usuario", key="save_new_user"):
            if not username or not password:
                st.error("Usuario y contraseña son obligatorios.")
            else:
                hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                user = User(
                    username=username,
                    name=name,
                    password=hashed,
                    role=role,
                    active=active
                )
                db.add(user)
                db.commit()
                st.success("Usuario creado correctamente.")
                time.sleep(1)
                st.rerun()

    st.write("---")
    st.write("## 📋 Lista de usuarios")

    users = db.query(User).order_by(User.id.desc()).all()

    users_query = db.query(User).order_by(User.id.desc())

    per_page = st.selectbox("Categorías por página", [5, 10, 20, 50], index=1)
    total = users_query.count()

    if "page_evt" not in st.session_state:
        st.session_state.page_evt = 1

    col1, col2, col3 = st.columns([1,1,3])
    with col1:
        if st.button("⬅️ Prev") and st.session_state.page_evt > 1:
            st.session_state.page_evt -= 1
    with col2:
        if st.button("Next ➡️") and (st.session_state.page_evt * per_page) < total:
            st.session_state.page_evt += 1

    offset = (st.session_state.page_evt - 1) * per_page
    users = users_query.offset(offset).limit(per_page).all()

    st.write(f"Página {st.session_state.page_evt} / {(total // per_page) + 1}")

    for u in users:
        with st.expander(f"👤 {u.username} ({u.role})"):

            new_name = st.text_input("Nombre", value=u.name, key=f"name_{u.id}")

            new_role = st.selectbox(
                "Rol",
                ROLES,
                index=ROLES.index(u.role) if u.role in ROLES else 0,
                key=f"role_{u.id}"
            )

            new_active = st.checkbox("Activo", value=u.active, key=f"active_{u.id}")

            col1, col2 = st.columns(2)

            with col1:
                if st.button("💾 Guardar cambios", key=f"save_{u.id}"):
                    u.name = new_name
                    u.role = new_role
                    u.active = new_active
                    db.commit()
                    st.success("Cambios guardados.")
                    time.sleep(1)
                    st.rerun()

            st.write("### 🔐 Cambiar contraseña")

            new_pass = st.text_input(
                "Nueva contraseña",
                type="password",
                key=f"pass_{u.id}"
            )

            if st.button("Actualizar contraseña", key=f"update_pass_{u.id}"):
                if new_pass.strip() == "":
                    st.error("La contraseña no puede estar vacía.")
                else:
                    hashed_pw = bcrypt.hashpw(new_pass.encode(), bcrypt.gensalt()).decode()
                    u.password = hashed_pw
                    db.commit()
                    st.success("Contraseña actualizada.")
                    time.sleep(1)
                    st.rerun()

            with col2:
                if st.button("🗑️ Eliminar usuario", key=f"delete_{u.id}"):
                    if u.username == current_user:
                        st.error("No puedes eliminar tu propio usuario.")
                    else:
                        db.delete(u)
                        db.commit()
                        st.warning("Usuario eliminado.")
                        time.sleep(1)
                        st.rerun()
