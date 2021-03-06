#!/usr/bin/python  
# filename: mklib-win32.py  
# make import x86_32 import-lib from windows win32 dll  
# author: cheungmine@gmail.com  
# date: 2013-5  
# version: 0.1  
#  
# MinGW:  
#   $ python build-win32.py target_dll  
#   $ python build-win32.py libtiff-5.dll  
#   $ python build-win32.py libtiff-5  
#   $ python build-win32.py tiff-5  
#   $ python build-win32.py c:/path/to/libtiff-5  
# ERROR: $ python build-win32.py c:\path\to\libtiff-5  
#  
# file operation:  
# import shutil  
#  
## copy file:  
#   shutil.copy(myfile, tmpfile)  
#  
## copy time of file:  
#   shutil.copy2(myfile, tmpfile)  
#  
## copy file dir tree, the 3rd parameter means:  
##   True: symbol link  
##   False: use phyical copy  
#   shutil.copytree(root_of_tree, destination_dir, True)  
###############################################################################  
  
import os  
import platform  
import time  
import getopt  
import optparse  
import sys  
import string  
  
###############################################################################  
# get installed VS???COMNTOOLS environment:  
###############################################################################  
def get_vspath():  
  _vspath = os.getenv('VS110COMNTOOLS')  
  if not _vspath:  
	_vspath = os.getenv('VS100COMNTOOLS')  
	if not _vspath:  
	  _vspath = os.getenv('VS90COMNTOOLS')  
	  if not _vspath:  
		_vspath = os.getenv('VS80COMNTOOLS')  
		if not _vspath:  
		  print "VS??COMNTOOLS not found"  
		  sys.exit()  
		else:  
		  print "VS80COMNTOOLS =", _vspath  
	  else:  
		print "VS90COMNTOOLS =", _vspath  
	else:  
	  print "VS100COMNTOOLS =", _vspath  
  else:  
	print "VS110COMNTOOLS =", _vspath  
  return _vspath  
  
###############################################################################  
# step (1): create a windows module definition: target_lib.def  
#   MSCMD:  
#     > dumpbin /EXPORTS target_lib.dll > ~target_lib.def  
#   or MinGW:  
#     $ pexports target_lib.dll > target_lib.def  
# step (2): use this target_lib.def to create module import file: target_lib.lib  
#   MSCMD:  
#     > lib /def:target_lib.def /machine:i386 /out:target_lib.lib  
###############################################################################  
def make_lib(workdir, tgtname):  
  print "[2-1] create a windows module definition: lib%s.def" % tgtname  
  dump_def = 'cd "%s"&pexports lib%s.dll > lib%s.def' % \  
	(work_dir, tgtname, tgtname)  
  ret = os.system(dump_def)  
  if ret == 0:  
	print "[2-2] use (lib%s.def) to create import module: lib%s.lib" % (tgtname, tgtname)  
	lib_cmd = 'cd "%s"&lib /def:lib%s.def /machine:i386 /out:lib%s.lib' % (workdir, tgtname, tgtname)  
	cmds = 'cd "%s"&vsvars32.bat&%s&cd "%s"' % (vs_path, lib_cmd, cwd_path)  
	ret = os.system(cmds)  
	if ret == 0:  
	  print "INFO: mklib (%s/lib%s.lib) success." % (cwd_path, tgtname)  
	  return 0;  
	else:  
	  print "ERROR: mklib (%s/lib%s.lib) failed." % (cwd_path, tgtname)  
	  return (-2)  
  else:  
	print "ERROR: mklib (%s/lib%s.def) failed." % (cwd_path, tgtname)  
	return (-1);  
  
###############################################################################  
# current directory:  
cwd_path = os.getcwd()  
vs_path = get_vspath()  
  
work_dir = "./"  
  
# lib name == parent folder name  
target_dll = "ERROR_dll_not_found"  
  
if sys.argv.__len__() == 1:  
  work_dir, target_dll = os.path.split(cwd_path)  
elif sys.argv.__len__() == 2:  
  work_dir = os.path.dirname(sys.argv[1])  
  target_dll = os.path.basename(sys.argv[1])  
else:  
  print "ERROR: invalid argument"  
  sys.exit(-1)  
  
if target_dll[0:3] == "lib":  
  target_dll = target_dll[3:]  
tgtname, extname = os.path.splitext(target_dll)  
  
if extname != ".dll":  
  tgtname = target_dll  
  
if work_dir == "":  
  work_dir = cwd_path  
  
print "working directory:", work_dir  
print "======== make import (lib%s.lib) from (lib%s.dll) ========" % \  
  (tgtname, tgtname)  
  
make_lib(work_dir, tgtname)  
  
sys.exit(0)  


