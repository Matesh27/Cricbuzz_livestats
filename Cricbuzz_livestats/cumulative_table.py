# app.py
import streamlit as st
import pandas as pd
from db_config import get_connection
import requests

# ---------------- CONFIG ----------------
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"
RAPIDAPI_KEY = "3dec87bbc9msh63017f83d98f567p18d1eajsnf0b05269a1a1"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

# ---------------- DATABASE CONNECTION -----------------
conn = get_connection()
cursor = conn.cursor()

# ---------------- HELPER FUNCTIONS -----------------
def parse_stats(stats_json):
    if not stats_json or "values" not in stats_json:
        return None
    rows = []
    for item in stats_json.get("values", []):
        v = item.get("values")
        if v:
            rows.append(v)
    if not rows:
        return None
    headers = stats_json.get("headers")
    maxlen = max(len(r) for r in rows)
    if headers and len(headers) >= maxlen:
        columns = headers[:maxlen]
    elif headers:
        columns = headers + [f"col_{i}" for i in range(len(headers), maxlen)]
    else:
        columns = [f"col_{i}" for i in range(maxlen)]
    norm_rows = [r + [""] * (maxlen - len(r)) for r in rows]
    df = pd.DataFrame(norm_rows, columns=columns)
    df = df.set_index(columns[0])
    return df

def get_player_details(player_id: str):
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except:
        return {}

def get_player_stats(player_id: str, stat_type: str):
    url = f"{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except:
        return {}

def _extract_rank_from_section(section):
    if not section:
        return {"test": "N/A", "odi": "N/A", "t20": "N/A"}
    if isinstance(section, list):
        sec = section[0] if len(section) > 0 and isinstance(section[0], dict) else {}
    elif isinstance(section, dict):
        sec = section
    else:
        sec = {}
    def find_value(candidates):
        for k in candidates:
            if k in sec and sec[k] not in (None, "", "0"):
                return sec[k]
        return "N/A"
    test = find_value(["testRank", "testBestRank", "test_rank", "testBest", "test"])
    odi = find_value(["odiRank", "odiBestRank", "odi_bestRank", "odi_best", "odi"])
    t20 = find_value(["t20Rank", "t20BestRank", "t20_bestRank", "t20_best", "t20"])
    return {"test": test, "odi": odi, "t20": t20}

def get_rankings(profile):
    ranks = profile.get("rankings") or {}
    bat_section = ranks.get("bat") or ranks.get("batting") or ranks.get("batsman") or ranks.get("bat_rank") or ranks.get("bats")
    bowl_section = ranks.get("bowl") or ranks.get("bowling") or ranks.get("bowler") or ranks.get("bowl_rank")
    if not bat_section and isinstance(ranks.get("all"), list) and ranks.get("all"):
        bat_section = ranks.get("all")[0]
    return _extract_rank_from_section(bat_section), _extract_rank_from_section(bowl_section)

# ---------------- FETCH ALL PLAYERS -----------------
def fetch_all_players():
    cursor.execute("SELECT player_id, player_name FROM all_players LIMIT 150")
    return cursor.fetchall()

players = fetch_all_players()

st.title("🏏 Player Stats Dashboard (Automated)")

# ---------------- UPDATE ALL PLAYERS -----------------
def update_all_players():
    for p in players:
        player_id = p["player_id"]
        name = p["player_name"]

        profile = get_player_details(player_id)
        bat_rank, bowl_rank = get_rankings(profile)

        # --- Batting ---
        batting_json = get_player_stats(player_id, "batting")
        df_bat = parse_stats(batting_json)
        if df_bat is not None:
            for fmt in ["Test", "ODI", "T20"]:
                if fmt in df_bat.columns:
                    matches = int(df_bat.loc["Matches", fmt] if "Matches" in df_bat.index else 0)
                    runs = int(df_bat.loc["Runs", fmt] if "Runs" in df_bat.index else 0)
                    avg = float(df_bat.loc["Average", fmt] if "Average" in df_bat.index else 0)
                    sr = float(df_bat.loc["Strike Rate", fmt] if "Strike Rate" in df_bat.index else 0)
                    best = df_bat.loc["Highest Score", fmt] if "Highest Score" in df_bat.index else ""
                    cursor.execute("""
                    REPLACE INTO player_stats_cum
                    (player_id, player_name, format_type, matches, runs, average, strike_rate, best_score, bat_rank, bowl_rank)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """, (
                    player_id, name, fmt, matches, runs, avg, sr, best,
                    bat_rank.get(fmt.lower(), "N/A"),
                    bowl_rank.get(fmt.lower(), "N/A")
                ))

                    conn.commit()

        # --- Bowling ---
        bowling_json = get_player_stats(player_id, "bowling")
        df_bowl = parse_stats(bowling_json)
        if df_bowl is not None:
            for fmt in ["Test", "ODI", "T20"]:
                if fmt in df_bowl.columns:
                    wickets = int(df_bowl.loc["Wickets", fmt] if "Wickets" in df_bowl.index else 0)
                    cursor.execute("""
                        UPDATE player_stats_cum SET wickets=%s WHERE player_id=%s AND format_type=%s
                    """, (wickets, player_id, fmt))
                    conn.commit()

st.sidebar.button("🔄 Update All Players Stats", on_click=update_all_players)

# ---------------- DISPLAY ALL PLAYER STATS -----------------
df_stats = pd.read_sql("SELECT * FROM player_stats_cum", conn)

# Add Top Performer Columns
df_stats["Top Runs"] = ""
df_stats["Top Average"] = ""
df_stats["Top Wickets"] = ""

for fmt in ["Test", "ODI", "T20"]:
    df_fmt = df_stats[df_stats["format_type"] == fmt]
    if not df_fmt.empty:
        df_stats.loc[df_fmt["runs"].idxmax(), "Top Runs"] = "Yes"
        df_stats.loc[df_fmt["average"].idxmax(), "Top Average"] = "Yes"
        df_stats.loc[df_fmt["wickets"].idxmax(), "Top Wickets"] = "Yes"

st.dataframe(df_stats)
