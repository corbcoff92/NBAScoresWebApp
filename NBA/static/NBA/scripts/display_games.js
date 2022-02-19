// Rretrieve & parse data passed from HTML Template
const json_data = JSON.parse(document.getElementById('js_data').textContent);
const gameStatus = json_data.gameStatus;
const game_update_url = json_data.game_update_url;
const update_interval = json_data.update_interval

// Update data as soon as the data is loaded
update()
// Update data at regular intervals
const games_update_interval = setInterval(update, update_interval)

/********************************************************************************
 * Fetches the JSON data for the current games from the NBA Scores web app. This 
 * allows the data to be displayed in nearly real time without page refreshes.
 ********************************************************************************/
function update() {
    fetch(game_update_url).then(convert_to_json).then(update_games)
}


/*************************************************************
 * Converts the given response into a JSON object.
 * @param {Request} response    Response that is to be 
 *                              converted into a JSON promise
 * @returns Response parsed to JSON object.
 *************************************************************/
function convert_to_json(response) {
    return response.json();
}

/**************************************************************************************
 * Displays the data in the given games dictionary that was obtained from the 
 * NBA Scores Web App. 
 * @param {JSON} game_dict  Dictionary containing a list of game data to be displayed.
 *                          list for the game that is to be displayed
 **************************************************************************************/
function update_games(games_dict) {
    // Get games list from the games dictionary
    let games = games_dict['games'];

    // If gameStatus parsed from the HTML template is not 0
    if (gameStatus != 0) {
        // Filter games by gameStatus
        games = games.filter((game) => game.gameStatus == gameStatus);
    }

    let html = "";
    // If games list is not empty, display the games
    if (games.length != 0) {
        html = games.map(get_game_html).join('');
        // Otherwise display a message indicatiing that there are no games to display
    } else {
        let type = ""
        switch (gameStatus) {
            case 1:
                type = "No scheduled games to display right now..."
                break;
            case 2:
                type = "There are currently no games in progress..."
                break;
            case 3:
                type = "No finished games to display yet..."
                break;
        }
        html = `<h5>${type}</h5>`;
    }
    document.getElementById('games_display').innerHTML = html;
}

/***********************************************************************************************
 * Generates an HTML string representing the given game that is to be displayed.
 * @param {JSON} game JSON object containing information about the game that is to be displayed
 * @returns HTML string representing the game that is to be displayed.
 ***********************************************************************************************/
function get_game_html(game) {
    let html = ''
    // Check if game is hidden
    if (game.hidden == true) {
        html = generate_hidden_game_html(game);
        // Otherwise select game display type based on game status
    } else {
        switch (game['gameStatus']) {
            case 1:
                html = generate_pregame_game_html(game)
                break;
            case 2:
                html = generate_in_progress_game_html(game)
                break;
            case 3:
                html = generate_finished_game_html(game)
                break;
        }
    }
    return html
}

/************************************************************************************************************
 * Generates and returns an HTML string used for displaying the state of the given game before it has begun.
 * @param {JSON} game JSON object representing the current state of the game to be displayed.
 * @returns HTML string representing the data from the given game that is to be displayed.
 ************************************************************************************************************/
function generate_pregame_game_html(game) {
    return `
    <div class="col-lg-6 border rounded bg-secondary">
        <div class="card-body container" align="center">
            <div class="row card-title">
                <div class="col">
                    <h5>${game.awayTeam.teamName}</h5>
                </div>
                <div class="col">
                    <h6>vs.</h6>
                </div>
                <div class="col">
                    <h5>${game.homeTeam.teamName}</h5>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <h5>${game.gameStatusText}</h5>
                </div>
            </div>
        </div>
    </div>
    `
}

/****************************************************************************************************************
 * Generates and returns an HTML string used for displaying the state of the given game while it is in progress.
 * @param {JSON} game JSON object representing the current state of the game to be displayed.
 * @returns HTML string representing the data from the given game that is to be displayed.
 ****************************************************************************************************************/
