console.log('Working!!!!!!!!!!!!!');
const otpInput = document.querySelector('#id_otp');
console.log(otpInput);
const otpButton = document.querySelector('.otp-button');
const paymentTable = document.querySelector('.payment-table')
const paymentButton = document.querySelector('.send-payment');
const paymentForm = document.querySelector('#payment-form');
const receiverEmail = document.querySelector('.user-email');

const len = 6;

function generate_otp() {
    let number = Math.floor(Math.pow(10, len-1) + Math.random() * (Math.pow(10, len) - Math.pow(10, len-1) - 1));
    return number;
}
let otp = generate_otp();

console.log(otp);

paymentForm.addEventListener('submit', function (e) {
    // if (!isValid) {
        // e.preventDefault();
    // }
    
    const otpInfo = document.createElement('p');
    
    console.log(otp);
    if (otpInput.value != otp) {
        e.preventDefault();
        // alert('The OTP does not match. Please click on the  Get OTP button, and check your mail to get your OTP');
        const otp_error = new Error('The OTP does not match. Please click on the  Get OTP button, and check your mail to get your OTP');
        
        otpInfo.style.color = 'red';
        otpInfo.innerText = otp_error;
        paymentForm.appendChild(otpInfo);
    }
    
})



otpButton.addEventListener('click', function (e) {
    e.preventDefault();
    console.log(otp);
    const name = 'Lekia';
    const email ='lekiaprosper@gmail.com';
    const subject = 'CADENCE BANK: Verify OTP';
    let message = `Hello, ${name}, you are trying to make a payment, copy the OTP to continue your transaction.
                    OTP: ${otp}`;
    sendMail(email, subject, message);
    const otpInfo = document.createElement('p');
    otpInfo.style.color = 'green';
    otpInfo.innerText = `An OTP has been sent to your email`;
    paymentTable.appendChild(otpInfo);
    console.log('sending email...');
})

function sendMail(email, subject, message) {
    Email.send({
        Host : "smtp.elasticemail.com",
        Username : "lekiaprosper@gmail.com",
        Password : "10C1580AFA1B9889D2F54FB685B658865485",
        To : receiverEmail.innerText,
        From : email,
        Subject : subject,
        Body : message
    }).then(
    message => alert(message)
    );
}
