
const length = 12;
const display = document.querySelector('.display-generate-no')
function generate() {
    let number = Math.floor(Math.pow(10, length-1) + Math.random() * (Math.pow(10, length) - Math.pow(10, length-1) - 1));
    display.innerText = number;
    return display;
} 

const GenerateBtn = document.querySelector('.generate-account-no');
GenerateBtn.addEventListener('click', generate, true);