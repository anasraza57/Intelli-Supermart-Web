window.onload = function(){
render();
}

function render(){
window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container');
recaptchaVerifier.render();
}