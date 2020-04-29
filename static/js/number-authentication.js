var isAuthenticated = false;
var disabledBtn = false;
// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: "AIzaSyCnfJW9IXONV7ZcKKAgYdC3fedXUqNMH9E",
    authDomain: "intelli-super-mart.firebaseapp.com",
    databaseURL: "https://intelli-super-mart.firebaseio.com",
    projectId: "intelli-super-mart",
    storageBucket: "intelli-super-mart.appspot.com",
    messagingSenderId: "298617996174",
    appId: "1:298617996174:web:3d206b0d0dda2aee845adf",
    measurementId: "G-8FMZRBHGFX"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();

// To apply the default browser preference instead of explicitly setting it.
firebase.auth().useDeviceLanguage();

 window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('recaptcha-container', {
      'size': 'invisible',
      'callback': function(response) {
        //alert("recaptcha success");
      },
      'expired-callback': function() {
        //alert("recaptcha failed");
      }
  });

function disableSendCodeBtn(){
    $("#sendBtn").attr("disabled", true);
    $("#sendBtn").css('cursor', 'default');
    $("#sendBtn").css('background-color', 'grey');
}

function enableSendCodeBtn(){
    $("#sendBtn").removeAttr("disabled");
    $("#sendBtn").css('cursor', 'pointer');
    $("#sendBtn").css('background-color', '#5B3F91');
}

function disableVerifyCodeBtn(){
    $("#verificationCode").val("");
    $("#confirm_code_btn").attr("disabled", true);
    $("#confirm_code_btn").css('cursor', 'default');
    $("#confirm_code_btn").css('background-color', 'grey');
    disabledBtn = true;
}

function enableVerifyCodeBtn(){
    $("#confirm_code_btn").removeAttr("disabled");
    $("#confirm_code_btn").css('cursor', 'pointer');
    $("#confirm_code_btn").css('background-color', '#5B3F91');
    disabledBtn = false;
}

function makePassRequired(){
    $('#verifiedImg').attr('src', '../static/images/icons/greentick.png');
    $('#verifiedImg').attr('height', '15px');
    $('#verifiedImg').attr('width', '15px');
    $(".requiredField").attr("required", true);
}

$("#sendBtn").on('click', function() {
    disableSendCodeBtn();
    setTimeout(function(){
        var number = $('#number').val();
        var appVerifier = window.recaptchaVerifier;
        firebase.auth().signInWithPhoneNumber(number, appVerifier)
        .then(function (confirmationResult) {
            // SMS sent. Prompt user to type the code from the message, then sign the
            // user in with confirmationResult.confirm(code).
            window.confirmationResult = confirmationResult;
            if(disabledBtn){
                enableVerifyCodeBtn();
            }
            enableSendCodeBtn();

            $("#confirm_code_btn").on('click', function(){
                var code = $("#verificationCode").val();
                confirmationResult.confirm(code).then(function (result) {
                    // User signed in successfully.
                    var user = result.user;
                    // ...
                    alert("Phone number verified!")
                    disableVerifyCodeBtn();
                    makePassRequired();
                    should_submit = true;
                    isAuthenticated = true;
                    console.log(user);
                }).catch(function (error) {
                    // User couldn't sign in (bad verification code?)
                    // ...
                    alert("Phone number verification failed!");
                });
            });
        }).catch(function (error) {
            console.log(error);
            enableSendCodeBtn();
            if(error['code'] == "auth/too-many-requests"){
                alert("Too many attempts! please try again later.")
            }else if(error['code'] == 'auth/invalid-phone-number'){
                alert("Please provide a valid phone number!")
            }else{
                alert("Something went wrong! please try again later.")
            }
        });
    }, 6000);
});

function comparePassword(){
    var pass = $('#passField').val();
    var confrmPass = $('#confirmPassField').val();
    if(pass != confrmPass || pass.size== 0 || confrmPass==0){
        return false;
    }
    return true;
}

$('#registrationForm').on('submit', function(){
        if(!comparePassword()){
            alert("Password and Confirm Password doesn't match!");
            return false;
        }
//    if(!isAuthenticated){
//        alert("Please verify Your Phone Number First!");
//        return false;
//    } else {
//        if(!comparePassword()){
//            alert("Password and Confirm Password doesn't match!");
//            return false;
//        }
//    }
    $('#registerMsg').html("**Registered Successfully");
    return true;

});