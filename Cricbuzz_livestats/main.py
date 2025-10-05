# main.py
import streamlit as st

st.set_page_config(page_title="Cricbuzz", layout="wide")
st.title("🏏 Cricbuzz LiveStats")

# Sidebar Navigation
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio(
    "Select a Page:",
    ["Home", "Live Matches", "Top Players", "SQL Queries", "CRUD"]
)

# Page Routing
# Page Routing
if page == "Home":
    st.header("Welcome to Cricbuzz LiveStats 📊")
    st.write("""
    - **Live Matches:** Get live cricket data from Cricbuzz API in a DataFrame  
    - **Top Players:** View palyer stats using player name from API Key  
    - **SQL Queries:** Run predefined queries with DataFrame output  
    - **CRUD:** Perform CRUD operations on players easily  
    """)
elif page == "Live Matches":
    from pages import _1_live_matches as live
    live.app()
elif page == "Top Players":
    from pages import _2_top_players as top
    top.app()
elif page == "SQL Queries":
    from pages import _3_SQL_queries as sql
    sql.app()
elif page == "CRUD":
    from pages import _4_CRUD as crud
    crud.app()


