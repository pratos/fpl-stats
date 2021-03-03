from fastcore.basics import typed

from src.constants import CATEGORY_TYPES
from src.utilities import to_float


@typed
def extract_team_details(team: dict) -> dict:
    return {str(team["code"]): {"name": team["name"].lower().replace(" ", "_"), "slug": team["short_name"]}}


@typed
def extract_player_fpl_stats(player: dict, fpl_team_mapper: dict) -> dict:
    return {
        "player_id": player["id"],
        "name": f"{player['first_name']} {player['second_name']}",
        "display_slug": player["web_name"],
        "team_id": player["team"],
        "team": fpl_team_mapper.get(str(player["team_code"])).get("name"),
        "team_slug": fpl_team_mapper.get(str(player["team_code"])).get("slug"),
        "position": CATEGORY_TYPES.get(str(player["element_type"])),
        "points_per_game": to_float(player["points_per_game"]),
        "form": to_float(player["form"]),
        "news": player["news"],
        "news_added_at": player["news_added"],
        "status": player["status"],
        "total_points": player["total_points"],
        "value_form": to_float(player["value_form"]),
        "value_season": to_float(player["value_season"]),
        "selected_by_percent": to_float(player["selected_by_percent"]),
        "points_per_game": to_float(player["points_per_game"]),
        "influence_rank_overall": player["influence_rank"],
        "creativity_rank_overall": player["creativity_rank"],
        "threat_rank_overall": player["threat_rank"],
        "influence_rank_by_position": player["influence_rank_type"],
        "creativity_rank_by_position": player["creativity_rank_type"],
        "threat_rank_by_position:": player["threat_rank_type"],
        "ict_index": player["ict_index_rank"],
        "ict_index_by_position": player["ict_index_rank_type"],
        "dreamteam_count": player["dreamteam_count"],
        "transfers_in": player["transfers_in"],
        "transfers_out": player["transfers_out"],
        "chance_of_playing_next_round": player["chance_of_playing_next_round"],
        "chance_of_playing_this_round": player["chance_of_playing_this_round"],
        "cost_change_event": player["cost_change_event"],
        "cost_change_event_fall": player["cost_change_event_fall"],
        "cost_change_start": player["cost_change_start"],
        "cost_change_start_fall": player["cost_change_start_fall"],
        "ep_next": player["ep_next"],
        "ep_this": player["ep_this"],
        "now_cost": player["now_cost"],
        "transfers_in": player["transfers_in"],
        "transfers_out": player["transfers_out"],
        "transfers_in_event": player["transfers_in_event"],
        "transfers_out_event": player["transfers_out_event"],
        "goals_scored": player["goals_scored"],
        "assists": player["assists"],
        "clean_sheets": player["clean_sheets"],
        "goals_conceded": player["goals_conceded"],
        "penalties_saved": player["penalties_saved"],
        "penalties_missed": player["penalties_missed"],
        "saves": player["saves"],
        "bonus": player["bonus"],
        "bps": player["bps"],
        "corners_and_indirect_freekicks_order": player["corners_and_indirect_freekicks_order"],
        "corners_and_indirect_freekicks_text": player["corners_and_indirect_freekicks_text"],
        "direct_freekicks_order": player["direct_freekicks_order"],
        "direct_freekicks_text": player["direct_freekicks_text"],
        "penalties_order": player["penalties_order"],
        "penalties_text": player["penalties_text"],
    }
