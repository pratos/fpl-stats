import os
import re
from datetime import date
from io import StringIO
from logging import debug

import pandas as pd
import requests
from dotenv import load_dotenv
from fastcore.foundation import L as flist
from loguru import logger
from requests.models import Response

from src.fbref.constants import FPL_URL_STATIC, STATS_AVAILABLE, TEAM_URLS
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

import boto3

if debug:
    logger.info(f"KEY: {os.getenv('DO_SPACES_KEY')}")
    logger.info(f"SECRET: {os.getenv('DO_SPACES_SECRET')}")

session = boto3.session.Session()
client = session.client(
    "s3",
    region_name="fra1",
    endpoint_url=os.getenv("DO_ENDPOINT"),
    aws_access_key_id=os.getenv("DO_SPACES_KEY"),
    aws_secret_access_key=os.getenv("DO_SPACES_SECRET"),
)


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


def load_file_to_do_spaces(dataframe: pd.DataFrame):
    t_now = re.sub(r"\D", "", str(date.today()))
    gameweek = check_live_gw()
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer)
    client.put_object(
        Bucket=os.getenv("DO_BUCKET"), Key=f"{t_now}_GW{gameweek}_fbref.csv", Body=csv_buffer.getvalue(), ACL="private"
    )


def check_live_gw():
    proxies = fetch_proxies(debug=False)
    try:
        all_fpl_data_raw = request_obj(url=FPL_URL_STATIC, proxies=proxies, via_proxy=True)
        if all_fpl_data_raw.status_code != 200:
            raise Exception
        all_fpl_data = all_fpl_data_raw.json()
        gameweek_list = flist(
            [{"gw": event["name"], "finished": event["finished"]} for event in all_fpl_data["events"]]
        )
        return gameweek_list.filter(lambda x: not x["finished"])[0]["gw"].split(" ")[1]
    except Exception as err:
        logger.exception(err)


def generate_csv(stats) -> pd.DataFrame:
    fbref_all = pd.DataFrame({})
    for team_stat in stats:
        team_lvl = pd.DataFrame({})
        logger.info(f"Formatting data for {team_stat['team'].title()}")
        for stats in STATS_AVAILABLE:
            if team_lvl.size == 0:
                team_lvl = pd.DataFrame(team_stat[stats])
            else:
                team_lvl = pd.merge(team_lvl, pd.DataFrame(team_stat[stats]), on=["name"])
        fbref_all = pd.concat([fbref_all, team_lvl])
    return fbref_all


def fetch_proxies(debug: bool = False):
    logger.info("Fetching proxies...")
    if debug:
        logger.info(f"URL ---> {os.getenv('PROXY_API_URL')}")

    proxy_response = requests.get(
        os.getenv("PROXY_API_URL"),
        headers={"Authorization": f"Token {os.getenv('PROXY_API_KEY')}"},
        timeout=120,
    )
    proxies = []
    if proxy_response.status_code == 200:
        proxies = [get_proxy_format(proxy_element=elem) for elem in proxy_response.json()["results"]]
    else:
        logger.error("[ERROR] Proxies couldn't be fetched")

    if debug:
        logger.debug(f"[FETCH] Proxies are:\n{proxies}")
    return proxies


def request_obj(url: str, proxies: list, via_proxy: bool) -> Response:
    if via_proxy:
        return requests.get(url, proxies={"http": proxies}, timeout=120)
    return requests.get(url, timeout=120)
