import os
import re
from datetime import date
from io import StringIO

import boto3
import pandas as pd
import requests
from fastcore.foundation import L as flist
from loguru import logger
from pipetools import pipe
from requests.models import Response

from src.constants import FPL_URL_STATIC, STATS_AVAILABLE


def build_client():
    session = boto3.session.Session()
    return session.client(
        "s3",
        region_name="fra1",
        endpoint_url=os.getenv("DO_ENDPOINT"),
        aws_access_key_id=os.getenv("DO_SPACES_KEY"),
        aws_secret_access_key=os.getenv("DO_SPACES_SECRET"),
    )


def format_age(age: str) -> str:
    try:
        spl = age.split("-")
        return f"{spl[0]} years and {spl[1]} days"
    except Exception:
        return "Age not known"


def to_float(text: str) -> float:
    if not text:
        return 0.0
    else:
        return text > pipe | str | float


def get_proxy_format(proxy_element: str):
    return f"http://{proxy_element['proxy_address']}:{proxy_element['ports']['http']}:{proxy_element['username']}:{proxy_element['password']}"


def load_file_to_do_spaces(dataframe: pd.DataFrame, source: str = "fbref"):
    t_now = re.sub(r"\D", "", str(date.today()))
    gameweek = check_live_gw()
    csv_buffer = StringIO()
    dataframe.to_csv(csv_buffer)
    build_client().put_object(
        Bucket=os.getenv("DO_BUCKET"),
        Key=f"{source}/{t_now}_GW{gameweek}_{source}.csv",
        Body=csv_buffer.getvalue(),
        ACL="private",
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
