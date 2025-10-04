import http.client
import json
import pandas as pd
import streamlit as st
from db_config import get_connection


st.title("📜 All Players List from Cricbuzz API")

all_players = []

# 🔁 Loop A-Z to get all players
for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    conn = http.client.HTTPSConnection("cricbuzz-cricket.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "f61f3ea877msh639a2f10de58520p1ee084jsnba7561211b52",
        'x-rapidapi-host': "cricbuzz-cricket.p.rapidapi.com"
    }
    endpoint = f"/stats/v1/player/search?plrN={ch}"
    conn.request("GET", endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()

    result = json.loads(data.decode("utf-8"))
    players = result.get("player", []) or result.get("players", [])
    for p in players:
        all_players.append({
            "Player ID": p.get("id"),
            "Player Name": p.get("name"),
            "Country": p.get("teamName", "N/A")
        })

# 🧹 Remove duplicates
df = pd.DataFrame(all_players).drop_duplicates(subset=["Player ID"]).reset_index(drop=True)

# 📊 Show table
st.dataframe(df)

st.success(f"✅ Total players fetched: {len(df)}")

# --- Store in MySQL ---
if st.button("📥 Save to MySQL"):
    conn = get_connection()
    cursor = conn.cursor()

    insert_sql = """
    REPLACE INTO all_players (player_id, player_name, country)
    VALUES (%s, %s, %s)
    """

    # Insert each row
    for _, row in df.iterrows():
        cursor.execute(insert_sql, (int(row["Player ID"]), row["Player Name"], row["Country"]))

    conn.commit()
    cursor.close()
    conn.close()

    st.success(f"✅ Successfully stored {len(df)} players into MySQL!")