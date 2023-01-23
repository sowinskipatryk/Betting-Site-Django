const betButtons = document.getElementsByClassName('betbutton');
var betHeader = document.getElementById('betHeader');
var chosenBets = document.getElementById('chosenBets');
var submitButton = $('input[type="submit"]');
var userLogged = betHeader.dataset.logged == "true";
var betSummary = $('#betSummary');
var betOdds = $('#betOdds')[0];
var betPrize = $('#betPrize')[0];
var betStake = $('#betStake')[0];
var stakeRange = $('#stakeRange');

var betPicks = {}
var odds = 0.0

for (i=0; i<betButtons.length; i++) {
    betButtons[i].addEventListener('click', function(){
        var team = this.dataset.team
        var pick = this.dataset.pick
        var matchNum = this.dataset.match
        var odd = this.dataset.odd

        var data = {'pick': pick, 'team': team, 'odd': odd};

        if (betPicks[matchNum] !== undefined && betPicks[matchNum]['pick'] === data['pick']) {
            delete betPicks[matchNum];
            odds /= parseFloat(odd);
        }
        else {
            if (Object.keys(betPicks).length === 0) {
            odds = parseFloat(odd);
            }

            else if (betPicks[matchNum] !== undefined)
            {
            odds /= parseFloat(betPicks[matchNum]['odd'])
            odds *= parseFloat(odd)
            }
            else {
            odds *= parseFloat(odd)
            }
            betPicks[matchNum] = data
        }

        var betsNum = Object.keys(betPicks).length;

        if (userLogged) {

            betStake.textContent = "$"+stakeRange[0].value;
            betPrize.textContent = "$"+(Math.round(odds*stakeRange[0].value * 100) / 100)
            stakeRange[0].oninput = function() {
                betStake.textContent = "$"+this.value;
                betPrize.textContent = "$"+(Math.round(odds*this.value * 100) / 100)
            }

            odds = Math.round(odds * 100) / 100
            if (betsNum == 1) {
            betHeader.innerText = 'Single Bet'
            betOdds.innerText = odds.toString()
            submitButton.removeClass('d-none')
            betSummary.removeClass('d-none')
            stakeRange.removeClass('d-none')
            }
            else if (betsNum > 1) {
            betHeader.innerText = 'Multi Bet'
            betOdds.innerText = odds.toString()
            submitButton.removeClass('d-none')
            betSummary.removeClass('d-none')
            stakeRange.removeClass('d-none')
            }
            else {
            betHeader.innerText = 'Add first event to the coupon'
            submitButton.addClass('d-none');
            betSummary.addClass('d-none');
            stakeRange.addClass('d-none');
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