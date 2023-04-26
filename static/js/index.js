document.getElementById("PeopleButton").addEventListener('click', ButtonPressed);
document.getElementById("DisableTraffic").addEventListener('click', DisableTraffic);
document.getElementById("EnableTraffic").addEventListener('click', EnableTraffic);
document.getElementById("NextState").addEventListener('click', NextState);
document.getElementById("PrevState").addEventListener('click', PrevState);
document.getElementById("BrakeTraffic").addEventListener('click', BrakeTraffic);

setInterval(UpdateTraffic, 1000);

CarRed = document.getElementById("CarRed");
CarYellow = document.getElementById("CarYellow");
CarGreen = document.getElementById("CarGreen");

PeopleRed = document.getElementById("PeopleRed");
PeopleGreen = document.getElementById("PeopleGreen");

TimerInfo = document.getElementById("TimerInfo");

TimerRange = document.getElementById("TimerSetting");
TimerRange.addEventListener('input', OnChangeTimer);
TimerRangeText = document.getElementById("TimerSettingText");

InfoText = document.getElementById("InfoText");

function NextState()
{
    fetch(document.location.protocol + "//" + document.location.host + "/NextState", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
}

function PrevState()
{
    fetch(document.location.protocol + "//" + document.location.host + "/PrevState", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
}

function BrakeTraffic()
{
    fetch(document.location.protocol + "//" + document.location.host + "/BrakeTraffic", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
}

function DisableTraffic()
{
    fetch(document.location.protocol + "//" + document.location.host + "/ToggleTraffic/0", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(obj => {console.log(obj)});
}

function EnableTraffic()
{
    fetch(document.location.protocol + "//" + document.location.host + "/ToggleTraffic/1", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(obj => {console.log(obj)});
}

var InfoTimer = 0;

function ClearInfoText()
{
    InfoText.innerText = "";
    InfoTimer = 0;
}

function ButtonPressed()
{
    fetch(document.location.protocol + "//" + document.location.host + "/PeopleRequest", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(obj => {
        InfoText.innerText = obj.ButtonResponse;
        
        if (InfoTimer != 0) clearTimeout(InfoTimer);
        InfoTimer = setTimeout(ClearInfoText, 5000);
    });
}

function ClearTraffic(element)
{
    element.classList.remove("bg-dark");
    element.classList.remove("bg-danger");
    element.classList.remove("bg-warning");
    element.classList.remove("bg-success");

    element.classList.add("bg-dark");
}

function OnChangeTimer()
{
    TimerRangeText.innerText = "Настройка таймера: " + TimerRange.value;
    fetch(document.location.protocol + "//" + document.location.host + "/SetTimer/" + TimerRange.value, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    });
}

var lastCarState;
function UpdateTraffic()
{
    fetch(document.location.protocol + "//" + document.location.host + "/GetState", {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => response.json()).then(obj => {
        console.log(obj);

        TimerInfo.innerText = "Таймер: " + obj.Timer + "\nВодители: " + obj.CarState + "\nПешеходы: " + obj.PeopleState;
        
        if(lastCarState != obj.CarState)
        {
            TimerRange.value = obj.MaxTimer;
            lastCarState = obj.CarState;
            TimerRangeText.innerText = "Настройка таймера: " + TimerRange.value;
        }

        ClearTraffic(CarRed);
        ClearTraffic(CarYellow);
        ClearTraffic(CarGreen);
        ClearTraffic(PeopleRed);
        ClearTraffic(PeopleGreen);

        if(obj.CarState == 'Green')
        {
            CarGreen.classList.remove("bg-dark");
            CarGreen.classList.add("bg-success");
        }
        else if(obj.CarState == 'BlinkGreen')
        {
            CarGreen.classList.remove("bg-dark");
            CarGreen.classList.add("bg-success");
            setTimeout(ClearTraffic, 500, CarGreen);
        }
        else if(obj.CarState == 'Yellow')
        {
            CarRed.classList.remove("bg-dark");
            CarRed.classList.add("bg-danger");
            CarYellow.classList.remove("bg-dark");
            CarYellow.classList.add("bg-warning");
        }
        else if(obj.CarState == "SecondYellow")
        {
            CarYellow.classList.remove("bg-dark");
            CarYellow.classList.add("bg-warning");
        }
        else if(obj.CarState == 'Red')
        {
            CarRed.classList.remove("bg-dark");
            CarRed.classList.add("bg-danger");
        }
        else if(obj.CarState == 'Disable')
        {
            CarYellow.classList.remove("bg-dark");
            CarYellow.classList.add("bg-warning");
            setTimeout(ClearTraffic, 500, CarYellow);
        }

        if(obj.PeopleState == 'Green')
        {
            PeopleGreen.classList.remove("bg-dark");
            PeopleGreen.classList.add("bg-success");
        }
        else if(obj.PeopleState == 'BlinkGreen')
        {
            setTimeout(ClearTraffic, 500, PeopleGreen);
            PeopleGreen.classList.remove("bg-dark");
            PeopleGreen.classList.add("bg-success");
        }
        else if(obj.PeopleState == 'Red')
        {
            PeopleRed.classList.remove("bg-dark");
            PeopleRed.classList.add("bg-danger");
        }
    });
}