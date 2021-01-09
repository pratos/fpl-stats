import os

import requests
from dotenv import load_dotenv
from loguru import logger
from requests.models import Response

from src.fbref.constants import TEAM_URLS
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
from src.fbref.utilities import get_proxy_format

load_dotenv()


def run_fbref(via_proxy: bool = True, debug: bool = False) -> None:
    proxies = fetch_proxies(debug=debug)
    try:
        for team in TEAM_URLS.items():
            logger.info(f"[TEAM:{team[0].upper()}] Fetching data from Fbref")
            response = request_obj(
                team_url=team[1], proxies=proxies, via_proxy=via_proxy
            )

            shooting_stats = extract_shooting_stats(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Shooting stats: {shooting_stats[0]}"
            )

            passing_stats = extract_passing_stats(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Passing stats: {passing_stats[0]}"
            )

            extra_passing_stats = extract_extra_passing_stats(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Extra Passing stats: {extra_passing_stats[0]}"
            )

            gca_stats = extract_gca_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example GCA stats: {gca_stats[0]}")

            defensive_action_stats = extract_defensive_actions(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Def Action stats: {defensive_action_stats[0]}"
            )

            posession_stats = extract_possession_stats(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Possession stats: {posession_stats[0]}"
            )

            playing_time_stats = extract_playing_time_stats(response=response)
            logger.info(
                f"[TEAM:{team[0].upper()}] Example Playing time stats: {playing_time_stats[0]}"
            )

            misc_stats = extract_misc_stats(response=response)
            logger.info(f"[TEAM:{team[0].upper()}] Example Misc stats: {misc_stats[0]}")
    except Exception as err:
        logger.exception(err)


def fetch_proxies(debug: bool = False):
    logger.info("Fetching proxies...")
    proxy_response = requests.get(
        "https://proxy.webshare.io/api/proxy/list/?page=1",
        headers={"Authorization": f"Token {os.getenv('PROXY_API_KEY')}"},
        timeout=120,
    )
    proxies = []
    if proxy_response.status_code == 200:
        proxies = [
            get_proxy_format(proxy_element=elem)
            for elem in proxy_response.json()["results"]
        ]
    else:
        logger.error("[ERROR] Proxies couldn't be fetched")

    if debug:
        logger.debug(f"[FETCH] Proxies are:\n{proxies}")
    return proxies


def request_obj(team_url: str, proxies: list, via_proxy: bool) -> Response:
    if via_proxy:
        return requests.get(team_url, proxies={"http": proxies}, timeout=120)
    return requests.get(team_url, timeout=120)
