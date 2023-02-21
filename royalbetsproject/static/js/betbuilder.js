const oddsButtons = document.getElementsByClassName('oddButton');
const betHeader = document.getElementById('betHeader');
const pickedBets = document.getElementById('pickedBets');
const placeBetButton = document.getElementById('placeBetButton');
const userLogged = betHeader.dataset.logged === "true";
const betSummary = document.getElementById('betSummary');
const betOdds = document.getElementById('betOdds');
const betPrize = document.getElementById('betPrize');
const betStake = document.getElementById('betStake');
const betContent = document.getElementById('betContent');
const stakeInput = document.getElementById('stakeInput');
const accBalance = document.getElementById('accountBalance');

let betPicks = {};
let odds = 0.0;

function updateAccountBalance(balance) {
    const floatVal = parseFloat(balance);
    const formatVal = floatVal.toFixed(2);
    accBalance.innerText = "$" + formatVal;
}

function checkBetNumber() {
    const betNum = Object.keys(betPicks).length;
    if (betNum == 1) {
    betHeader.innerText = 'Single Bet';
    betOdds.innerText = odds.toString();
    placeBetButton.classList.remove('d-none');
    betSummary.classList.remove('d-none');
    stakeInput.classList.remove('d-none');
    betContent.classList.add('p-3');
    }
    else if (betNum > 1) {
    betHeader.innerText = 'Multi Bet';
    betOdds.innerText = odds.toString();
    placeBetButton.classList.remove('d-none');
    betSummary.classList.remove('d-none');
    stakeInput.classList.remove('d-none');
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
          <button type="button" class="btn btn-danger deleteBetBtn" onclick="deleteBet(${key}, ${odd});">X</button>
        </div>
      `;
      string += betString;
    }
    pickedBets.innerHTML = string;
}

function deleteBet(id, odd) {
    delete betPicks[id];
    odds /= parseFloat(odd);
    odds = Math.round(odds * 100) / 100;
    updateCouponStruct(betPicks);
    checkBetNumber();
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

function sendData() {
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
    xhr.onload = function() {
      if (xhr.status === 200) {
        var response = JSON.parse(xhr.responseText);
        if (response.status == 'success') {
          updateAccountBalance(response.accountBalance, stakeInput.value);
          setInitialState();
          alert('Coupon submitted successfully!');
        }
      }
    };
    xhr.send(JSON.stringify(data));
}

document.addEventListener('click', function(event){
    if (event.target.classList.contains('oddButton')) {
        const team = event.target.dataset.team;
        const pick = event.target.dataset.pick;
        const matchNum = event.target.dataset.match;
        const odd = event.target.dataset.odd;

        const data = {'pick': pick, 'team': team, 'odd': odd};

        if (betPicks[matchNum] !== undefined && betPicks[matchNum]['pick'] === data['pick']) {
            deleteBet(matchNum, odd);
        }
        else {
            if (Object.keys(betPicks).length === 0) {
            odds = parseFloat(odd);
            }

            else if (betPicks[matchNum] !== undefined)
            {
            odds /= parseFloat(betPicks[matchNum]['odd']);
            odds *= parseFloat(odd);
            }
            else {
            odds *= parseFloat(odd);
            }
            betPicks[matchNum] = data;
        }

        if (userLogged) {
            betStake.textContent = "$"+(parseFloat(stakeInput.value).toFixed(2));
            betPrize.textContent = "$"+((Math.round(odds*stakeInput.value * 100) / 100).toFixed(2));
            stakeInput.oninput = function() {
                betStake.textContent = "$"+(parseFloat(this.value).toFixed(2));
                betPrize.textContent = "$"+((Math.round(odds*this.value * 100) / 100).toFixed(2));
            }

            odds = Math.round(odds * 100) / 100;

            checkBetNumber();

            updateCouponStruct(betPicks);
        }
    }});

placeBetButton.addEventListener("click", function(event) {
    event.preventDefault();
    sendData();
});
