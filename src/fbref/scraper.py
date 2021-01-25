from bs4 import BeautifulSoup
from fastcore.basics import typed
from loguru import logger
from requests.models import Response

from fbref.constants import (
    FBREF_DEF_ACTIONS,
    FBREF_GCA,
    FBREF_MISC,
    FBREF_PASSING,
    FBREF_PLAYING_TIME,
    FBREF_POSSESSION,
    FBREF_SHOOTING,
    FBREF_XTRA_PASSING,
)
from src.fbref.collections import (
    DefensiveActions,
    ExtraPassingStats,
    GCAStats,
    MiscStats,
    PassingStats,
    PlayingTimeStats,
    PossessionStats,
    ShootingStats,
)
from src.fbref.utilities import format_age, to_float


@typed
def extract_shooting_stats(response: Response) -> list:
    try:
        shooting_stats = []
        shooting = BeautifulSoup(response.content, features="lxml").find(
            attrs={"id": FBREF_SHOOTING}
        )
        shooting = BeautifulSoup(shooting.contents[4], features="lxml").find_all("tr")[2:-2]

        for stat in shooting:
            shooting_stats.append(
                ShootingStats(
                    name=(stat.find("th").text),
                    profile_url=f'https://fbref.com{stat.find("a").attrs["href"]}',
                    nationality=stat.find(attrs={"data-stat": "nationality"}).text.split(
                        " "
                    ),
                    position=stat.find(attrs={"data-stat": "position"}).text,
                    age=format_age(stat.find(attrs={"data-stat": "age"}).text),
                    minutes_90s=float(stat.find(attrs={"data-stat": "minutes_90s"}).text),
                    goals=int(stat.find(attrs={"data-stat": "goals"}).text),
                    shots_total=int(stat.find(attrs={"data-stat": "shots_total"}).text),
                    shots_on_target=int(
                        stat.find(attrs={"data-stat": "shots_on_target"}).text
                    ),
                    shots_on_target_pct=to_float(
                        stat.find(attrs={"data-stat": "shots_on_target_pct"}).text
                    ),
                    shots_total_per90=to_float(
                        stat.find(attrs={"data-stat": "shots_total_per90"}).text
                    ),
                    goals_per_shot=to_float(
                        stat.find(attrs={"data-stat": "goals_per_shot"}).text
                    ),
                    goals_per_shot_on_target=to_float(
                        stat.find(attrs={"data-stat": "goals_per_shot_on_target"}).text
                    ),
                    shots_free_kicks=to_float(
                        stat.find(attrs={"data-stat": "shots_free_kicks"}).text
                    ),
                    pens_made=int(stat.find(attrs={"data-stat": "pens_made"}).text),
                    pens_att=int(stat.find(attrs={"data-stat": "pens_att"}).text),
                    xg=to_float(stat.find(attrs={"data-stat": "xg"}).text),
                    npxg=to_float(stat.find(attrs={"data-stat": "npxg"}).text),
                    npxg_per_shot=to_float(
                        stat.find(attrs={"data-stat": "npxg_per_shot"}).text
                    ),
                    xg_net=stat.find(attrs={"data-stat": "xg_net"}).text,
                    npxg_net=stat.find(attrs={"data-stat": "npxg_net"}).text,
                )
            )
        return shooting_stats
    except Exception as err:
        logger.exception(err)


