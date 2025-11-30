# Evoticket 🎫: Plataforma de Gestión de Eventos y Tickets

**Evoticket** es una moderna plataforma diseñada para la **gestión integral de eventos** y la **venta de tickets**, construida con **Python** y **Streamlit**.

Permite gestionar eventos, categorías de tickets, usuarios con roles, compras, y lo más importante: la generación de tickets seguros en **PDF con código QR único**.

---

## ✨ Características Principales

* **Gestión Completa (CRUD):**
    * Eventos.
    * Tickets y sus Categorías.
    * Usuarios y sus roles (**Administrador**, **Operario**, **Gestor de contenido**).
* **Proceso de Compra:**
    * Interfaz pública para la consulta de eventos y la compra de tickets.
    * Validaciones de **edad** y **disponibilidad** de tickets en tiempo real.
* **Tickets Seguros:**
    * Generación de tickets en **PDF** con un **QR único** para cada compra.
    * Descarga de tickets directa para el comprador.
* **Panel Administrativo:**
    * Funcionalidades de CRUD.
    * **Filtros** y **paginación** para una gestión eficiente.
    * Control de la cantidad de tickets disponibles.

---

## 💻 Tecnologías Utilizadas

El proyecto Evoticket se basa en las siguientes tecnologías principales:

| Categoría | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend** | **Python** 🐍 | Lenguaje de programación principal para la lógica de la aplicación. |
| **Frontend/UI** | **Streamlit** | Framework de Python utilizado para construir la interfaz de usuario web de forma rápida y sencilla. |
| **Base de Datos** | **PostgreSQL** (Sugerido) | Sistema de gestión de bases de datos relacionales robusto y escalable (la configuración inicial usa SQLite, pero está preparada para PostgreSQL). |
| **Contenedores** | **Docker** (Recomendado) | Para empaquetar la aplicación y sus dependencias, asegurando un entorno de ejecución consistente. |

---

## ⚙️ Instalación

Sigue estos pasos para poner en marcha Evoticket en tu entorno local:

1.  **Clonar el repositorio:**

    ```bash
    git clone [https://github.com/tu_usuario/evoticket.git](https://github.com/tu_usuario/evoticket.git)
    cd evoticket
    ```

2.  **Crear y activar un entorno virtual** (recomendado):

    ```bash
    python -m venv venv
    # En Linux / macOS
    source venv/bin/activate
    # En Windows
    venv\Scripts\activate
    ```

3.  **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar variables de entorno** (si usas un archivo `.env`):

    ```env
    DATABASE_URL=sqlite:///evoticket.db
    ```

5.  **Crear la base de datos y tablas:**

    ```bash
    python create_db.py
    ```

---

## 🚀 Uso

Una vez configurado, ejecuta la aplicación principal de Streamlit:

```bash
streamlit run app.py