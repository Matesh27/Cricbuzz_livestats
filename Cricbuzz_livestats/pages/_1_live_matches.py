# # pages/1_Live_Matches.py
# import streamlit as st
# import requests
# import pandas as pd

# # 🔑 Replace with your RapidAPI Key
# RAPIDAPI_KEY = "787f633245msha1e09df8c3ca801p1192cejsna2ba2b7cddb1"
# RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

# def app():

   
#     st.header("📡 Matches")
#     # st.button("Fetch Live Matches")
#     # st.button("Fetch Upcoming Matches")
#     # st.button("Fetch Completed Matches")
#     # st.button("Fetch Series")
#     # st.button("Fetch Teams")

# #Incase of live matches
#     if st.button("Fetch Live Matches"):
#         url = f"https://{RAPIDAPI_HOST}/matches/v1/live"
#         headers = {
#             "X-RapidAPI-Host": RAPIDAPI_HOST,
#             "X-RapidAPI-Key": RAPIDAPI_KEY
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=15)
#             data = response.json()

#             matches = []
#             if "typeMatches" in data:
#                 for tm in data["typeMatches"]:
#                     for sm in tm.get("seriesMatches", []):
#                         series = sm.get("seriesAdWrapper", {})
#                         matches.extend(series.get("matches", []))

#             if matches:
#                 df = pd.json_normalize(matches)

#                 useful_cols = [
#                     "matchInfo.matchId",
#                     "matchInfo.seriesName",
#                     "matchInfo.matchDesc",
#                     "matchInfo.team1.teamName",
#                     "matchInfo.team2.teamName",
#                     "matchInfo.status",
#                     "matchInfo.venueInfo.ground",
#                     "matchInfo.venueInfo.city",
#                 ]
#                 df = df[[c for c in useful_cols if c in df.columns]]
#                 col_rename = {
#                     "matchInfo.matchId": "ID",
#                     "matchInfo.seriesName": "Series",
#                     "matchInfo.matchDesc": "Desc",
#                     "matchInfo.team1.teamName": "Team 1",
#                     "matchInfo.team2.teamName": "Team 2",
#                     "matchInfo.status": "Status",
#                     "matchInfo.venueInfo.ground": "Ground",
#                     "matchInfo.venueInfo.city": "City",
#                 }
#                 df = df.rename(columns=col_rename)

#                 st.success("✅ Live match data fetched successfully!")
#                 st.dataframe(df)
#             else:
#                 st.warning("⚠️ No match data found. Check the API structure.")
#         except Exception as e:
#             st.error(f"❌ API fetch failed: {e}")

# #Incase of upcoming matches
#     if st.button("Fetch upcoming matches"):
#         url = f"https://{RAPIDAPI_HOST}/matches/v1/upcoming"
#         headers = {
#             "X-RapidAPI-Host": RAPIDAPI_HOST,
#             "X-RapidAPI-Key": RAPIDAPI_KEY
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=15)
#             data = response.json()

#             matches = []
#             if "typeMatches" in data:
#                 for tm in data["typeMatches"]:
#                     for sm in tm.get("seriesMatches", []):
#                         series = sm.get("seriesAdWrapper", {})
#                         matches.extend(series.get("matches", []))

#             if matches:
#                 df = pd.json_normalize(matches)

#                 useful_cols = [
#                     "matchInfo.matchId",
#                     "matchInfo.seriesName",
#                     "matchInfo.matchDesc",
#                     "matchInfo.team1.teamName",
#                     "matchInfo.team2.teamName",
#                     "matchInfo.venueInfo.ground",
#                     "matchInfo.venueInfo.city",
#                 ]
#                 df = df[[c for c in useful_cols if c in df.columns]]
#                 col_rename = {
#                     "matchInfo.matchId": "ID",
#                     "matchInfo.seriesName": "Series",
#                     "matchInfo.matchDesc": "Desc",
#                     "matchInfo.team1.teamName": "Team 1",
#                     "matchInfo.team2.teamName": "Team 2",
#                     "matchInfo.venueInfo.ground": "Ground",
#                     "matchInfo.venueInfo.city": "City",
#                 }
#                 df = df.rename(columns=col_rename)

#                 st.success("✅ Live match data fetched successfully!")
#                 st.dataframe(df)
#             else:
#                 st.warning("⚠️ No match data found. Check the API structure.")
#         except Exception as e:
#             st.error(f"❌ API fetch failed: {e}")

# #Incase of recently completed matches
#     if st.button("Fetch recently completed matches"):  
#         url = f"https://{RAPIDAPI_HOST}/matches/v1/recent"
#         headers = {
#             "X-RapidAPI-Host": RAPIDAPI_HOST,
#             "X-RapidAPI-Key": RAPIDAPI_KEY
#         }

