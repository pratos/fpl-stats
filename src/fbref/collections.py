import collections

ShootingStats = collections.namedtuple(
    "ShootingStats",
    "name profile_url nationality position age minutes_90s goals shots_total shots_on_target \
    shots_on_target_pct shots_total_per90 goals_per_shot goals_per_shot_on_target \
    shots_free_kicks pens_made pens_att xg npxg npxg_per_shot xg_net npxg_net",
)

PassingStats = collections.namedtuple(
    "PassingStats",
    "name passes_completed passes passes_pct passes_total_distance passes_progressive_distance \
    passes_completed_short passes_short passes_pct_short passes_completed_medium passes_medium \
    passes_pct_medium passes_completed_long passes_long passes_pct_long assists xa xa_net assisted_shots \
    passes_into_final_third passes_into_penalty_area crosses_into_penalty_area progressive_passes",
)

ExtraPassingStats = collections.namedtuple(
    "ExtraPassingStats",
    "name passes_live passes_dead passes_free_kicks through_balls passes_pressure passes_switches\
    crosses corner_kicks corner_kicks_in corner_kicks_out corner_kicks_straight passes_ground\
    passes_low passes_high passes_left_foot passes_right_foot passes_head throw_ins passes_other_body\
    passes_completed passes_offsides passes_oob passes_intercepted passes_blocked",
)

GCAStats = collections.namedtuple(
    "GCAStats",
    "name sca sca_per90 sca_passes_live sca_passes_dead sca_dribbles sca_shots sca_fouled gca\
    gca_per90 gca_passes_live gca_passes_dead gca_dribbles gca_shots gca_fouled gca_og_for",
)

DefensiveActions = collections.namedtuple(
    "DefensiveActions",
    "name tackles tackles_won tackles_def_3rd tackles_mid_3rd tackles_att_3rd dribble_tackles dribbles_vs\
    dribble_tackles_pct dribbled_past pressures pressure_regains pressure_regain_pct pressures_def_3rd\
    pressures_mid_3rd pressures_att_3rd blocks blocked_shots blocked_shots_saves blocked_passes interceptions\
    tackles_interceptions clearances errors",
)

PossessionStats = collections.namedtuple(
    "PossessionStats",
    "name touches touches_def_pen_area touches_def_3rd touches_mid_3rd touches_att_3rd touches_att_pen_area\
    touches_live_ball dribbles_completed dribbles dribbles_completed_pct players_dribbled_past nutmegs\
    carries carry_distance carry_progressive_distance pass_targets passes_received passes_received_pct\
    miscontrols dispossessed",
)

PlayingTimeStats = collections.namedtuple(
    "PlayingTimeStats",
    "name games minutes minutes_per_game minutes_pct minutes_90s games_starts minutes_per_start\
    games_subs minutes_per_sub unused_subs points_per_match on_goals_for on_goals_against plus_minus\
    plus_minus_per90 plus_minus_wowy on_xg_for on_xg_against xg_plus_minus xg_plus_minus_per90\
    xg_plus_minus_wowy",
)

MiscStats = collections.namedtuple(
    "MiscStats",
    "name cards_yellow cards_red cards_yellow_red fouls fouled offsides crosses interceptions\
    tackles_won pens_won pens_conceded own_goals ball_recoveries aerials_won aerials_lost aerials_won_pct",
)
