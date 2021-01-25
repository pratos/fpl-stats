import pandas as pd
from dotenv import load_dotenv
from fastcore.foundation import L as flist
from loguru import logger

from constants import FPL_URL_STATIC
from fpl.downloader import extract_player_fpl_stats, extract_team_details
from src.constants import TEAM_URLS
from src.fbref.scraper import (
    extract_defensive_actions,
    extract_extra_passing_stats,
    extract_gca_stats,
    extract_misc_stats,
    extract_passing_stats,
    extract_playing_time_stats,
    extract_possession_stats,
    extract_shooting_stats,
)
from src.utilities import (
    fetch_proxies,
    generate_csv,
    load_file_to_do_spaces,
    request_obj,
)

load_dotenv()


def run_fpl_official(via_proxy: bool = False, debug: bool = False) -> None:
    fpl_team_mapper = {}
    proxies = fetch_proxies(debug=debug)
    try:
        fpl_request = request_obj(url=FPL_URL_STATIC, proxies=proxies, via_proxy=via_proxy)
        all_fpl_data = fpl_request.json()
        fpl_players = flist(all_fpl_data["elements"])
        fpl_teams = flist(all_fpl_data["teams"])
        [fpl_team_mapper.update(extract_team_details(team)) for team in fpl_teams]
        fpl_player_stats = flist(
            [extract_player_fpl_stats(player=player, fpl_team_mapper=fpl_team_mapper) for player in fpl_players]
        )
        fpl_player_stats_df = pd.DataFrame.from_dict(fpl_player_stats)
        load_file_to_do_spaces(dataframe=fpl_player_stats_df, source="fpl_official")
    except Exception as err:
        logger.exception(err)


def run_fbref(via_proxy: bool = False, debug: bool = False) -> None:
    proxies = fetch_proxies(debug=debug)
    team_details = []
    try:
        for team in TEAM_URLS.items():
            logger.info(f"[TEAM:{team[0].upper()}] Fetching data from Fbref")
            response = request_obj(url=team[1], proxies=proxies, via_proxy=via_proxy)

            shooting_stats = extract_shooting_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Shooting stats: {shooting_stats[0]}")

            passing_stats = extract_passing_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Passing stats: {passing_stats[0]}")

            extra_passing_stats = extract_extra_passing_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Extra Passing stats: {extra_passing_stats[0]}")

            gca_stats = extract_gca_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example GCA stats: {gca_stats[0]}")

            defensive_action_stats = extract_defensive_actions(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Def Action stats: {defensive_action_stats[0]}")

            posession_stats = extract_possession_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Possession stats: {posession_stats[0]}")

            playing_time_stats = extract_playing_time_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Playing time stats: {playing_time_stats[0]}")

            misc_stats = extract_misc_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Misc stats: {misc_stats[0]}")

            team_details.append(
                {
                    "team": team[0].upper(),
                    "fbref_url": team[1],
                    "shooting_stats": shooting_stats,
                    "passing_stats": passing_stats,
                    "extra_passing_stats": extra_passing_stats,
                    "gca_stats": gca_stats,
                    "defensive_action_stats": defensive_action_stats,
                    "possession_stats": posession_stats,
                    "playing_time_stats": playing_time_stats,
                    "misc_stats": misc_stats,
                }
            )
        formatted_dataframe = generate_csv(stats=team_details)
        load_file_to_do_spaces(dataframe=formatted_dataframe, source="fbref")
    except Exception as err:
        logger.exception(err)
