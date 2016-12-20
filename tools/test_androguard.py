#!/usr/bin/python
from sys import argv
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import optparse

def main(apkpath):
	a = apk.APK(apkpath)
	d = dvm.DalvikVMFormat(a.get_dex())
	package_name = a.get_package()
	activities = a.get_activities()
	for activity in activities:
		if package_name in activity:
			print "[*] ", activity

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