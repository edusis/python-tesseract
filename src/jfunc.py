from __future__ import print_function
import platform, os, subprocess,glob
import subprocess, glob, struct

WIN64=True
DEBUG=True
WARNING_LEVEL=10
USE_MINGW=True
colors={'LIST':'\033[95m',
		'BLACK':'\033[0m',
		'FLOAT' : '\033[95m',
		'INT' : '\033[94m',
		'STR' : '\033[92m',
		'WARNING' : '\033[93m',
		'DICT' : '\033[95m',
		'OKBLUE' : '\033[94m',
		'OKGREEN' : '\033[92m',
		'WARNING' : '\033[93m',
		'FAIL' :'\033[91m',
		'ENDC' : '\033[0m',
		}
colorkeys=list(colors.keys())
import logging
#FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s"
logging.basicConfig(level=logging.INFO,format=FORMAT)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
pp=logger.info

class jfunc():
	def __init__(self):
		self.mingwPaths=self.getMingwPaths()
		self.python_version=self.getPythonVersion()
		self.python_archit=self.getPythonArchit()
		self.osname=self.getOsName()
		self.pythonBinPaths=self.getPythonPathForWindows()

		#print(self.osname)
		self.defineSitePackagesLocations()

	def getPythonArchit(self):
		return 8*struct.calcsize("P")

	def getPythonPathForWindows(self):
		pythonBinPaths={}
		pythonPaths=glob.glob("c:\python*")
		if not pythonPaths:
			return None
		for pythonPath in pythonPaths:
			cmdList=[pythonPath+'\python','-c','import struct;print(8*struct.calcsize("P"))']
			archit=int(self.cmdRaw(cmdList))
			pythonBinPaths[archit]=pythonPath
		return pythonBinPaths

	def getMingwPaths(self):
		mingwPaths={}
		mingwPaths[32]=[]
		mingwPaths[64]=[]
		mdirs=sorted(glob.glob(r'c:\Program Files*\mingw-w64\*\mingw*\bin'))
		for mdir in mdirs:
			if "mingw32" in mdir:
				mingwPaths[32].append(mdir)
			elif "mingw64" in mdir:
				mingwPaths[64].append(mdir)
		return mingwPaths

	def getPythonVersion(self):
		python_version=self.cmd('python --version')
		return "python"+".".join(python_version.split(".")[:-1])

	def listDoer(self,doer,anyFile):
		mfiles=glob.glob(anyFile)
		print(mfiles)
		for mfile in mfiles:
			doer(mfile)
	def remove(self,mfile):
		self.listDoer(self.removeOneFile,mfile)

	def removeOneFile(self, mfile):
		try:
			os.remove(mfile)
		except:
			print("Cannot Remove: %s"%mfile)
			if not os.path.exists(mfile):
				print("File not existed")

	def type(self,a):
		return repr(type(a)).split(" ")[-1][1:-2].upper()

	def puts(self,*argv,**kwargs):
		END=kwargs.get("END","\t")
		START=kwargs.get("START","")
		mlen=len(argv)
		if mlen> 1 and isinstance( argv[-1], int ):
			warning=argv[-1]
			argv=argv[:-1]
		else:
			warning=0

		if not DEBUG or (warning < WARNING_LEVEL):
			return

		for arg in argv:
			argType=self.type(arg)
			if argType in colorkeys:
				START_=colors[argType]+"[%s]"%argType+START
				END_=END+colors['ENDC']
			builtins.print(START_,repr(arg).strip(),end=END_)
		builtins.print()

	def defineSitePackagesLocations(self):
		osname=self.osname
		if osname=="darwin":
			#brew_prefix=subprocess.getstatusoutput('brew --prefix')[1]
			brew_prefix=self.cmd('brew --prefix')
			self.sitepackagesLocations=[
				os.path.expanduser("~/Library/Python/2.7/lib/python/site-packages"),
				"/usr/local/lib/python2.7/site-packages/",
				"/Library/Python/2.7/site-packages"
				]
		elif osname=="linux":
			pyVers=["2.7","3","3.4"]
			pyDirFmt=[os.path.expanduser("~/.local/lib/python%%/site-packages"),
				"/usr/local/lib/python%%/dist-packages",
				"/usr/lib/python%%/dist-packages",
				"/usr/lib/python%%/site-packages"]
			self.sitepackagesLocations=[]
			for pyVer in pyVers:
				self.sitepackagesLocations+= [ mdir.replace("%%",pyVer) for mdir in pyDirFmt ]
			#print(self.sitepackagesLocations)


		elif osname=="windows" or osname=="mingw":
			self.sitepackagesLocations=[
				os.path.expanduser("~\\appdata\\roaming\\python\\python27\\site-packages")]
			for archit in self.pythonBinPaths.keys():
				mpath=os.path.join(self.pythonBinPaths[archit] ,"Lib","site-packages")
				print("mpath:",mpath)
				self.sitepackagesLocations.append(mpath)

		else:
			self.sitepackagaesLocations=[]



	def getOsName(self):
		osname=platform.uname()[0].lower().strip()
		if osname=="windows":
			if self.isMinGW():
				osname="mingw"
		return osname


	def isMinGW(self):
		cmdStr=self.mingwPaths[self.python_archit][-1]+"/gcc --version"
		print(cmdStr)
		results=subprocess.Popen(cmdStr, stdout=subprocess.PIPE).stdout.read()
		if USE_MINGW and "MinGW" in results:
			return True

	def runCmd4Files(self,pwd,cmd,mfiles):
		for mfile in mfiles:
			#print mfile
			mfile=os.path.join(pwd,mfile)
			mfiles=glob.glob(mfile)
			for mfile in mfiles:
				if  os.path.exists(mfile):
					rmStr='%s %s'%(cmd,mfile)
					print(rmStr)
					os.system(rmStr)
				else:
					print("%s cannot be removed"%mfile)

	def runRm4Dirs(self,pwd,mfiles):
		if self.osname == "windows" or self.osname=="mingw":
			rmDirCmd="rd /S /Q"
		else:
			rmDirCmd="rm -rf"


		self.runCmd4Files(pwd,rmDirCmd,mfiles)

	def runRm4Files(self,pwd,mfiles):
		self.puts([self.osname,len(self.osname)])
		self.puts("------------------")


		if self.osname == "windows" or self.osname=="mingw":
			self.puts([self.osname,len(self.osname)])
			self.puts("........")
			rmFileCmd="del /S /Q"
		else:
			self.puts("????")
			rmFileCmd="rm -rf"
			self.puts("removed")

		self.puts("****************")
		self.runCmd4Files(pwd,rmFileCmd,mfiles)
		self.puts("*****-----***********")

	def rmFiles(self,mFiles,PROTECTED_FILES=[]):
		mFiles2=[]
		for mFile in mFiles:
			mFiles2+=glob.glob(mFile)
		mFiles2=sorted(list(set(mFiles2).difference(PROTECTED_FILES)))
		for mFile in mFiles2:
			#print(mFile)
			os.remove(mFile)

	def getTesseractVersion(self):
		result=self.cmd("tesseract -v")
		if not result:
			print("Tesseract Not Installed!")
			return None
		for item in result.split("\n"):
			subItems=item.split()
			if len(subItems)!=2:
				continue
			name, version=subItems
			if name.strip().lower()=="tesseract":
				return version.strip()

		return None
	def cmd(self, cmdStr):
		return self.cmdRaw(cmdStr.split())

	def cmdRaw(self,cmdList):
		try:
			result=subprocess.check_output(cmdList,stderr=subprocess.STDOUT)
		except:
			return
		if result:
			return result.decode('utf-8').strip()

j=jfunc()
osname=j.osname
mingwPaths=j.mingwPaths
sitepackagesLocations=j.sitepackagesLocations
print("Your os is:%s"%osname)

def puts(*argv,**kwargs):
	j.puts(*argv,**kwargs)



if __name__ == "__main__":
	#puts("os is %s"%osname,11)
	#puts("Warining Level is %s"%8,8)
	#puts("Warining Level is %s"%11,11)
	#puts(1.21,3,"apple",[1,2,3],192)
	#puts(1.21,3,"apple",[1,2,3],192,END=" ")
	#puts(1.21,3,"apple",[1,2,3],192,START="*"*10,END="%s,\n"%("^"*10))
	#print(j.osname)
	#j.getPythonPathForWindows()
	#print(j.python_version)
	#print(j.pythonBinPaths)
	rmFiles="main.h config.h tesseract.py *wrap.cpp setuptools* *tar.gz* *.pyc *.h".split(" ")
	j.rmFiles(rmFiles,PROTECTED_FILES=["fmemopen.h"])