@typed
def extract_passing_stats(response: Response) -> list:
    passing_stats = []

    passing = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_PASSING}
    )
    passing = BeautifulSoup(passing.contents[4], features="lxml").find_all("tr")[2:-2]

    for stat in passing:
        passing_stats.append(
            PassingStats(
                name=stat.find("th").text,
                passes_completed=int(
                    stat.find(attrs={"data-stat": "passes_completed"}).text
                ),
                passes=int(stat.find(attrs={"data-stat": "passes"}).text),
                passes_pct=to_float(stat.find(attrs={"data-stat": "passes_pct"}).text),
                passes_total_distance=to_float(
                    stat.find(attrs={"data-stat": "passes_total_distance"}).text
                ),
                passes_progressive_distance=to_float(
                    stat.find(attrs={"data-stat": "passes_progressive_distance"}).text
                ),
                passes_completed_short=int(
                    stat.find(attrs={"data-stat": "passes_completed_short"}).text
                ),
                passes_short=int(stat.find(attrs={"data-stat": "passes_short"}).text),
                passes_pct_short=to_float(
                    stat.find(attrs={"data-stat": "passes_pct_short"}).text
                ),
                passes_completed_medium=int(
                    stat.find(attrs={"data-stat": "passes_completed_medium"}).text
                ),
                passes_medium=int(stat.find(attrs={"data-stat": "passes_medium"}).text),
                passes_pct_medium=to_float(
                    stat.find(attrs={"data-stat": "passes_pct_medium"}).text
                ),
                passes_completed_long=int(
                    stat.find(attrs={"data-stat": "passes_completed_long"}).text
                ),
                passes_long=int(stat.find(attrs={"data-stat": "passes_long"}).text),
                passes_pct_long=to_float(
                    stat.find(attrs={"data-stat": "passes_pct_long"}).text
                ),
                assists=int(stat.find(attrs={"data-stat": "assists"}).text),
                xa=to_float(stat.find(attrs={"data-stat": "xa"}).text),
                xa_net=stat.find(attrs={"data-stat": "xa_net"}).text,
                assisted_shots=int(
                    stat.find(attrs={"data-stat": "assisted_shots"}).text
                ),
                passes_into_final_third=int(
                    stat.find(attrs={"data-stat": "passes_into_final_third"}).text
                ),
                passes_into_penalty_area=int(
                    stat.find(attrs={"data-stat": "passes_into_penalty_area"}).text
                ),
                crosses_into_penalty_area=int(
                    stat.find(attrs={"data-stat": "crosses_into_penalty_area"}).text
                ),
                progressive_passes=int(
                    stat.find(attrs={"data-stat": "progressive_passes"}).text
                ),
            )
        )
    return passing_stats


@typed
def extract_extra_passing_stats(response: Response) -> list:
    extra_passing_stats = []

    extra_passing = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_XTRA_PASSING}
    )
    extra_passing = BeautifulSoup(extra_passing.contents[4], features="lxml").find_all(
        "tr"
    )[2:-2]

    for stat in extra_passing:
        extra_passing_stats.append(
            ExtraPassingStats(
                name=stat.find("th").text,
                passes_live=int(stat.find(attrs={"data-stat": "passes_live"}).text),
                passes_dead=int(stat.find(attrs={"data-stat": "passes_dead"}).text),
                passes_free_kicks=int(
                    stat.find(attrs={"data-stat": "passes_free_kicks"}).text
                ),
                through_balls=int(stat.find(attrs={"data-stat": "through_balls"}).text),
                passes_pressure=int(
                    stat.find(attrs={"data-stat": "passes_pressure"}).text
                ),
                passes_switches=int(
                    stat.find(attrs={"data-stat": "passes_switches"}).text
                ),
                crosses=int(stat.find(attrs={"data-stat": "crosses"}).text),
                corner_kicks=int(stat.find(attrs={"data-stat": "corner_kicks"}).text),
                corner_kicks_in=int(
                    stat.find(attrs={"data-stat": "corner_kicks_in"}).text
                ),
                corner_kicks_out=int(
                    stat.find(attrs={"data-stat": "corner_kicks_out"}).text
                ),
                corner_kicks_straight=int(
                    stat.find(attrs={"data-stat": "corner_kicks_straight"}).text
                ),
                passes_ground=int(stat.find(attrs={"data-stat": "passes_ground"}).text),
                passes_low=int(stat.find(attrs={"data-stat": "passes_low"}).text),
                passes_high=int(stat.find(attrs={"data-stat": "passes_high"}).text),
                passes_left_foot=int(
                    stat.find(attrs={"data-stat": "passes_left_foot"}).text
                ),
                passes_right_foot=int(
                    stat.find(attrs={"data-stat": "passes_right_foot"}).text
                ),
                passes_head=int(stat.find(attrs={"data-stat": "passes_head"}).text),
                throw_ins=int(stat.find(attrs={"data-stat": "throw_ins"}).text),
                passes_other_body=int(
                    stat.find(attrs={"data-stat": "passes_other_body"}).text
                ),
                passes_completed=int(
                    stat.find(attrs={"data-stat": "passes_completed"}).text
                ),
                passes_offsides=int(
                    stat.find(attrs={"data-stat": "passes_offsides"}).text
                ),
                passes_oob=int(stat.find(attrs={"data-stat": "passes_oob"}).text),
                passes_intercepted=int(
                    stat.find(attrs={"data-stat": "passes_intercepted"}).text
                ),
                passes_blocked=int(
                    stat.find(attrs={"data-stat": "passes_blocked"}).text
                ),
            )
        )
    return extra_passing_stats


