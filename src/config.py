import os
import streamlit as st


def get_database_url():
    app_env = os.getenv("APP_ENV")

    if app_env is None:
        app_env = os.getenv("APP_ENV", "development")

    if app_env == "production":
        if "DB_URL" in st.secrets:
            return st.secrets["DB_URL"]

    return os.getenv("DB_URL")
