import datetime
from django.urls import path
from . import views

app_name = 'NBA'
urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.games, name='games', kwargs={'gameStatus': 0}),
    path('games/scheduled/', views.games,
         name='scheduled', kwargs={"gameStatus": 1}),
    path('games/in_progress/', views.games,
         name='in_progress', kwargs={"gameStatus": 2}),
    path('games/finished/', views.games,
         name='finished', kwargs={"gameStatus": 3}),
    path('games/update_games/', views.update_games, name='update_games'),
    path('games/toggle_hide_scores/',
         views.toggle_hide_scores, name='toggle_hide_scores'),
    path('games/hidden_game_settings', views.hidden_games_settings,
         name='hidden_games_settings'),
    path('game/<str:gameId>', views.game, name='game'),
    path('game/update_game/<str:gameId>',
         views.update_game, name='update_game'),
    path('schedule/', views.select_date, name='select_date'),
    path('schedule/tomorrows_games', views.schedule, name='tomorrows_games', kwargs={'date':(datetime.datetime.today() + datetime.timedelta(days=1)).date()}),
    path('schedule/yesterdays_games', views.schedule, name='yesterdays_games', kwargs={'date':(datetime.datetime.today() - datetime.timedelta(days=1)).date()}),
    path('schedule/<str:date>', views.schedule, name='schedule'),
]
