#!/usr/bin/python
from sys import argv
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm

def main(apkpath):
	a = apk.APK(apkpath)
	d = dvm.DalvikVMFormat(a.get_dex())
	for current_class in d.get_classes():
		for method in current_class.get_methods():
			print "[*] ",method.get_name(), method.get_descriptor()
			byte_code = method.get_code()
			if byte_code != None:
				byte_code = byte_code.get_bc()
				idx = 0
				for i in byte_code.get_instructions():
					print "\t, %x " % (idx),i.get_name(),i.get_output()
					idx += i.get_length()

def print_help(parser):
    print "arguments error!!\n"
    parser.print_help()
    exit(-1)

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-f', '--file', action="store", help="APK file path", dest="apk",type="string")

    (opts, args) = parser.parse_args()
    if opts.apk is not None:
        main(opts.apk)
    else:
        print_help(parser)