@typed
def extract_gca_stats(response: Response) -> list:
    gca_stats = []
    gca = BeautifulSoup(response.content, features="lxml").find(attrs={"id": FBREF_GCA})
    gca = BeautifulSoup(gca.contents[4], features="lxml").find_all("tr")[2:-2]

    for stat in gca:
        gca_stats.append(
            GCAStats(
                name=stat.find("th").text,
                sca=int(stat.find(attrs={"data-stat": "sca"}).text),
                sca_per90=to_float(stat.find(attrs={"data-stat": "sca_per90"}).text),
                sca_passes_live=int(
                    stat.find(attrs={"data-stat": "sca_passes_live"}).text
                ),
                sca_passes_dead=int(
                    stat.find(attrs={"data-stat": "sca_passes_dead"}).text
                ),
                sca_dribbles=int(stat.find(attrs={"data-stat": "sca_dribbles"}).text),
                sca_shots=int(stat.find(attrs={"data-stat": "sca_shots"}).text),
                sca_fouled=int(stat.find(attrs={"data-stat": "sca_fouled"}).text),
                gca=int(stat.find(attrs={"data-stat": "gca"}).text),
                gca_per90=to_float(stat.find(attrs={"data-stat": "gca_per90"}).text),
                gca_passes_live=int(
                    stat.find(attrs={"data-stat": "gca_passes_live"}).text
                ),
                gca_passes_dead=int(
                    stat.find(attrs={"data-stat": "gca_passes_dead"}).text
                ),
                gca_dribbles=int(stat.find(attrs={"data-stat": "gca_dribbles"}).text),
                gca_shots=int(stat.find(attrs={"data-stat": "gca_shots"}).text),
                gca_fouled=int(stat.find(attrs={"data-stat": "gca_fouled"}).text),
                gca_og_for=int(stat.find(attrs={"data-stat": "gca_og_for"}).text),
            )
        )
    return gca_stats


@typed
def extract_defensive_actions(response: Response) -> list:
    defensive_actions = []
    defensive = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_DEF_ACTIONS}
    )
    defensive = BeautifulSoup(defensive.contents[4], features="lxml").find_all("tr")[
        2:-2
    ]

    for stat in defensive:
        defensive_actions.append(
            DefensiveActions(
                name=stat.find("th").text,
                tackles=int(stat.find(attrs={"data-stat": "tackles"}).text),
                tackles_won=int(stat.find(attrs={"data-stat": "tackles_won"}).text),
                tackles_def_3rd=int(
                    stat.find(attrs={"data-stat": "tackles_def_3rd"}).text
                ),
                tackles_mid_3rd=int(
                    stat.find(attrs={"data-stat": "tackles_mid_3rd"}).text
                ),
                tackles_att_3rd=int(
                    stat.find(attrs={"data-stat": "tackles_att_3rd"}).text
                ),
                dribble_tackles=int(
                    stat.find(attrs={"data-stat": "dribble_tackles"}).text
                ),
                dribbles_vs=int(stat.find(attrs={"data-stat": "dribbles_vs"}).text),
                dribble_tackles_pct=to_float(
                    stat.find(attrs={"data-stat": "dribble_tackles_pct"}).text
                ),
                dribbled_past=int(stat.find(attrs={"data-stat": "dribbled_past"}).text),
                pressures=int(stat.find(attrs={"data-stat": "pressures"}).text),
                pressure_regains=int(
                    stat.find(attrs={"data-stat": "pressure_regains"}).text
                ),
                pressure_regain_pct=to_float(
                    stat.find(attrs={"data-stat": "pressure_regain_pct"}).text
                ),
                pressures_def_3rd=int(
                    stat.find(attrs={"data-stat": "pressures_def_3rd"}).text
                ),
                pressures_mid_3rd=int(
                    stat.find(attrs={"data-stat": "pressures_mid_3rd"}).text
                ),
                pressures_att_3rd=int(
                    stat.find(attrs={"data-stat": "pressures_att_3rd"}).text
                ),
                blocks=int(stat.find(attrs={"data-stat": "blocks"}).text),
                blocked_shots=int(stat.find(attrs={"data-stat": "blocked_shots"}).text),
                blocked_shots_saves=int(
                    stat.find(attrs={"data-stat": "blocked_shots_saves"}).text
                ),
                blocked_passes=int(
                    stat.find(attrs={"data-stat": "blocked_passes"}).text
                ),
                interceptions=int(stat.find(attrs={"data-stat": "interceptions"}).text),
                tackles_interceptions=int(
                    stat.find(attrs={"data-stat": "tackles_interceptions"}).text
                ),
                clearances=int(stat.find(attrs={"data-stat": "clearances"}).text),
                errors=int(stat.find(attrs={"data-stat": "errors"}).text),
            )
        )
    return defensive_actions


