import json
# TODO Handle Soccer Teams/Players
# TODO Check Players, references spot check incomplete (Missing AJ Green)
import os
from os.path import dirname, realpath

from sportsreference.mlb.teams import Teams as MLBTeams
from sportsreference.nba.teams import Teams as NBATeams
from sportsreference.nfl.teams import Teams as NFLTeams
from sportsreference.nhl.teams import Teams as NHLTeams

from src.main.utils.nlp_conversion_util import NLPConversionUtil
from src.main.utils.nlp_resource_util import NLPResourceUtil
from src.main.utils.banter_dictionary_creator.sports_reference_scraper import SportsReferenceScraper
BASEDIR = os.path.abspath(os.path.dirname(os.path.dirname(dirname(realpath(__file__)))))
SAVE_LOCATION = '%s/resources/reference_dict' % BASEDIR

MLB_OUTFIELD_POSITIONS = ['LF', 'RF', 'OF', 'CF']
FANTASY_FOOTBALL_POSITIONS = ['QB', 'RB', 'WR', 'TE', 'K']

def get_position(player, league):
    if league == 'MLB':
        return get_position_mlb(player)
    elif league == 'NFL':
        return get_position_nfl(player)
    elif league == 'NBA':
        return get_position_nba(player)
    else:
        return ''

def get_position_mlb(player):
    try:
        positions = player._position
        if type(positions) == list:
            if positions[0] not in MLB_OUTFIELD_POSITIONS:
                return positions[0]
            else:
                return 'OF'
        else:
            if positions != '':
                if '/' in positions:
                    # CB/LB/RB
                    return positions.split('/')[0]
                else:
                    return positions
            else:
                return positions
    except:
        return ''

def get_position_nfl(player):
    is_every_position_empty = True
    try:
        positions = player._position
        if type(positions) == list:
            for index, position in enumerate(positions):
                if position.upper() in FANTASY_FOOTBALL_POSITIONS:
                    return position.upper()
                else:
                    if position != '':
                        is_every_position_empty = False
            if is_every_position_empty:
                return SportsReferenceScraper().scrape_nfl(player.player_id, FANTASY_FOOTBALL_POSITIONS)
            else:
                return ''
        else:
            if positions != '':
                if '/' in positions:
                    # CB/LB/RB
                    position = positions.split('/')[0]
                    if position in FANTASY_FOOTBALL_POSITIONS:
                        return position
                else:
                    if positions in FANTASY_FOOTBALL_POSITIONS:
                        return positions
                return ''
            else:
                return ''
    except:
        return ''

def get_position_nba(player):
    try:
        positions = player._position
        if type(positions) == list:
            if positions[0] not in FANTASY_FOOTBALL_POSITIONS:
                return positions[0]
            else:
                return 'OF'
        else:
            if positions != '':
                if '/' in positions:
                    # CB/LB/RB
                    return positions.split('/')[0]
                else:
                    return positions
            else:
                return positions
    except:
        return ''


def create_player_dict_on_teams(teams, league):
    player_dict = {}
    for team in teams:
        roster = team.roster
        for player in roster.players:
            try:
                position = get_position(player, league)
                player_dict[NLPConversionUtil().normalize_text(player.name)] = {"team": NLPConversionUtil().normalize_text(team.name),
                                                                                "position": NLPConversionUtil().normalize_text(
                                                                                    position)}
            except:
                # Some players have a name as None in sportsreference dict
                try:
                    position = get_position(player, league)
                    player_dict[NLPConversionUtil().normalize_text(player.name)] = {"team": NLPConversionUtil().normalize_text(team.name),
                                                "position": NLPConversionUtil().normalize_text(position)}
                except:
                    pass

    return player_dict


def save_dict(dictionary, file_name):
    tmp_json = json.dumps(dictionary)
    f = open(f"{SAVE_LOCATION}/{file_name}.json", "w")
    f.write(tmp_json)
    f.close()


def create_player_dict(modify_existing: bool, is_team_upper_case: False):
    if modify_existing:
        if is_team_upper_case:
            existing_dict = NLPResourceUtil().sports_player_dict
            nfl_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NFL"].items())
            nba_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NBA"].items())
            mlb_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["MLB"].items())
            nhl_upper = dict(
                (NLPConversionUtil().normalize_text(k), v.upper()) for k, v in existing_dict["NHL"].items())
            save_dict(nhl_upper, "NHL_player_dict")
            save_dict(nba_upper, "NBA_player_dict")
            save_dict(mlb_upper, "MLB_player_dict")
            save_dict(nfl_upper, "NFL_player_dict")
        else:
            existing_dict = NLPResourceUtil().sports_player_dict
            nfl_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NFL"].items())
            nba_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NBA"].items())
            mlb_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["MLB"].items())
            nhl_upper = dict((NLPConversionUtil().normalize_text(k), v) for k, v in existing_dict["NHL"].items())
            save_dict(nhl_upper, "NHL_player_dict")
            save_dict(nba_upper, "NBA_player_dict")
            save_dict(mlb_upper, "MLB_player_dict")
            save_dict(nfl_upper, "NFL_player_dict")


    else:
        try:
            teams = NHLTeams(2020)
            nhl_dict = create_player_dict_on_teams(teams, 'NHL')
            save_dict(nhl_dict, "NHL_player_dict")
        except:
            teams = NHLTeams(2019)
            nhl_dict = create_player_dict_on_teams(teams, 'NHL')
            save_dict(nhl_dict, "NHL_player_dict")
        try:
            teams = NBATeams(2020)
            nba_dict = create_player_dict_on_teams(teams, 'NBA')
            save_dict(nba_dict, "NBA_player_dict")
        except:
            teams = NBATeams(2019)
            nba_dict = create_player_dict_on_teams(teams, 'NBA')
            save_dict(nba_dict, "NBA_player_dict")
        try:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams, 'MLB')
            save_dict(mlb_dict, "MLB_player_dict")
        except:
            teams = MLBTeams(2019)
            mlb_dict = create_player_dict_on_teams(teams, 'MLB')
            save_dict(mlb_dict, "MLB_player_dict")

        try:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams, 'NFL')
            # SPOT FIX
            nfl_dict["AJ GREEN"] = {"team" : "CINCINNATI BENGALS",
                                    "position": "WR"}
            save_dict(nfl_dict, "NFL_player_dict")
        except:
            teams = NFLTeams(2019)
            nfl_dict = create_player_dict_on_teams(teams, 'NFL')
            # SPOT FIX
            nfl_dict["AJ GREEN"] = {"team" : "CINCINNATI BENGALS",
                                    "position": "WR"}
            save_dict(nfl_dict, "NFL_player_dict")


if __name__ == '__main__':
    teams = NBATeams(2019)
    nfl_dict = create_player_dict_on_teams(teams)
