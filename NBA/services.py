from random import randint
import datetime
from .utils import get_data

from .models import HiddenGamePreferences, Team

from nba_api.live.nba.endpoints import scoreboard as scoreboard_live, boxscore as boxscore_live, playbyplay as playbyplay_live
from nba_api.stats.endpoints import scoreboard as scoreboard_stats

GAMES_UPDATE_INTERVAL = 60000
GAME_UPDATE_INTERVAL = 30000

# Choose to simulate games using pickled data
SIMULATE = False
SIMULATE_PROGRESS = False

# If simulate is chosen, obtain the data from the pickled files
if SIMULATE:
    month = 2
    day = 15
    year = 2022
    time_slot = 10

    data_sim = get_data(month, day, year, time_slot)
    games_sim = data_sim['scoreboard_live'].games.get_dict()
    pbps_sim = data_sim['playbyplays_stats']

    if SIMULATE_PROGRESS:
        for game in games_sim:
            game['gameStatus'] = 1
            game['period'] = 1
            game['gameClockTime'] = datetime.timedelta(
                days=0, minutes=12, seconds=0)


def update_games():
    '''
    Queries the NBA API for data about any current NBA games using the nba_api module, 
    and returns the data as a list of dictionaries.
    Returns: List containing dictionaries representing any current NBA games.
    '''
    if SIMULATE:
        games = games_sim
        if SIMULATE_PROGRESS:
            simulate_progress(games_sim)
    else:
        games = scoreboard_live.ScoreBoard().games.get_dict()
    return games


def simulate_progress(games_sim):
    '''
    Used for simulating the given list of games. 
    Mostly deprecated since pickled data has been stored.
    '''
    for game in games_sim:
        if game['gameStatus'] == 1:
            if randint(0, 100) <= 5:
                game['gameStatus'] = 2
        elif game['gameStatus'] == 2:
            game['awayTeam']['score'] += randint(0, 4)
            game['homeTeam']['score'] += randint(0, 4)
            game['gameClockTime'] -= datetime.timedelta(minutes=randint(
                0, 1), seconds=randint(1, 59), microseconds=randint(0, 99))
            minutes, seconds, microseconds = game['gameClockTime'].seconds//60, game['gameClockTime'].seconds % 60, int(
                game['gameClockTime'].seconds % 60 % 60)
            game['gameStatusText'] = f"Q{game['period']}<br>{(str(minutes)+':') if minutes > 0 else ''}{seconds:02g}{('.'+str(microseconds)) if minutes <= 0 else ''}"
            if game['gameClockTime'] <= datetime.timedelta(minutes=0, seconds=0):
                if game['period'] >= 4 and game['homeTeam']['score'] != game['awayTeam']['score']:
                    game['gameStatus'] = 3
                    game['gameStatusText'] = 'Final'
                else:
                    game['gameClockTime'] = datetime.timedelta(
                        minutes=12, seconds=0)
                    game['period'] += 1


def get_game_data(gameID):
    '''
    Queries the NBA API for detailed data corresponding to the specific given game id using the nba_api module, 
    and returns the data sets as dictionaries.
    Returns: Dictionaries containing information about the specific NBA games.
    '''
    if not SIMULATE:
        # Obtain current data
        actions = playbyplay_live.PlayByPlay(gameID).get_dict()[
            'game']['actions']
        boxscore = boxscore_live.BoxScore(gameID).get_dict()['game']
    else:
        # Obtain pickled data
        actions = [pbp for pbp in data_sim['playbyplays_live'] if pbp.get_dict(
        )['game']['gameId'] == gameID][0].get_dict()['game']['actions']
        boxscore = [box for box in data_sim['boxscore_live'] if box.get_dict(
        )['game']['gameId'] == gameID][0].get_dict()['game']

    # Format boxscore data
    boxscore = parse_boxscore(boxscore)

    # Format actions data
    for action in actions:
        action['clock'] = parse_game_clock(action['clock'])

    return actions, boxscore


def get_scheduled_games(date):
    '''
    Queries the NBA API for data corresponding to the given date's games using the nba_api module, 
    and returns the data as a list of dictionaries.
    Returns: List of dictionaries containing information about the NBA games from the given date.
    '''
    # Obtain data
    game_data = scoreboard_stats.Scoreboard(
        game_date=str(date)).get_dict()['resultSets'][0]

    # Format data
    games_list = []
    for row in game_data['rowSet']:
        game = {}
        game['gameId'] = row[2]
        game['gameStatus'] = row[3]
        if game['gameStatus'] < 2:
            game['gameStatusText'] = row[4]
            game.update(
                homeTeam={'teamName': Team.objects.get(pk=row[6]).team_name})
            game.update(
                awayTeam={'teamName': Team.objects.get(pk=row[7]).team_name})
        else:
            game = boxscore_live.BoxScore(game['gameId']).get_dict()['game']
        games_list.append(game)
    return games_list


def update_team_models():
    from nba_api.stats.static import teams
    print(teams)


def check_hide_games(games, user):
    '''
    Used to hide the scores for the given games list, based on the criteria stored in the given user's account.
    Params: 
        games : List of dictionaries containing the information about the games that should be inspected.
        user : User account that should be used to determine whether or not the scores should be hidden.
    Returns:
        Modified list of games dictionaries.
    '''
    # Check if user is logged in
    if user.is_authenticated:
        user_preferences = HiddenGamePreferences.objects.get(user=user)
        # Check if user has decided to hide games
        if user_preferences.hide_scores:
            # Check each game against user's current hidden scores criteria
            for game in games:
                if game['gameStatus'] > 1:
                    score_difference = abs(
                        game['homeTeam']['score'] - game['awayTeam']['score'])
                    if (game['period'] >= user_preferences.hide_after_period and score_difference <= user_preferences.max_score_difference):
                        game['hidden'] = True
                    else:
                        game['hidden'] = False
        else:
            # Reset hidden game scores key in case user has decided to unhide games
            for game in games:
                game['hidden'] = False
    else:
        # Reset hidden game scores key in case user has decided to unhide games
        for game in games:
            game['hidden'] = False
    return games


def parse_boxscore(boxscore):
    '''
    Standardizes the keys and values for the given boxscore dictionary.
    Params:
        boxscore: Dictionary containing NBA game data.
    Returns:
        Standardized boxscore dictionary
    '''
    boxscore['gameClock'] = parse_game_clock(boxscore['gameClock'])
    if ":" in boxscore['gameStatusText']:
        boxscore['gameStatusText'] = "In Progress"
    return boxscore


def parse_game_clock(gameClock):
    '''
    Standardizes the given NBA game clock string.
    Params:
        gameClock: String containing the game clock as presnted by the NBA API
    Returns:
        String containing the standardized game clock for displaying.
    '''
    gameClock = gameClock.replace("PT", "").replace("M", ":").replace("S", "")
    minutes, seconds = gameClock.split(":")
    seconds, microseconds = seconds.split(".")
    minutes, seconds, microseconds = [
        int(val) for val in (minutes, seconds, microseconds)]
    return f"{(str(minutes)+':') if minutes > 0 else ''}{f'{seconds:02g}' if minutes > 0 else f'{seconds}'}{'.'+f'{microseconds:02g}' if minutes <= 0 else ''}"
