#!/usr/bin/python
import os
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
	class_name = convert_descriptor(re.search("(.*);->", method).group(1))
	method_tmp = re.search("<(.*)>", method)
	andro_method = None
	if method_tmp is None:
		method_name = re.search(";->(.*)\(", method).group(1)
		signature = re.search(method_name + "(.*) \[", method).group(1)
		andro_method = AndroMethod(class_name,method_name,signature)
		#print andro_method.toString()

	return andro_method

def getAndroClasses(app, package_name):
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

	for an in andro_classes:
		an.print_info()
	return andro_classes

def writeFridaHeader(file, class_name):
	file.write("Java.perform(function() {\n")
	file.write("\t// Class to hook\n")
	file.write("\tvar ThisActivity = Java.use('" + class_name + "');\n")

def writeFridaHook(file,method):
	if method is not None:
		file.write("\tThisActivity." + method.methodname + ".implementation = function() {\n")
		file.write("\t\tsend('hook - " + method.methodname + "')\n")
		file.write("\t\tthis.")
		file.write("\t};\n")

def writeFridaPython(package_name, classname, python_path):
	py = open(python_path,"w")
	#Write header
	py.write('import frida, sys\n')
	py.write('package_name = "' + package_name + '"\n')
	#Write function get_messages_from_js
	py.write('def get_messages_from_js(message, data):\n')
	py.write('\tprint(message)\n')
	py.write("\tprint(message['payload'])\n")
	#Write function instrument_load_url
	py.write("def instrument_load_url():\n")
	py.write("\twith open('" + classname + "', 'r') as myfile:\n")
	py.write("\t\thook_code = myfile.read()\n")
	py.write("\treturn hook_code\n")
	#Write bottom
	py.write("process = frida.get_usb_device().attach(package_name)\n")
	py.write("script = process.create_script(instrument_load_url())\n")
	py.write("script.on('message',get_messages_from_js)\n")
	py.write("script.load()\n")
	py.write("sys.stdin.read()\n")

def writeFridaHooks(andro_classes, outputdir, package_name):
	createNewDir(outputdir + package_name) #Create directory for this apk

	for cl in andro_classes:
		filepath = outputdir + package_name + "/" + cl.classname
		hook_code = filepath + ".js"
		f = open(hook_code,"a")
		writeFridaHeader(f, str(cl.classname))
		for method in cl.methods:
			writeFridaHook(f, method)

		f.write("});")	#Close file structure
		f.close()
		writeFridaPython(package_name, cl.classname + ".js", filepath + ".py")


def createNewDir(dirpath):
	if not os.path.exists(dirpath):
		print "[*] Creating new directory in %s ..." % (dirpath)
		os.makedirs(dirpath)

def main(apkpath):
	outputdir = "hook_code/"
	createNewDir(outputdir)

	app = AndroApp(apkpath)
	package_name = app.a.get_package()
	#activities = app.a.get_activities()

	andro_classes = getAndroClasses(app,package_name)
	#andro_classes has AndroClasses info
	writeFridaHooks(andro_classes,outputdir, package_name)

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