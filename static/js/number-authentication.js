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
        //swal("Recaptcha Success","", "success");
      },
      'expired-callback': function() {
        //swal("Recaptcha Failed","", "error");
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

function showVerifiedIcon(){
    $('#verifiedImg').attr('src', '../static/images/icons/greentick.png');
    $('#verifiedImg').attr('height', '15px');
    $('#verifiedImg').attr('width', '15px');
}

$("#sendBtn").on('click', function() {
//    generateRequest();
    disableSendCodeBtn();
    setTimeout(function(){
        var number = $('#number').val();
        var appVerifier = window.recaptchaVerifier;
        firebase.auth().signInWithPhoneNumber(number, appVerifier)
        .then(function (confirmationResult) {
            // SMS sent. Prompt user to type the code from the message, then sign the
            // user in with confirmationResult.confirm(code).
            window.confirmationResult = confirmationResult;
            swal("Sent!", "Code is sent to your mobile.", "success");
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
                    swal("Verified", "Your number is verified", "success");
                    disableVerifyCodeBtn();
                    showVerifiedIcon();
                    should_submit = true;
                    var phone = user.phoneNumber;
                    var uid = user.uid
                    generateRequest(uid, phone);
                }).catch(function (error) {
                    // User couldn't sign in (bad verification code?)
                    swal("Failed", "Phone number verification failed!", "error");
                    enableSendCodeBtn();
                });
            });
        }).catch(function (error) {
            console.log(error);
            enableSendCodeBtn();
            if(error['code'] == "auth/too-many-requests"){
                swal("Failed", "Too many attempts! please try again later.", "error");
            }else if(error['code'] == 'auth/invalid-phone-number'){
                swal("Failed", "Please provide a valid phone number!", "error");
            }else{
                swal("Failed", "Something went wrong! please try again later.", "error");
            }
        });
    }, 6000);
});
function generateRequest(id, phone){
    $.ajax({
            url: '/phone-verification',
            type: 'POST',
            data:{'customer_id' : id, "phone": phone},
            success: function(result) {
                window.location.replace("/");
            },
            error: function(){
                swal("Failed", "Couldn't add user", "error");
            }
    });
}