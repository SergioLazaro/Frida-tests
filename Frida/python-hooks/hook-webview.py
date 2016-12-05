import frida
import sys

package_name = "com.example.t4k3d0wn.exampleapp"


def get_messages_from_js(message, data):
            print(message)
            print (message['payload'])
 

def instrument_load_url():

    hook_code = """
    Java.perform(function () {
        // Function to hook is defined here
        var WebViewActivity = Java.use('com.example.t4k3d0wn.exampleapp.WebViewActivity');

        // Whenever button is clicked
        WebViewActivity.refreshWebView.implementation = function (v) {
            
            // Show a message to know that the function got called
            send('Call - refreshWebView');

            this.updateURL("http://www.facebook.com");
        };

    });
    """

    return hook_code

process = frida.get_usb_device().attach(package_name)
script = process.create_script(instrument_load_url())
script.on('message',get_messages_from_js)
script.load()
sys.stdin.read()
              
