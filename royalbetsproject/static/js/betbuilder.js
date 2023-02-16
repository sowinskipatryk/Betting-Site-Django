const oddsButtons = document.getElementsByClassName('oddButton');
const betHeader = document.getElementById('betHeader');
const pickedBets = document.getElementById('pickedBets');
const placeBetButton = document.getElementById('placeBetButton');
const userLogged = betHeader.dataset.logged === "true";
const betSummary = document.getElementById('betSummary');
const betOdds = document.getElementById('betOdds');
const betPrize = document.getElementById('betPrize');
const betStake = document.getElementById('betStake');
const stakeInput = document.getElementById('stakeInput');
const betContent = document.getElementById('betContent');
const accountBalance = document.getElementById('accountBalance');

let betPicks = {};
let odds = 0.0;

function updateAccountBalance(value) {
    if (value < accBalance) {
    const floatVal = parseFloat(accBalance - value);
    const formatVal = floatVal.toFixed(2);
    accountBalance.innerText = "$" + formatVal;
    }
}

function checkBetNumber() {
    const betNum = Object.keys(betPicks).length;
    if (betNum == 1) {
    betHeader.innerText = 'Single Bet'
    betOdds.innerText = odds.toString()
    placeBetButton.classList.remove('d-none')
    betSummary.classList.remove('d-none')
    stakeInput.classList.remove('d-none')
    betContent.classList.add('p-3');
    }
    else if (betNum > 1) {
    betHeader.innerText = 'Multi Bet'
    betOdds.innerText = odds.toString()
    placeBetButton.classList.remove('d-none')
    betSummary.classList.remove('d-none')
    stakeInput.classList.remove('d-none')
    }
    else {
    setInitialState();
    }
}

function updateCouponStruct(picks) {
    let string = "";
    for (const [key, {pick, team, odd}] of Object.entries(picks)) {
      const betString = `
        <div class='betPick mb-1 rounded'>
          #<span class='matchIdInput'>${key}</span>
          Pick: <span class='matchPickInput'>${pick}</span>
          Team: ${team}
          <strong>${odd}</strong>
          <button type="button" class="btn btn-warning deleteBetBtn" onclick="deleteBet(${key}, ${odd}); console.log(betPicks);">X</button>
        </div>
      `;
      string += betString
    }
    pickedBets.innerHTML = string;
}

function deleteBet(id, odd) {
    delete betPicks[id];
    odds /= parseFloat(odd);
    odds = Math.round(odds * 100) / 100
    updateCouponStruct(betPicks)
    checkBetNumber()
}

function setInitialState() {
    betHeader.innerText = 'Add first event to the coupon';
    pickedBets.innerHTML = '';
    betContent.classList.remove('p-3');
    placeBetButton.classList.add('d-none');
    betSummary.classList.add('d-none');
    stakeInput.classList.add('d-none');
    betPicks = {};
    odds = 0.0;
}

for (i=0; i<oddsButtons.length; i++) {
    oddsButtons[i].addEventListener('click', function(){
        const team = this.dataset.team
        const pick = this.dataset.pick
        const matchNum = this.dataset.match
        const odd = this.dataset.odd

        const data = {'pick': pick, 'team': team, 'odd': odd};

        if (betPicks[matchNum] !== undefined && betPicks[matchNum]['pick'] === data['pick']) {
            deleteBet(matchNum, odd)
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

        if (userLogged) {

            betStake.textContent = "$"+stakeInput.value;
            betPrize.textContent = "$"+(Math.round(odds*stakeInput.value * 100) / 100)
            stakeInput.oninput = function() {
                betStake.textContent = "$"+this.value;
                betPrize.textContent = "$"+(Math.round(odds*this.value * 100) / 100)
            }

            odds = Math.round(odds * 100) / 100

            checkBetNumber()
            console.log(betPicks)

            updateCouponStruct(betPicks)
        }
    });
};

placeBetButton.addEventListener("click", function(event) {
    event.preventDefault();
    let xhr = new XMLHttpRequest();
    let url = "/coupon_submit/";
    xhr.open("POST", url, true);

    let betsInput = [];
    const typeInput = document.getElementById("typeInput");
    const matchPickInputs = $('.matchPickInput');
    const matchIdInputs = $('.matchIdInput');
    matchIdInputs.each(function(index, element) {
        const matchId = element.innerText;
        const matchPick = matchPickInputs[index].innerText;
        const obj = {'matchId': matchId, 'matchPick': matchPick};
        betsInput.push(obj);
    });

    let data = {
      'betsInput': betsInput,
      'stakeInput': stakeInput.value,
      'oddsInput': betOdds.innerText,
      'prizeInput': betPrize.innerText
    };

    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send(JSON.stringify(data));

    updateAccountBalance(stakeInput.value)
    setInitialState();
});