@typed
def extract_possession_stats(response: Response) -> list:
    possesion_stats = []
    possesion = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_POSSESSION}
    )
    possesion = BeautifulSoup(possesion.contents[4], features="lxml").find_all("tr")[
        2:-2
    ]

    for stat in possesion:
        possesion_stats.append(
            PossessionStats(
                name=stat.find("th").text,
                touches=int(stat.find(attrs={"data-stat": "touches"}).text),
                touches_def_pen_area=int(
                    stat.find(attrs={"data-stat": "touches_def_pen_area"}).text
                ),
                touches_def_3rd=int(
                    stat.find(attrs={"data-stat": "touches_def_3rd"}).text
                ),
                touches_mid_3rd=int(
                    stat.find(attrs={"data-stat": "touches_mid_3rd"}).text
                ),
                touches_att_3rd=int(
                    stat.find(attrs={"data-stat": "touches_att_3rd"}).text
                ),
                touches_att_pen_area=int(
                    stat.find(attrs={"data-stat": "touches_att_pen_area"}).text
                ),
                touches_live_ball=int(
                    stat.find(attrs={"data-stat": "touches_live_ball"}).text
                ),
                dribbles_completed=int(
                    stat.find(attrs={"data-stat": "dribbles_completed"}).text
                ),
                dribbles=int(stat.find(attrs={"data-stat": "dribbles"}).text),
                dribbles_completed_pct=to_float(
                    stat.find(attrs={"data-stat": "dribbles_completed_pct"}).text
                ),
                players_dribbled_past=int(
                    stat.find(attrs={"data-stat": "players_dribbled_past"}).text
                ),
                nutmegs=int(stat.find(attrs={"data-stat": "nutmegs"}).text),
                carries=int(stat.find(attrs={"data-stat": "carries"}).text),
                carry_distance=int(
                    stat.find(attrs={"data-stat": "carry_distance"}).text
                ),
                carry_progressive_distance=int(
                    stat.find(attrs={"data-stat": "carry_progressive_distance"}).text
                ),
                pass_targets=int(stat.find(attrs={"data-stat": "pass_targets"}).text),
                passes_received=int(
                    stat.find(attrs={"data-stat": "passes_received"}).text
                ),
                passes_received_pct=to_float(
                    stat.find(attrs={"data-stat": "passes_received_pct"}).text
                ),
                miscontrols=int(stat.find(attrs={"data-stat": "miscontrols"}).text),
                dispossessed=int(stat.find(attrs={"data-stat": "dispossessed"}).text),
            )
        )
    return possesion_stats


