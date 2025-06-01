import requests

API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.cricapi.com/v1"

def get_current_matches():
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"
    response = requests.get(url)
    data = response.json()

    if not data.get("data"):
        return "No current matches found."

    match_summaries = []
    for match in data["data"]:
        name = match.get("name")
        status = match.get("status")
        venue = match.get("venue")
        date = match.get("date")
        teams = " vs ".join(match.get("teams", []))

        score_lines = []
        for score in match.get("score", []):
            inning = score.get("inning", "Inning")
            runs = score.get("r", 0)
            wickets = score.get("w", 0)
            overs = score.get("o", 0)
            score_lines.append(f"{inning}: {runs}/{wickets} in {overs} overs")

        match_info = (
            f"🏏 **{name}**\n"
            f"📍 Venue: {venue}\n"
            f"🗓 Date: {date}\n"
            f"📊 Status: {status}\n"
            + "\n".join(score_lines)
        )
        match_summaries.append(match_info)

    return "\n\n".join(match_summaries)

def get_series(offset=0):
    try:
        url = f"{BASE_URL}/series?apikey={API_KEY}&offset={offset}"
        res = requests.get(url).json()
        if res.get("status") != "success":
            return "Failed to fetch series."
        series = res.get("data", [])
        if not series:
            return "No series found."
        return "\n".join([f"{s['name']} ({s['startDate']} to {s['endDate']})" for s in series])
    except Exception as e:
        return f"Failed to fetch series: {str(e)}"

def search_player(player_name):
    try:
        url = f"{BASE_URL}/players?apikey={API_KEY}&offset=0&search={player_name}"
        res = requests.get(url).json()
        if res.get("status") != "success":
            return "Failed to fetch player data."
        players = res.get("data", [])
        if not players:
            return "No players found."
        return "\n".join([f"{p['name']} - {p['country']}" for p in players])
    except Exception as e:
        return f"Failed to fetch player: {str(e)}"
