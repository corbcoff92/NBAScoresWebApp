from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

import datetime

from NBA.forms import DateSelectorForm, HiddenGamePreferencesForm
from NBA.models import HiddenGamePreferences
from . import services


def index(request):
    '''
    Displays NBA Home page
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        HTTP response representing the NBA Home Page
    '''
    return render(request, 'NBA/index.html', {})


def games(request, gameStatus):
    '''
    Displays the current NBA games using data retrieved from the NBA API using the nba_api module.
    Games are filtered by the given game status. 
    Params:
        request: Instance representing the HTTP request that queried this view.
        gameStatus: Integer representing the game status with which to filter the displayed games.
    Returns:
        HTTP response representing the current NBA games.
    '''
    # Check if user is logged in & has selected to hide scores
    if request.user.is_authenticated:
        scores_hidden = HiddenGamePreferences.objects.get(
            user=request.user).hide_scores
    else:
        scores_hidden = False
    context = {
        'scores_hidden': scores_hidden,
        'js_data': {
            'gameStatus': gameStatus,
            'game_update_url': reverse("NBA:update_games"),
            'update_interval': services.GAMES_UPDATE_INTERVAL,
        }
    }
    return render(request, 'NBA/games.html', context)


def update_games(request):
    '''
    Retrives the information for and current NBA games from the NBA API using the nba_api 
    module. The information is returned using JSON format. This view acts as an intermediary 
    API between JavaScript and the NBA API that can be queried at regular intervals. This 
    allows the data to be displayed in real time, without the need for full page refreshes.
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        Json response representing data for any current NBA games.
    '''
    games = services.update_games()
    games = services.check_hide_games(games, request.user)
    context = {
        'games': games
    }
    return JsonResponse(context)


def game(request, gameId):
    '''
    Displays detailed information about the specific NBA game with the given game id. 
    Params:
        request: Instance representing the HTTP request that queried this view.
        gameId: String representing the game id of the game which is to be displayed.
    Returns:
        HTTP response representing the detailed NBA game.
    '''
    context = {
        'gameId': gameId,
        'js_data': {
            'gameId': gameId,
            'update_interval': services.GAME_UPDATE_INTERVAL,
        }
    }
    return render(request, 'NBA/game.html', context)


def update_game(request, gameId):
    '''
    Retrives the information for the NBA game with the given game id from the NBA API 
    using the nba_api module. The information is returned using JSON format. This view
    acts as an intermediary API between JavaScript and the NBA API that can be queried at
    regular intervals. This allows the data to be displayed in real time, without the 
    need for full page refreshes.
    Params:
        request: Instance representing the HTTP request that queried this view.
        gameId: String representing the game id of the game for which the data should be retrieved.
    Returns:
        Json response representing the detailed NBA game data.
    '''
    actions, boxscore = services.get_game_data(gameId)
    context = {
        'actions': actions,
        'boxscore': boxscore,
    }
    return JsonResponse(context)


def select_date(request):
    '''
    Displays a form allowing the user to select a date. 
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        HTTP response representing the date selection form if the form has
        not been submitted, otherwise a redirected HTTP response to display the
        game data for the specfic date.
    '''
    # Form has been submitted
    if request.method == "POST":
        date_form = DateSelectorForm(request.POST)

        # Form is valid
        if date_form.is_valid():
            date = date_form.cleaned_data['game_date']
            return redirect("NBA:schedule", date)
    else:
        date_form = DateSelectorForm()

    date_form = DateSelectorForm()
    return render(request, 'NBA/select_date.html', {})


def schedule(request, date):
    '''
    Displays the NBA games associated with the given date using data retrieved
    from the NBA API using the nba_api module.
    Params:
        request: Instance representing the HTTP request that queried this view.
        date: String representing the date for which the game data should be retreived.
    Returns:
        HTTP response representing the NBA games associated with the given date if the current
        date is not selected, otherwise an HTTP redirect to the current games page.
    '''
    # Check if current date is selected, if so redirect to current game page
    if date == str(datetime.datetime.now().date()):
        return redirect('NBA:games')
    else:
        # Check if user is logged in & if so, get hide scores preference
        if request.user.is_authenticated:
            scores_hidden = HiddenGamePreferences.objects.get(
                user=request.user).hide_scores
        else:
            scores_hidden = False
        # Get data from given date
        games = services.get_scheduled_games(date)
        games = services.check_hide_games(games, request.user)
        context = {
            'scores_hidden': scores_hidden,
            'date': date,
            'games': games,
        }
        return render(request, 'NBA/schedule.html', context)


@login_required
def hidden_games_settings(request):
    '''
    Displays a form used to display & alter the currently logged in user's hidden scores preferences. 
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        HTTP response representing the hidden games settings form if the form has
        not been submitted, otherwise a redirected HTTP response to the NBA current
        games page.
    '''
    # Get currently logged in user's hidden game preferences
    preferences_instance = HiddenGamePreferences.objects.get(user=request.user)

    # Create form with user's current preferences already filled in
    form = HiddenGamePreferencesForm(instance=preferences_instance)
    context = {
        'form': form,
    }

    # Form has not yet been submitted
    if request.method == "GET":
        return render(request, 'NBA/hidden_games_settings_form.html', context)
    # Form has been submitted
    elif request.method == "POST":
        form = HiddenGamePreferencesForm(
            request.POST, instance=preferences_instance)
        # Form has been submitted & is valid
        if form.is_valid():
            # Automaticall hide scores anytime the user change's their hidden scores criteria
            preferences_instance.hide_scores = True
            preferences = form.save()
            return redirect(reverse('NBA:games'))
        # Form has been submitted but is invalid
        else:
            return render(request, 'NBA/hidden_games_settings_form.html', context)


def toggle_hide_scores(request):
    '''
    View used for toggling whether or not the current user would like to reveal or hide
    scores based on their currently selected criteria.
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        Redirected HTTP response to the url from which this view was queried.
    '''
    # Ensure that user is logged in
    if request.user.is_authenticated:
        # Toggle & save user preference for whether or not scores should be hidden
        user_preferences = HiddenGamePreferences.objects.get(user=request.user)
        user_preferences.hide_scores = not user_preferences.hide_scores
        user_preferences.save()
    return redirect(request.META.get('HTTP_REFERER'))
