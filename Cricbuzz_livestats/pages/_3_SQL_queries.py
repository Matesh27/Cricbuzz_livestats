import streamlit as st
from db_config import get_connection    
import pandas as pd

def app():   
    st.title("📋 SQL Queries")       
    st.subheader("Select a query to run:")

    # ✅ Define your queries
    query_options = {
        "Top 10 Highest Run Scorers in T20": """
            SELECT player_name, matches, runs, average, strike_rate 
            FROM player_stats_cum 
            ORDER BY runs DESC 
            LIMIT 10
        """,
        # Add more queries here if needed
    }

    # ✅ Dropdown for selecting query
    selected_query_name = st.selectbox("Query Options", list(query_options.keys()))

    # ✅ Run query only when button is clicked
    if st.button("Run Query"):
        try:
            # Connect to MySQL
            conn = get_connection()
            cursor = conn.cursor()

            # Execute selected query
            cursor.execute(query_options[selected_query_name])
            result = cursor.fetchall()

            # Get column names
            columns = [i[0] for i in cursor.description]

            # Convert to DataFrame
            df = pd.DataFrame(result, columns=columns)

            # Display table
            st.subheader(f"Results: {selected_query_name}")
            st.dataframe(df)

        except Exception as e:
            st.error(f"Error fetching data: {e}")