function generate_in_progress_game_html(game) {
    return `
    <div class="col-lg-6 border rounded bg-secondary">
        <div class="card-body container">
            <h5 class="card-title">${game.gameStatusText}</h5>
            <div class="row card-title">
                <div class="col">
                    <h4>${game.awayTeam.teamTricode}</h4>
                </div>
                <div class="col">
                    
                </div>
                <div class="col">
                    <h4>${game.homeTeam.teamTricode}</h4>
                </div>
            </div>
            <div class="row card-title">
                <div class="col">
                    <h4>${game.awayTeam.score}</h4>
                </div>
                <div class="col">
                
                </div>
                <div class="col">
                    <h4>${game.homeTeam.score}</h4>
                </div>
            </div>
            <div class="row card-title">
                <div class="col">
                    <p>
                        Timeouts: ${game.homeTeam.timeoutsRemaining}<br>
                        ${(game.homeTeam.inBonus != 0 ? "Bonus" : "<br>")}
                    <p>
                </div>
                <div class="col">

                </div>
                <div class="col">
                    <p>
                        Timeouts: ${game.awayTeam.timeoutsRemaining}<br>
                        ${(game.awayTeam.inBonus != 0 ? "Bonus" : "<br")}
                    <p>
                </div>
            </div>
            <div class="row">
                <a href="/NBA/game/${game.gameId}" class="btn btn-info">Details</a>
            </div>
        </div>
    </div>
    `
}

/***************************************************************************************************************
 * Generates and returns an HTML string used for displaying the state of the given game after it has finiished.
 * @param {JSON} game JSON object representing the current state of the game to be displayed.
 * @returns HTML string representing the data from the given game that is to be displayed.
 ***************************************************************************************************************/
function generate_finished_game_html(game) {
    return `
    <div class="col-lg-6 border rounded bg-secondary">
        <div class="card-body container" align="center">
            <h5 class="card-title">${game.gameStatusText}</h5>
            <div class="row card-title">
                <div class="col">
                    <h5>${game.awayTeam.teamTricode}</h5>
                </div>
                <div class="col">
                    
                </div>
                <div class="col">
                    <h5>${game.homeTeam.teamTricode}</h5>
                </div>
            </div>
            <div class="row card-title">
                <div class="col">
                    <h4>${game.awayTeam.score}</h4>
                </div>
                <div class="col">
                </div>
                <div class="col">
                    <h4>${game.homeTeam.score}</h4>
                </div>
            </div>
            <div class="row">
                <a href="/NBA/game/${game.gameId}" class="btn btn-info">Details</a>
            </div>
        </div>
    </div>
    `
}

/**********************************************************************************************************************
 * Generates and returns an HTML string used for displaying the state of the given game whose scores should be hidden.
 * @param {JSON} game JSON object representing the current state of the game to be displayed.
 * @returns HTML string representing the data from the given game that is to be displayed.
 **********************************************************************************************************************/
function generate_hidden_game_html(game) {
    console.log("hidden");
    return `
    <div class="col-lg-6 border rounded bg-secondary">
        <div class="card-body container" align="center">
            <h5 class="card-title">Hidden</h5>
            <div class="row card-title">
            </div>
            <div class="row card-title">
                <div class="col">
                    <h5>${game.awayTeam.teamTricode}</h5>
                </div>
                <div class="col">

                </div>
                <div class="col">
                    <h5>${game.homeTeam.teamTricode}</h5>
                </div>
            </div>
            <div class="row card-title">
                <div class="col">
                    <h4>-</h4>
                </div>
                <div class="col">
                </div>
                <div class="col">
                    <h4>-</h4>
                </div>
            </div>
            <div class="row">
                <a href="/NBA/game/${game.gameId}" class="btn btn-info">Details</a>
            </div>
        </div>
    </div>
    `
}