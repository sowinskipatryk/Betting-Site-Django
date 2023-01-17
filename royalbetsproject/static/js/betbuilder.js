const betButtons = document.getElementsByClassName('betbutton');
var betHeader = document.getElementById('betHeader');
var chosenBets = document.getElementById('chosenBets');
var userLogged = betHeader.dataset.logged == "true"

var betPicks = {}

for (i=0; i<betButtons.length; i++) {
    betButtons[i].addEventListener('click', function(){
        var team = this.dataset.team
        var pick = this.dataset.pick
        var matchNum = this.dataset.match
        var odd = this.dataset.odd

        var data = {'pick': pick, 'team': team, 'odd': odd};

        if (betPicks[matchNum] !== undefined && betPicks[matchNum]['pick'] === data['pick']) {
            delete betPicks[matchNum];
        }
        else {
            betPicks[matchNum] = data
        }

        var betsNum = Object.keys(betPicks).length;

        if (userLogged) {
            if (betsNum == 1) {
            betHeader.innerText = 'Single Bet'}
            else if (betsNum > 1) {
            betHeader.innerText = 'Multi Bet'}
            else {
            betHeader.innerText = 'Dodaj pierwsze zdarzenie do kuponu'
            }

            var string = "";
            for (const [key, value] of Object.entries(betPicks)) {
                betString = "<div id='betPick' class='mb-1 rounded'>" + "#" + key + "  Pick: " + value['pick'] + "  Team: " + value['team'] + " <strong>" + value['odd'] + "</strong></div>"
                string += betString
                }
            chosenBets.innerHTML = string;
        }
    });
};