#         try:
#             response = requests.get(url, headers=headers, timeout=15)
#             data = response.json()

#             matches = []
#             if "typeMatches" in data:
#                 for tm in data["typeMatches"]:
#                     for sm in tm.get("seriesMatches", []):
#                         series = sm.get("seriesAdWrapper", {})
#                         matches.extend(series.get("matches", []))

#             if matches:
#                 df = pd.json_normalize(matches)

#                 useful_cols = [
#                     "matchInfo.matchId",
#                     "matchInfo.seriesName",
#                     "matchInfo.matchDesc",
#                     "matchInfo.team1.teamName",
#                     "matchInfo.team2.teamName",
#                     "matchInfo.status",
#                     "matchInfo.venueInfo.ground",
#                     "matchInfo.venueInfo.city",
#                 ]
#                 df = df[[c for c in useful_cols if c in df.columns]]
#                 col_rename = {
#                     "matchInfo.matchId": "ID",
#                     "matchInfo.seriesName": "Series",
#                     "matchInfo.matchDesc": "Desc",
#                     "matchInfo.team1.teamName": "Team 1",
#                     "matchInfo.team2.teamName": "Team 2",
#                     "matchInfo.status": "Status",
#                     "matchInfo.venueInfo.ground": "Ground",
#                     "matchInfo.venueInfo.city": "City",
#                 }
#                 df = df.rename(columns=col_rename)

#                 st.success("✅ Completed match data fetched successfully!")
#                 st.dataframe(df)
#             else:
#                 st.warning("⚠️ No match data found. Check the API structure.")          
#         except Exception as e:
#             st.error(f"❌ API fetch failed: {e}")


# pages/_1_Live_Matches.py
import streamlit as st
import requests
import pandas as pd

# 🔑 Replace with your RapidAPI Key
RAPIDAPI_KEY = "787f633245msha1e09df8c3ca801p1192cejsna2ba2b7cddb1"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"

st.set_page_config(page_title="Live Matches Dashboard", layout="wide")

def fetch_matches_with_score(endpoint):
    """Fetch matches (live/upcoming/recent) and include score if available."""
    url = f"https://{RAPIDAPI_HOST}/matches/v1/{endpoint}"
    headers = {"X-RapidAPI-Host": RAPIDAPI_HOST, "X-RapidAPI-Key": RAPIDAPI_KEY}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
    except Exception as e:
        st.error(f"❌ Failed to fetch data: {e}")
        return pd.DataFrame()

    matches_list = []
    if "typeMatches" in data:
        for tm in data["typeMatches"]:
            for sm in tm.get("seriesMatches", []):
                series = sm.get("seriesAdWrapper", {})
                for match in series.get("matches", []):
                    match_info = match.get("matchInfo", {})
                    match_score = match.get("matchScore", {})  # May be empty for upcoming
                    matches_list.append({
                        "ID": match_info.get("matchId"),
                        "Series": match_info.get("seriesName"),
                        "Desc": match_info.get("matchDesc"),
                        "Team 1": match_info.get("team1", {}).get("teamName"),
                        "Team 2": match_info.get("team2", {}).get("teamName"),
                        "Status": match_info.get("status"),
                        "Ground": match_info.get("venueInfo", {}).get("ground"),
                        "City": match_info.get("venueInfo", {}).get("city"),
                        "Score": match_score
                    })
    return pd.DataFrame(matches_list)

def app():
    st.title("📡 Cricket Matches Dashboard")

    endpoint = st.selectbox("Select Match Type", ["live", "upcoming", "recent"])
    
    df = fetch_matches_with_score(endpoint)
    if df.empty:
        st.warning("⚠️ No matches found.")
        return

    # Display basic match info in table
    st.subheader("Matches")
    st.dataframe(df[["Series", "Desc", "Team 1", "Team 2", "Status", "Ground", "City"]], use_container_width=True)

    # Select a match for detailed scorecard
    selected_index = st.selectbox(
        "Select a Match to View Scorecard",
        df.index,
        format_func=lambda x: f"{df.at[x,'Team 1']} vs {df.at[x,'Team 2']} | {df.at[x,'Desc']}"
    )

    score_data = df.at[selected_index, "Score"]
    st.subheader("Scorecard")
    
    if score_data:
        # Display structured scorecard
        for team_key in ["team1Score", "team2Score"]:
            team_score = score_data.get(team_key, {})
            if team_score:
                for innings_key, innings in team_score.items():
                    st.markdown(f"**{innings_key.upper()}**")
                    runs = innings.get("runs", 0)
                    wickets = innings.get("wickets", 0)
                    overs = innings.get("overs", 0)
                    st.write(f"Runs: {runs}, Wickets: {wickets}, Overs: {overs}")
    else:
        st.info("Scorecard not available yet for this match.")

