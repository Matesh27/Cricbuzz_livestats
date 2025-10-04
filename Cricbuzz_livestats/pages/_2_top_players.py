import streamlit as st
import requests
import pandas as pd
import re

# ---------------- CONFIGURATION ----------------
RAPIDAPI_KEY = "787f633245msha1e09df8c3ca801p1192cejsna2ba2b7cddb1"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com"


# ---------- 0. Helper: Normalize player names ----------
def normalize_name(name: str) -> str:
    """Remove extra spaces and normalize to lowercase."""
    return re.sub(r"\s+", " ", name).strip().lower()


# ---------- 1. Convert stats JSON -> DataFrame ----------
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


# ---------- 2. Safe API helpers (with caching & error handling) ----------
@st.cache_data(ttl=300)
def get_player_id(name: str):
    """Return player id for given name or None on failure."""
    url = f"{BASE_URL}/stats/v1/player/search"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    params = {"plrN": name}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=10)
        resp.raise_for_status()
        j = resp.json()
        if "player" in j and isinstance(j["player"], list) and len(j["player"]) > 0:
            # Case-insensitive partial match
            for p in j["player"]:
                if p.get("name") and normalize_name(name) in normalize_name(p.get("name")):
                    return p.get("id")
            # fallback: return first result
            return j["player"][0].get("id")
    except Exception:
        return None
    return None


@st.cache_data(ttl=300)
def get_player_details(player_id: str):
    url = f"{BASE_URL}/stats/v1/player/{player_id}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


@st.cache_data(ttl=300)
def get_player_stats(player_id: str, stat_type: str):
    url = f"{BASE_URL}/stats/v1/player/{player_id}/{stat_type}"
    headers = {"X-RapidAPI-Key": RAPIDAPI_KEY, "X-RapidAPI-Host": RAPIDAPI_HOST}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return {}


# ---------- 3. Robust ranking extractor ----------
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


# ---------- 4. Streamlit page ----------
def app():
    st.set_page_config(page_title="Player Stats Dashboard", layout="wide")
    st.title("🏏 Player Stats Dashboard")

    player_name_input = st.text_input("🔍 Enter Player Name", placeholder="e.g., Usman Khawaja")
    if not player_name_input:
        st.info("Type a player name to fetch stats.")
        return

    # normalize input
    player_name_input = normalize_name(player_name_input)

    with st.spinner("🔎 Searching for player..."):
        player_id = get_player_id(player_name_input)

    if not player_id:
        st.error("❌ Player not found. Try a different spelling.")
        return

    with st.spinner("📊 Fetching player details..."):
        profile = get_player_details(player_id)
        batting_stats = get_player_stats(player_id, "batting")
        bowling_stats = get_player_stats(player_id, "bowling")

    # --- Player Info ---
    st.subheader("👤 Player Info")
    st.markdown(f"**Name:** {profile.get('name', 'N/A')}")
    st.markdown(f"**Batting Style:** {profile.get('bat', 'N/A')}")
    st.markdown(f"**Bowling Style:** {profile.get('bowl', 'N/A')}")
    st.markdown(f"**Role:** {profile.get('role', 'N/A')}")
    st.markdown(f"**Team:** {profile.get('intlTeam', 'N/A')}")

    # --- Rankings ---
    bat_rank, bowl_rank = get_rankings(profile)
    st.markdown(f"**Batting Rankings:** Test: {bat_rank['test']} | ODI: {bat_rank['odi']} | T20: {bat_rank['t20']}")
    if bowl_rank and any(v != "N/A" for v in bowl_rank.values()):
        st.markdown(f"**Bowling Rankings:** Test: {bowl_rank['test']} | ODI: {bowl_rank['odi']} | T20: {bowl_rank['t20']}")

    st.markdown("---")

    # --- Batting Stats Table ---
    st.subheader("📊 Batting Statistics")
    bat_df = parse_stats(batting_stats)
    if bat_df is not None:
        st.dataframe(bat_df, use_container_width=True)
    else:
        st.info("No batting data available for this player.")

    # --- Bowling Stats Table ---
    st.subheader("🥎 Bowling Statistics")
    bowl_df = parse_stats(bowling_stats)
    if bowl_df is not None:
        st.dataframe(bowl_df, use_container_width=True)
    else:
        st.info("No bowling data available for this player.")

    # --- Link to full profile ---
    weburl = profile.get("appIndex", {}).get("webURL")
    if weburl:
        st.markdown(f"🌐 [View full profile on Cricbuzz]({weburl})")


if __name__ == "__main__":
    app()

