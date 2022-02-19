// Rretrieve & parse data passed from HTML Template
const json_data = JSON.parse(document.getElementById('js_data').textContent);
const gameId = json_data.gameId
const update_interval = json_data.update_interval

// Update data as soon as the data is loaded
update()
// Update data at regular intervals
const game_update_interval = setInterval(update, update_interval);


/******************************************************************************
 * Fetches the JSON data for a specific game from the NBA Scores web app. This 
 * allows the data to be displayed in nearly real time without page refreshes.
 ******************************************************************************/
function update() {
    fetch(`./update_game/${gameId}`).then(convert_to_json).then(update_game)
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

/****************************************************************************
 * Displays the data in the given game dictionary that was obtained from the 
 * NBA Scores Web App. 
 * @param {JSON} game_dict  Dictionary containing a boxscore and actions
 *                          list for the game that is to be displayed
 ***************************************************************************/
function update_game(game_dict) {
    // Get individual dictionaries from the game dictionary
    let boxscore = game_dict['boxscore']
    let actions = game_dict['actions']

    // Display data relevant to all games
    document.getElementById('game_status_display').textContent = boxscore['gameStatusText'];
    document.getElementById('game_display').innerHTML = generate_game_html(boxscore);
    get_game_actions_html(actions)

    if (boxscore.gameStatus < 3) {
        // Display data specfic to games that are not finished
        document.getElementById('period').textContent = `Period: ${boxscore.period}`;
        document.getElementById('game_clock').textContent = `Game Clock: ${boxscore.gameClock}`;
        document.getElementById('last_action').textContent = `Last action: ${actions.at(-1).description}`;
    } else {
        // If the game is finished, stop querying for new data to conserve resources
        clearInterval(game_update_interval);
    }
}

/*************************************************************************************************
 * Generates and returns an HTML string used for displaying the data from the given boxscore.
 * @param {JSON} boxscore JSON object representing the current state of the game to be displayed
 * @returns HTML string representing the data from the given boxscore
 ************************************************************************************************/
function generate_game_html(boxscore) {
    return `
    <div class="col-lg-6">
            <div class="row">
                <div class="col">
                    <h4>${boxscore.awayTeam.teamName}</h4>
                </div>
                <div class="col">
                </div>
                <div class="col">
                    <h4>${boxscore.homeTeam.teamName}</h4>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <h4>${boxscore.awayTeam.score}</h4>
                </div>
                <div class="col">
                
                </div>
                <div class="col">
                    <h4>${boxscore.homeTeam.score}</h4>
                </div>
            </div>
            <div class="row">
                <div class="col">
                    <p>
                        ${boxscore.gameStatus == 2 ? "Timeouts: " + boxscore.homeTeam.timeoutsRemaining + "<br>": ""}
                        ${boxscore.gameStatus == 2 ? (boxscore.homeTeam.inBonus != 0 ? "Bonus" : "<br>") : ""}
                    <p>
                </div>
                <div class="col">

                </div>
                <div class="col">
                    <p>
                        ${boxscore.gameStatus == 2 ? "Timeouts: " + boxscore.awayTeam.timeoutsRemaining + "<br>": ""}
                        ${boxscore.gameStatus == 2 ? (boxscore.awayTeam.inBonus != 0 ? "Bonus" : "<br") : ""}
                    <p>
                </div>
            </div>
    </div>
    `
}

/****************************************************************************************************
 * Displays the data from the given game actions list that was obtained from the NBA Scores Web App. 
 * @param {Promise<JSON>[]} actions  List of JSON objects each containing the information regarding an action
 *                          that occured during the game to be displayed.
 ****************************************************************************************************/
function get_game_actions_html(actions) {
    let period = 0
    let links_html = ''
    let actions_html = ''

    // Display each action
    actions.forEach(action => {
        // Create new heading & link for new periods
        if (action.period != period) {
            period = action.period;

            // Create & append link HTML
            const link = document.createElement("a")
            link.href = `#period_${period}`
            link.textContent = `Period ${period}`
            link.className = "btn btn-info m-1"
            links_html += link.outerHTML

            // Create & append heading HTML
            const h4 = document.createElement("h4")
            h4.textContent = `Period ${period}`;
            h4.id = `period_${period}`
            actions_html += h4.outerHTML
        }
        if (action.description != 10) {
            // If description exists, create & append action HTML
            const p = document.createElement("p")
            p.textContent = `Clock: ${action.clock} | ${action.description} | Score: (${action.scoreAway} - ${action.scoreHome})`
            actions_html += p.outerHTML
        }
    });

    // Display actions and links
    document.getElementById('actions_display').innerHTML = actions_html;
    document.getElementById('actions_links').innerHTML = links_html;
}