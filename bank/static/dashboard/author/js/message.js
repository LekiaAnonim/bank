
const message = document.querySelector('#message');

setTimeout(() => {
    message.style.display = "none";
}, 5000);

document.querySelectorAll('.messages').forEach((mess) => {
    setTimeout(() => {
        mess.style.display = "none";
    }, 5000);
});


// const accountSuspendBtn = document.querySelectorAll('.account_suspend_btn');
// accountSuspendBtn.forEach((btn) => {
//     btn.addEventListener('click', () => {
//         const suspendDiv = document.createElement('div');
//         suspendDiv.classList.add('suspend');
//         suspendDiv.setAttribute('id', 'message');
//         suspendDiv.innerText = document.querySelector('.suspend_message').value;
        
//         document.querySelector('.customer-payment-container').append(suspendDiv);
//         setTimeout(() => {
//            suspendDiv.style.display = "none";
//         }, 5000);
//     }
//     )
// })



                            