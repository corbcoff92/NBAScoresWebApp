from nba_api.live.nba.endpoints import scoreboard as board_live
from nba_api.live.nba.endpoints import playbyplay as pbp_live
from nba_api.live.nba.endpoints import boxscore as box_live
from nba_api.stats.endpoints import scoreboard as board_stats
from nba_api.stats.endpoints import playbyplay as pbp_stats

import pickle as pkl
import os
import time
import datetime

day_offset = 0


def _change_dirs():
    '''
    Redirects the os to a newly created time directory used for storing pickled data. 
    Also returns the current directory so that the os can be redirected again later.
    Returns: The directory from which this method was called.
    '''
    current_dir = os.getcwd()
    os.chdir("NBA/pickled_objects")
    date = datetime.datetime.now().date()
    t = time.strftime("%I_%M_%p", time.localtime())
    year = date.year
    month = date.month
    day = date.day
    path = f"{year}/{month}/{day}/{t}"
    for dir in path.split("/"):
        if not os.path.exists(dir):
            os.mkdir(dir)
        os.chdir(dir)
    return current_dir


def _pkl_stats_nba_data():
    '''
    Pickles the stats data provided by the nba_api module.
    '''
    board = board_stats.Scoreboard(day_offset)
    _pkl_stats_scoreboard(board)
    _pkl_stats_playbyplay(board)


def _pkl_live_nba_data():
    '''
    Pickles the live data provided by the nba_api module.
    '''
    board = board_live.ScoreBoard()
    _pkl_live_scoreboard(board)
    _pkl_live_playbyplay(board)
    _pkl_live_boxscore(board)


def _pkl_live_scoreboard(board):
    '''
    Pickles the live scoreboard data provided by the nba_api module.
    Params:
        board: nba_api Scoreboard object to be pickled
    '''
    with open(f'scoreboard_live.pkl', 'wb') as file:
        pkl.dump(board, file)


def _pkl_stats_scoreboard(board):
    '''
    Pickles the stats scoreboard data provided by the nba_api module.
    Params:
        board: nba_api Scoreboard object to be pickled
    '''
    with open(f'scoreboard_stats.pkl', 'wb') as file:
        pkl.dump(board, file)


def _pkl_live_playbyplay(board):
    '''
    Pickles the live play by play data provided by the nba_api module.
    Params:
        board: nba_api Scoreboard object containing the games to be pickled
    '''
    pbps = []
    for game in board.games.get_dict():
        if game['gameStatus'] == 2:
            pbp = pbp_live.PlayByPlay(game['gameId'])
            pbps.append(pbp)
    if pbps:
        with open(f'playbyplays_live.pkl', 'wb') as file:
            pkl.dump(pbps, file)


def _pkl_stats_playbyplay(board):
    '''
    Pickles the stats play by play data provided by the nba_api module.
    Params:
        board: nba_api Scoreboard object containing the games to be pickled
    '''
    pbps = []
    for row in board.get_dict()['resultSets'][0]['rowSet']:
        pbp = pbp_stats.PlayByPlay(row[2])
        pbps.append(pbp)
    if pbps:
        with open(f'playbyplays_stats.pkl', 'wb') as file:
            pkl.dump(pbps, file)


def _pkl_live_boxscore(board):
    '''
    Pickles the live boxscore data provided by the nba_api module.
    Params:
        board: nba_api Scoreboard object containing the games to be pickled
    '''
    boxes = []
    for game in board.games.get_dict():
        if game['gameStatus'] == 2:
            box = box_live.BoxScore(game['gameId'])
            boxes.append(box)
    if boxes:
        with open(f'boxscore_live.pkl', 'wb') as file:
            pkl.dump(boxes, file)


def pkl_current_nba_data():
    '''
    Pickles the current NBA data provided by the nba_api module.
    The data is pickled in newly created directories representing 
    the date and time that the data was retrieved.
    '''
    current_dir = _change_dirs()
    _pkl_live_nba_data()
    _pkl_stats_nba_data()
    os.chdir(current_dir)


def get_data(month, day, year, time_slot):
    '''
    Gets the data from the pickled data directory specified by the given parameters.
    Params:
        month: Integer representing the Month directory from which the data should be retrieved
        day: Integer representing the day directory from which the data should be retrieved
        year: Integer representing the year directory from which the data should be retrieved
        time_slot: Integer representing the index of the time directory from which the data should be retrieved
    '''
    dir = f"NBA/pickled_objects/{year}/{month}/{day}/"
    t = os.listdir(dir)[time_slot-1]
    path = f"{dir}/{t}"
    data = {}
    for file in os.listdir(path):
        with open(f"{path}/{file}", 'rb') as file:
            file_name = file.name.split("/")[-1].split(".")[0]
            data[file_name] = pkl.load(file)
    return data
