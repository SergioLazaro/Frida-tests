import frida
import sys
import optparse

def get_messages_from_js(message, data):
    print(message)
    print (message['payload'])
 

def instrument_load_url(filepath):
    with open(filepath, 'r') as hook_file:
        hook_code = hook_file.read()
    
    return hook_code


def main(filepath, package_name):
    process = frida.get_usb_device().attach(package_name)
    script = process.create_script(instrument_load_url(filepath))
    script.on('message',get_messages_from_js)
    script.load()
    sys.stdin.read()

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", help="JavaScript file with hook code", dest="file",type="string")
    parser.add_option('-p', '--package', action="store", help="APK package name", dest="package",type="string")

    (opts, args) = parser.parse_args()
    if opts.file is not None and opts.package is not None:
        main(opts.file, opts.package)
    else:
        print_help(parser)

