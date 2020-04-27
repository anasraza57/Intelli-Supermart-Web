// window.onload = function () {
//     alert();
// }

$(window).load(function () {
    alert();
});

function render() {
    window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container');
    recaptchaVerifier.render();
}