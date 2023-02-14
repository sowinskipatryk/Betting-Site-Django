const betButtons = document.getElementsByClassName('betButton');
var betHeader = document.getElementById('betHeader');
var chosenBets = document.getElementById('chosenBets');
var submitButton = $('input[type="submit"]');
var userLogged = betHeader.dataset.logged == "true";
var betSummary = $('#betSummary');
var betOdds = $('#betOdds')[0];
var betPrize = $('#betPrize')[0];
var betStake = $('#betStake')[0];
var stakeInput = $('#stakeInput');
var betContent = $('#betContent');

var betPicks = {}
var odds = 0.0

function setInitialState() {
    betHeader.innerText = 'Add first event to the coupon';
    chosenBets.innerHTML = '';
    betContent.removeClass('p-3');
    submitButton.addClass('d-none');
    betSummary.addClass('d-none');
    stakeInput.addClass('d-none');
    betPicks = {};
    odds = 0.0;
}

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

            betStake.textContent = "$"+stakeInput[0].value;
            betPrize.textContent = "$"+(Math.round(odds*stakeInput[0].value * 100) / 100)
            stakeInput[0].oninput = function() {
                betStake.textContent = "$"+this.value;
                betPrize.textContent = "$"+(Math.round(odds*this.value * 100) / 100)
            }

            odds = Math.round(odds * 100) / 100
            if (betsNum == 1) {
            betHeader.innerText = 'Single Bet'
            betOdds.innerText = odds.toString()
            submitButton.removeClass('d-none')
            betSummary.removeClass('d-none')
            stakeInput.removeClass('d-none')
            betContent.addClass('p-3');
            }
            else if (betsNum > 1) {
            betHeader.innerText = 'Multi Bet'
            betOdds.innerText = odds.toString()
            submitButton.removeClass('d-none')
            betSummary.removeClass('d-none')
            stakeInput.removeClass('d-none')
            }
            else {
            setInitialState();
            }

            var string = "";
            for (const [key, value] of Object.entries(betPicks)) {
                betString = "<div class='betPick mb-1 rounded'>" + "#<span class='matchIdInput'>" + key + "</span>  Pick: <span class='matchPickInput'>" + value['pick'] + "</span>  Team: " + value['team'] + " <strong>" + value['odd'] + "</strong></div>"
                string += betString
                }
            chosenBets.innerHTML = string;
        }
    });
};

submitButton[0].addEventListener("click", function(event) {
    event.preventDefault();
    let xhr = new XMLHttpRequest();
    let url = "/coupon_submit/";
    xhr.open("POST", url, true);

    var betsInput = [];
    var typeInput = document.getElementById("typeInput");
    var matchPickInputs = $('.matchPickInput');
    var matchIdInputs = $('.matchIdInput');
    matchIdInputs.each(function(index, element) {
        var matchId = element.innerText;
        var matchPick = matchPickInputs[index].innerText;
        var obj = {'matchId': matchId, 'matchPick': matchPick};
        betsInput.push(obj);
    });

    let data = {
      'betsInput': betsInput,
      'stakeInput': stakeInput[0].value,
      'oddsInput': betOdds.innerText,
      'prizeInput': betPrize.innerText
    };

    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));

    setInitialState();
});