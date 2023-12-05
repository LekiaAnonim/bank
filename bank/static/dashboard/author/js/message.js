const message = document.querySelector('#message');

setTimeout(() => {
    message.style.display = "none";
}, 5000);

document.querySelectorAll('.messages').forEach((mess) => {
    setTimeout(() => {
        mess.style.display = "none";
    }, 5000);
});

let amountColumn = document.querySelectorAll('td:nth-child(3)');

amountColumn.forEach((ele) => {
    if (ele.innerText.startsWith("-")) {
        ele.style.color = 'red';
        console.log('red');
    } else {
        ele.style.color = 'green';
        console.log('green');
    }
})