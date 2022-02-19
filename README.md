# Overview
This web app displays current NBA data. The data is fetched from the NBA's API using the nba_api API Client which can be installed using `pip` (Python's 
built-in package manager). The app presently displays scores & game actions for past & present games, as well as futurely scheduled NBA games. The NBA 
API is queried at regular intervals, and displayed to the user through a series of dynamic webpages that were created using Python's Django web framwork. 
The current data is provided to the webpages using a form of AJAX through JSON data, allowing the data to be displayed in real-time without the need of 
full-page refreshes.

The NBA Scores Web App includes a user managment system, and provides the ability to hide scores based on criteria that can be customized. 
This criteria is stored for each user, allowing the preferences to remain between sessions. This functionality allows the user the ability to find NBA 
games without spoilers.

This web app was written to assist with and demonstrate the learning of basic web development using Python's Django web framework. It also facilitated the 
learning of basic JavaScript, API queries, and dynamically generated HTML pages. The web app was developed using Django's built-in test server. This test 
server can be created and accessed through Django's provided command-line utility, using the command `python manage.py runserver` from the web app's working
directory. After initiaing this command, the website can then be accessed using the url `http://127.0.0.1:8000/NBA/`. This url displays the home page of the 
NBA Scores Web App.

A demonstration of the app is provided here: [NBA Scores Web App Demonstration Video](https://youtu.be/vyL-GwbTPJI)

# Web Pages
The created web pages include:
* Today's Games
    - This page displays the current NBA games, including scheduled games , games in progress, and finished games. 
    - Includes subpages that filters today's games to by each of these categories.
* Schedule
    - This page displays either futurely scheduled games or games that have been completed in the past. The date is chosen by the user. If the user selects the current day, they are automatically redirected to Today's Games.
    - Includes shortcut subpages for displaying the game's for tomorrow or yesterday.
* Game Detail Pages
    - Each displayed game that is either in progress or finished provides a link to a custom page that displays the details for that specific game. These details include a list of all of the actions that have occured during that game.
* User Managment Related Pages
    - These include pages for login, logout, a dashboard, and a webpage that allows the user to select their custom hidden scores criteria.
* Each page that displays game scores provides the ability to toggle hiding the game scores based on the specfic user provided criteria. The only exception to this is the game detail pages. This allows the user the ability to view the scores for any specifc game, essentially "bypassing" their hidden score preferences for very specific games of their choosing. 

# Development Environment
* Python 3.10.1
* nba_api | V1.1.11
* JavaScript
* Bootstrap CDN version 3.3.7
* Visual Studio Code | Version: 1.64.2

# Useful Websites

* [Django Official Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/) (Official Tutorial Site)
* [Django Tutorial—RealPython](https://realpython.com/get-started-with-django-1/) (Tutorial)
* [Django Tutorial—TutorialsPoint](https://www.tutorialspoint.com/django/index.htm) (Tutorial Site)
* [Django 2.2 Tutorial For Beginners](https://www.youtube.com/watch?v=OSBOZdwMCNw) (YouTube Video Tutorial)

# Future Work
* Additional hidden scores criteria and customization
* Ability to select individual scores to hide/unhide, and remain between user sessions.
* Populate home page with NBA news articles
* Populate user dashboard with additional customizations