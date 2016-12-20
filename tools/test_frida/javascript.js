Java.perform(function () {
    // Function to hook is defined here 
    var MainActivity = Java.use('com.example.t4k3d0wn.exampleapp.MainActivity');
    // Whenever button is clicked
    MainActivity.getIMEI.implementation = function (v) {
        // Show a message to know that the function got called
        send('Call - getIMEI');
        //Modify IMEI display
        this.updateTV("p0wn3d");
        // Set our values after running the original onClick handler
        this.imei.value = "p0wn3d";
    };
    // Whenever button is clicked
    MainActivity.checkPIN.implementation = function (v) {
        // Show a message to know that the function got called
        send('Call - CheckPIN');
        this.hidePinVerification();
    };
});
