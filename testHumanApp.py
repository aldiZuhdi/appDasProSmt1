import streamlit as web
import time

with web.spinner("Sabar Loading dulu..."):
    time.sleep(5)
    web.title("Ini Dashboard")