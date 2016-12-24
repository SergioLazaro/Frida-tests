#!/usr/bin/python
from sys import argv

import re
from androguard.core.analysis import analysis
from androguard.core.bytecodes import apk
from androguard.core.bytecodes import dvm
import optparse

class AndroApp:
	def __init__(self, apkpath):
		self.a = apk.APK(apkpath)
		self.d = dvm.DalvikVMFormat(self.a.get_dex())
		self.vmx = analysis.newVMAnalysis(self.d)

class AndroClass:
	def __init__(self,classname, methods):
		self.classname = classname
		self.methods = methods

	def print_info(self):
		print "CLASSNAME = " + self.classname
		print "METHODS"
		for method in self.methods:
			print method.toString()


class AndroMethod:

	def __init__(self,classname,methodname,signature):
		self.classname = classname
		self.methodname = methodname
		self.signature = signature

	def toString(self):
		return self.classname + " - " + self.methodname + " - " + self.signature

def convert_descriptor(name):
	name = name[1:]
	return name.replace("/",".").replace(";","")

def method_parser(method):
	class_name = re.search("(.*);->", method).group(1)
	method_tmp = re.search("<(.*)>", method)
	andro_method = None
	if method_tmp is None:
		method_name = re.search(";->(.*)\(", method).group(1)
		signature = re.search(method_name + "(.*) \[", method).group(1)
		andro_method = AndroMethod(class_name,method_name,signature)
		#print andro_method.toString()

	return andro_method


def main(apkpath):

	app = AndroApp(apkpath)

	package_name = app.a.get_package()
	print package_name
	activities = app.a.get_activities()

	andro_classes = list()

	for cl in app.d.get_classes():
		modified_class_name = convert_descriptor(cl.get_name())
		if package_name in modified_class_name and "R$" not in modified_class_name and \
				modified_class_name != package_name + ".BuildConfig" and \
				modified_class_name != package_name + ".R":

			andro_methods = list()
			for method in cl.get_methods():
				m = method_parser(str(method))
				if m is not None:
					andro_methods.append(m)
			andro_classes.append(AndroClass(modified_class_name, andro_methods))

	for ac in andro_classes:
		print ac.print_info()






	'''
	methods = app.d.get_methods()
	print "PACKAGE NAME: ", package_name 
	print "ACTIVITIES:"
	for activity in activities:
		if package_name in activity:		#Check for ensure app activities
			print "[*] ", activity

	print "Methods:"
	#for method in methods:
	#	print method.get_tags()
	'''

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