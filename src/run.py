from dotenv import load_dotenv
from loguru import logger

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
        load_file_to_do_spaces(dataframe=formatted_dataframe)
    except Exception as err:
        logger.exception(err)
