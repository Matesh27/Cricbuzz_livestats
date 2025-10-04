import streamlit as st
from db_config import get_connection
import pandas as pd


def app():
    st.title("📋 Players CRUD Operations")

    # --- READ DATA ---
    st.subheader("📊 All Players")

    try:
        # ✅ Step 1: Connect to MySQL
        conn = get_connection()
        cursor = conn.cursor()

        # ✅ Step 2: Fetch all players

        cursor.execute("SELECT * FROM player_stats_cum")  # replace with your table name
        result = cursor.fetchall()

        # Get column names
        columns = [i[0] for i in cursor.description]

        # Convert to Pandas DataFrame
        df = pd.DataFrame(result, columns=columns)

        # Streamlit UI
        st.title("MySQL Data in Streamlit")

        # Show the table
        st.dataframe(df)
        
    except Exception as e:
        st.error(f"Error fetching players: {e}")
        

    # ✅ CREATE: Add new player stats

    st.subheader("➕ Add New Player Stats")
    with st.form("add_form"):
        player_id = st.number_input("Player ID", min_value=1, step=1)
        player_name = st.text_input("Player Name")
        format_type = st.selectbox("Format", ["Test", "ODI", "T20"])
        matches = st.number_input("Matches", min_value=0, step=1)
        runs = st.number_input("Runs", min_value=0, step=1)
        average = st.number_input("Average", min_value=0.0, step=0.1)
        strike_rate = st.number_input("Strike Rate", min_value=0.0, step=0.1)
        wickets = st.number_input("Wickets", min_value=0, step=1)
        best_score = st.text_input("Best Score")
        bat_rank = st.text_input("Bat Rank")
        bowl_rank = st.text_input("Bowl Rank")
        submit = st.form_submit_button("Add Record")

        if submit:
            cursor.execute(
                """INSERT INTO all_players (player_id, player_name, country) VALUES (%s, %s, "INDIA")""",
                (player_id, player_name)
            )

            cursor.execute(
                """
                INSERT INTO player_stats_cum 
                (player_id, player_name, format_type, matches, runs, average, strike_rate, wickets, best_score, bat_rank, bowl_rank)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (player_id, player_name, format_type, matches, runs, average, strike_rate, wickets, best_score, bat_rank, bowl_rank)
            )

            conn.commit()
            st.success("✅ Record added successfully!")


    # ✅ UPDATE: Update player stats by ID

    st.subheader("✏️ Update Existing Record")
    with st.form("update_form"):
        update_id = st.number_input("Enter Player ID to Update", min_value=1, step=1)
        new_runs = st.number_input("New Runs", min_value=0, step=1)
        new_average = st.number_input("New Average", min_value=0.0, step=0.1)
        new_strike_rate = st.number_input("New Strike Rate", min_value=0.0, step=0.1)
        new_wickets = st.number_input("New Wickets", min_value=0, step=1)
        update = st.form_submit_button("Update Record")

        if update:
            cursor.execute("""
                UPDATE player_stats_cum
                SET runs=%s, average=%s, strike_rate=%s, wickets=%s
                WHERE player_id=%s
            """, (new_runs, new_average, new_strike_rate, new_wickets, update_id))
            conn.commit()
            st.success("✅ Record updated successfully!")

    # ✅ DELETE: Delete player by name

    st.subheader("🗑️ Delete a Record")
    with st.form("delete_form"):
        delete_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)
        confirm_delete = st.checkbox("Are you sure?")
        delete = st.form_submit_button("Delete Record")

        if delete and confirm_delete:
            cursor.execute("DELETE FROM player_stats_cum WHERE player_id = %s", (delete_id,))
            conn.commit()
            st.success("🗑️ Record deleted successfully!")

    cursor.close()
    conn.close()