@typed
def extract_playing_time_stats(response: Response) -> list:
    playing_time_stats = []
    playing_time = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_PLAYING_TIME}
    )
    playing_time = BeautifulSoup(playing_time.contents[4], features="lxml").find_all(
        "tr"
    )[2:-2]

    for stat in playing_time:
        playing_time_stats.append(
            PlayingTimeStats(
                name=stat.find("th").text,
                games=int(stat.find(attrs={"data-stat": "games"}).text),
                minutes=to_float(
                    stat.find(attrs={"data-stat": "minutes"}).text.replace(",", "")
                ),
                minutes_per_game=to_float(
                    stat.find(attrs={"data-stat": "minutes_per_game"}).text
                ),
                minutes_pct=to_float(
                    stat.find(attrs={"data-stat": "minutes_pct"}).text
                ),
                minutes_90s=to_float(
                    stat.find(attrs={"data-stat": "minutes_90s"}).text
                ),
                games_starts=int(stat.find(attrs={"data-stat": "games_starts"}).text),
                minutes_per_start=to_float(
                    stat.find(attrs={"data-stat": "minutes_per_start"}).text
                ),
                games_subs=int(stat.find(attrs={"data-stat": "games_subs"}).text),
                minutes_per_sub=to_float(
                    stat.find(attrs={"data-stat": "minutes_per_sub"}).text
                ),
                unused_subs=int(stat.find(attrs={"data-stat": "unused_subs"}).text),
                points_per_match=to_float(
                    stat.find(attrs={"data-stat": "points_per_match"}).text
                ),
                on_goals_for=to_float(
                    stat.find(attrs={"data-stat": "on_goals_for"}).text
                ),
                on_goals_against=to_float(
                    stat.find(attrs={"data-stat": "on_goals_against"}).text
                ),
                plus_minus=stat.find(attrs={"data-stat": "plus_minus"}).text,
                plus_minus_per90=stat.find(
                    attrs={"data-stat": "plus_minus_per90"}
                ).text,
                plus_minus_wowy=stat.find(attrs={"data-stat": "plus_minus_wowy"}).text,
                on_xg_for=to_float(stat.find(attrs={"data-stat": "on_xg_for"}).text),
                on_xg_against=to_float(
                    stat.find(attrs={"data-stat": "on_xg_against"}).text
                ),
                xg_plus_minus=stat.find(attrs={"data-stat": "xg_plus_minus"}).text,
                xg_plus_minus_per90=stat.find(
                    attrs={"data-stat": "xg_plus_minus_per90"}
                ).text,
                xg_plus_minus_wowy=stat.find(
                    attrs={"data-stat": "xg_plus_minus_wowy"}
                ).text,
            )
        )
    return playing_time_stats


@typed
def extract_misc_stats(response: Response) -> list:
    misc_stats = []
    misc = BeautifulSoup(response.content, features="lxml").find(
        attrs={"id": FBREF_MISC}
    )
    misc = BeautifulSoup(misc.contents[4], features="lxml").find_all("tr")[2:-2]

    for stat in misc:
        misc_stats.append(
            MiscStats(
                name=stat.find("th").text,
                cards_yellow=int(stat.find(attrs={"data-stat": "cards_yellow"}).text),
                cards_red=int(stat.find(attrs={"data-stat": "cards_red"}).text),
                cards_yellow_red=int(
                    stat.find(attrs={"data-stat": "cards_yellow_red"}).text
                ),
                fouls=int(stat.find(attrs={"data-stat": "fouls"}).text),
                fouled=int(stat.find(attrs={"data-stat": "fouled"}).text),
                offsides=int(stat.find(attrs={"data-stat": "offsides"}).text),
                crosses=int(stat.find(attrs={"data-stat": "crosses"}).text),
                interceptions=int(stat.find(attrs={"data-stat": "interceptions"}).text),
                tackles_won=int(stat.find(attrs={"data-stat": "tackles_won"}).text),
                pens_won=int(stat.find(attrs={"data-stat": "pens_won"}).text),
                pens_conceded=int(stat.find(attrs={"data-stat": "pens_conceded"}).text),
                own_goals=int(stat.find(attrs={"data-stat": "own_goals"}).text),
                ball_recoveries=int(
                    stat.find(attrs={"data-stat": "ball_recoveries"}).text
                ),
                aerials_won=int(stat.find(attrs={"data-stat": "aerials_won"}).text),
                aerials_lost=int(stat.find(attrs={"data-stat": "aerials_lost"}).text),
                aerials_won_pct=to_float(
                    stat.find(attrs={"data-stat": "aerials_won_pct"}).text
                ),
            )
        )
    return misc_stats
