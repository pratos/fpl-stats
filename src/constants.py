from pathlib import Path

TEAM_URLS = {
    "liverpool": "https://fbref.com/en/squads/822bd0ba/Liverpool-Stats",
    "aston_villa": "https://fbref.com/en/squads/8602292d/Aston-Villa-Stats",
    "leeds_united": "https://fbref.com/en/squads/5bfb9659/Leeds-United-Stats",
    "crystal_palace": "https://fbref.com/en/squads/47c64c55/Crystal-Palace-Stats",
    "chelsea": "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats",
    "leicester_city": "https://fbref.com/en/squads/a2d435b3/Leicester-City-Stats",
    "wolves": "https://fbref.com/en/squads/8cec06e1/Wolverhampton-Wanderers-Stats",
    "tottenham_hotspurs": "https://fbref.com/en/squads/361ca564/Tottenham-Hotspur-Stats",
    "westham_united": "https://fbref.com/en/squads/7c21e445/West-Ham-United-Stats",
    "manchester_city": "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats",
    "everton": "https://fbref.com/en/squads/d3fd31cc/Everton-Stats",
    "southampton": "https://fbref.com/en/squads/33c895d4/Southampton-Stats",
    "newcastle_united": "https://fbref.com/en/squads/b2b47a98/Newcastle-United-Stats",
    "manchester_united": "https://fbref.com/en/squads/19538871/Manchester-United-Stats",
    "brighton": "https://fbref.com/en/squads/d07537b9/Brighton-and-Hove-Albion-Stats",
    "westbrom": "https://fbref.com/en/squads/60c6b05f/West-Bromwich-Albion-Stats",
    "burnley": "https://fbref.com/en/squads/943e8050/Burnley-Stats",
    "sheffield_united": "https://fbref.com/en/squads/1df6b87e/Sheffield-United-Stats",
    "fulham": "https://fbref.com/en/squads/fd962109/Fulham-Stats",
    "arsenal": "https://fbref.com/en/squads/18bb7c10/Arsenal-Stats",
}

FBREF_SHOOTING = "all_stats_shooting_10728"
FBREF_PASSING = "all_stats_passing_10728"
FBREF_XTRA_PASSING = "all_stats_passing_types_10728"
FBREF_GCA = "all_stats_gca_10728"
FBREF_DEF_ACTIONS = "all_stats_defense_10728"
FBREF_POSSESSION = "all_stats_possession_10728"
FBREF_PLAYING_TIME = "all_stats_playing_time_10728"
FBREF_MISC = "all_stats_misc_10728"

STATS_AVAILABLE = [
    "shooting_stats",
    "passing_stats",
    "extra_passing_stats",
    "gca_stats",
    "defensive_action_stats",
    "possession_stats",
    "playing_time_stats",
    "misc_stats",
]

CATEGORY_TYPES = {"1": "GKP", "2": "DEF", "3": "MID", "4": "FWD"}

ROOT_DIRECTORY = Path(__file__).parents[2]
FBREF_DATA = Path(ROOT_DIRECTORY / "data/fbref-data")
FPL_DATA = Path(ROOT_DIRECTORY / "data/fpl-data")
FPL_URL_STATIC = "https://fantasy.premierleague.com/api/bootstrap-static/"
