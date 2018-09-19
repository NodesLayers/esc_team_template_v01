# NukeShared v1.9 - Max van Leeuwen - maxvanleeuwen.com/nukeshared
#
#
# Configuration:





open_dir_name 		= 	'Open NukeShared repository here'			# Text to show on button to open folder in file browser.
replace_underscore	=	True										# Auto-replace underscores ('_') with a space (' ') in the UI.
load_same_name_py	=	True										# Add the Python file to the UI when the .gizmo with the same name is right next to it in the same folder (will add '.py' to UI name).

autoinstaller 		= 	'autoinstaller.dat'							# Name of the empty file in the directories you want to load using their own menu.py/init.py (same as the '_AutoInstaller' folder).
openfolderbutton 	=	'openfolderbutton.dat' 						# Name of the empty file to put in a toolbar/menubar folder of which you want there to be a button with the name <open_dir_name>.
ignore 				= 	'ignore.dat' 								# Name of the empty file in the directories you want to completely ignore when scanning (subdirectories will still be scanned).

showconfirmation 	= 	True										# Show a confirmation print in the console when this instance of NukeShared has been loaded.
custommessage 		=	'Done!'
showstats 			=	True										# Print the amount of plugins and scripts loaded at the end of the confirmation.

write_active_user 	= 	False										# Enable user logging by making files with usernames, generated like this: 'NukeShared/Required/user_activity/JohnSmith.dat'.

cached 				= 	False										# Advanced: cache a generated menu.py and init.py file. This mainly exists for debugging purposes - it shows exactly what commands NukeShared sends to Nuke on startup.
cache_chance 		= 	1											# The chance (randomly 1 in every cache_chance) of having to cache the new list. Set to -1 to never update the existing cache.
cache_notification 	= 	True										# Show a message when your computer has to write the cache.
cache_message 		= 	'You are the chosen one. Writing cache.'	# What message the caching computer should see.





#
#
# Folders in the Repository explained:
#
# _AutoInstaller
#	All folders and subfolders in this folder will be loaded to Nuke, but not to the UI and only if they have a menu.py or init.py in them.
#	This folder is meant for plugins that have their own set of files - for instance, simply dragging the entire download folder for Cryptomatte or PixelFudger in there will install it.
#
# _Autorun
#	All Python files in this folder and its subfolders will be run on Nuke startup.
#	There are two subdirectories in this folder that cannot be changed or removed: _init and _menu. 
#	Place your scripts in the _init folder to have them run on Nuke startup (before UI), and in _menu to have them load with the UI.
#
# _Fonts
#	If there's more than one file in this folder or one of its subfolders, the Nuke script will have set its Font folder in the project settings to this path.
#	This way, the Text node can find all fonts in that folder (and all of its subfolders).
#
# _Shortcuts
#	Change the contents of the file 'change_shortcuts_here.txt' to quickly remap Nuke's keyboard shortcuts.
#	(See that file for more information.)
#
# _ViewerProcesses
#	The gizmo's in this folder and its subfolders will be registered as Nuke viewerprocesses in the viewer.
#
#
# All content of the other folders will be loaded and added to the UI in the right menu according to the folder name.
# E.g. 'Nodes' is the one you should place your gizmo's in, in order to have them on the left of the screen and in the TAB menu.
# 'Nuke' is the menu bar on the top of the screen, and 'Viewer' is the right-click menu in the viewer.
# For all names and their locations in Nuke, see this page by the Foundry: https://learn.foundry.com/nuke/developers/63/pythondevguide/custom_ui.html.
#
#





# # # # #


import os
import random
import inspect


try: #if the universal counting var exists, add 1 to its value - else start it at 0
	initID += 1
except NameError:
	initID = 0
initIDString = '{:03}'.format(initID + 1) #start counting amount of init.py files at 1 in logs so user won't be confused

NukeSharedStr	= "[NukeShared v1.9%s] "
NukeSharedPrint = NukeSharedStr % (' (' + initIDString + ')' if initIDString != "001" else '') #don't show initID in message when it is the first NukeShared


currroot = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/") #get the full path of the current location (<Z:/dir>)
root = os.path.dirname(currroot) + "/Repository/" #get the repository path (<Z:/Repository/>)
root_req = os.path.dirname(currroot) + "/Required/"

dir_fonts =			"_Fonts"
dir_autorun =		"_Autorun"
dir_shortcuts = 	"_Shortcuts"
dir_viewerprocess = "_ViewerProcesses"
dir_autoinstaller = "_AutoInstaller"
MenuTypes = ['Nuke', 'Pane', 'Nodes', 'Properties', 'Animation', 'Viewer', 'Node Graph', 'Axis'] #all possible menu types in Nuke

cachef = currroot + "/cache_init.py" #the path to the cache file (<Z:/dir/cache>)
cachenow = True if (random.random() <= (1.0 / cache_chance)) else False #determine if this computer should cache the plugin list right now (if cached == True)

fonts = []
autorun = []
viewerprocess = []
menutype = []
autorun_menu = []

pyFound = 0
fontFound = 0
viewerprocessFound = 0


def LoadCache(): #load the init file
	f = open(cachef,'r')
	ReadFile = f.read()
	exec ReadFile
	f.close()


def ManualInit(): #generate the init file
	global pyFound
	global fontFound
	global viewerprocessFound

	ToDo_Init = '' #placeholder for list of actions to evaluate, or read from cache

	for founddir in os.listdir(root): #get all base items
		if founddir == dir_autorun:
			for froot, fdir, ffiles in os.walk(root + founddir): #get all folders in autorun folder
				if not os.path.isfile(froot + ignore):
					froot = froot.replace('\\', '/') + '/'
					if (root + dir_autorun + "/_init/" in froot):
						autorun.append(froot) #add to list of autorun folders
					elif (root + dir_autorun + "/_menu/" in froot):
						autorun_menu.append(froot) #add to list of autoruns to run in menu.py
		elif (founddir == dir_fonts): #get fonts in fonts base
			for froot, fdir, ffiles in os.walk(root + founddir):
				froot = froot.replace('\\', '/') + '/'
				if not os.path.isfile(froot + ignore):
					ToDo_Init += "nuke.pluginAddPath(\"" + froot + "\")" + "\n" #add font folder to plugin list
					fontFound = len(ffiles)
		elif (founddir == dir_shortcuts):
			for froot, fdir, ffiles in os.walk(root + founddir):
				froot = froot.replace('\\', '/') + '/'	
				if not os.path.isfile(froot + ignore):
					ToDo_Init += "nuke.pluginAddPath(\"" + froot + "\")" + "\n" #add font folder to plugin list
		elif (founddir == dir_viewerprocess):
			for froot, fdir, ffiles in os.walk(root + founddir):
				froot = froot.replace('\\', '/') + '/'
				if not os.path.isfile(froot + ignore):
					ToDo_Init += "nuke.pluginAddPath(\"" + froot + "\")" + "\n" #add font folder to plugin list

					for eachItem in os.listdir(froot):
						ext = os.path.splitext(eachItem)[1]
						if(ext == '.gizmo' or ext == '.gznc'):
							ToDo_Init += "nuke.ViewerProcess.register('" + os.path.splitext(eachItem)[0] + "', nuke.Node, ('" + froot + eachItem + "', ''))" + '\n'
							viewerprocessFound += 1
		elif (founddir == dir_autoinstaller):
			for froot, fdir, ffiles in os.walk(root + founddir):
				froot = froot.replace('\\', '/') + '/'
				if ((os.path.isfile(froot + 'menu.py') or os.path.isfile(froot + 'init.py')) and not os.path.isfile(froot + ignore)): #only load plugin folder if a menu.py or init.py is present, don't do anything else with these folders
					ToDo_Init += "nuke.pluginAddPath(\"" + froot + "\")" + "\n" #add font folder to plugin list
		elif (founddir in MenuTypes):
			for froot, fdir, ffiles in os.walk(root + founddir):
				froot = froot.replace('\\', '/') + '/'
				if not os.path.isfile(froot + ignore):
					ToDo_Init += "nuke.pluginAddPath(\"" + froot + "\")" + "\n" #add font folder to plugin list

			menutype.append(root + founddir) #add to list of MenuType bases (all MenuTypes mashed togeter for now)


	for eachPath in menutype:
		for froot, fdir, ffiles in os.walk(eachPath): #get all sub dirs in plugins folder
			froot = froot if froot[len(froot)-1:] == '/' else froot + '/' #always end the path with /

			if not os.path.isfile(froot + ignore): #ignore if the 'ignore'-file is present in directory
				ToDo_Init += "nuke.pluginAddPath(\"" + froot.replace("\\", "/") + "\")" + "\n" #add every found subfolder as a loaded path so the plugins are already available in Nuke (just not in the GUI yet)

			
	for eachPath in autorun:
		eachPath = eachPath.replace("\\", "/")
		if not os.path.isfile(eachPath + ignore): #ignore if the 'ignore'-file is present in directory
			ToDo_Init += "nuke.pluginAddPath(\"" + eachPath + "\")" + "\n"
			for eachItem in [allFiles for allFiles in os.listdir(eachPath) if os.path.isfile(eachPath + allFiles)]: #only files
				if (eachItem == 'menu.py' or eachItem == 'init.py'):
					pyFound += 1
				else:
					ToDo_Init += "nuke.load('" + eachPath + eachItem + "')" + '\n'


	if(cached): #if caching is enabled, write cache and load from cache, else execute to-be-cached text
		f = open(cachef, 'w')
		f.write(ToDo_Init)
		f.close()

		LoadCache()
	else:
		exec ToDo_Init


if(cached):
	if cache_chance == -1: #never cache
		cachenow = False
	if(cachenow):
		if(cache_notification):
			print(NukeSharedPrint + cache_message)
		ManualInit()
	else:
		if os.path.isfile(cachef):
			LoadCache()
		else:
			if cache_chance == -1:
				print(NukeSharedPrint + "Cache is enabled, but no cache file exists and writing cache is disabled!")
			else:
				cachenow = True
				if(cache_notification):
					print(NukeSharedPrint + cache_message)
				ManualInit()
else:
	ManualInit()


CreateDicts = False #determines if universal dictionaries should be made or if they already exist
try:
	u_root
except:
	CreateDicts = True


if (CreateDicts): #make dicts for universal variable sharing (init.py files are all loaded before the first menu.py is loaded, which makes sharing data with menu.py files pretty difficult when multiple NukeShared instances are installed)
	u_currroot 						= 		{}
	u_root 							= 		{}
	u_root_req 						= 		{}
	u_dir_fonts						=		{}
	u_autorun_menu					=		{}
	u_menutype 						= 		{}

	u_open_dir_name 				= 		{}
	u_replace_underscore			=		{}
	u_load_same_name_py				=		{}
	u_ignore						=		{}
	u_autoinstaller					=		{}
	u_openfolderbutton				=		{}
	u_showconfirmation				=		{}
	u_custommessage					=		{}
	u_showstats						=		{}
	u_write_active_user				=		{}
	u_cached						=		{}
	u_cache_chance					=		{}
	u_cache_notification			=		{}
	u_cache_message					=		{}
	u_cachenow						=		{}

	u_pyFound						=		{}
	u_fontFound						=		{}
	u_viewerprocessFound			=		{}


#add data to universal dicts
u_currroot[initID]					=		currroot
u_root[initID] 						=		root
u_root_req[initID] 					=		root_req
u_dir_fonts[initID]					=		dir_fonts
u_autorun_menu[initID]				=		autorun_menu
u_menutype[initID] 					=		menutype

u_open_dir_name[initID] 			= 		open_dir_name
u_replace_underscore[initID]		=		replace_underscore
u_load_same_name_py[initID]			=		load_same_name_py
u_ignore[initID]					=		ignore
u_autoinstaller[initID]				=		autoinstaller
u_openfolderbutton[initID]			=		openfolderbutton
u_showconfirmation[initID]			=		showconfirmation
u_custommessage[initID]				=		custommessage + ' '
u_showstats[initID]					=		showstats
u_write_active_user[initID]			=		write_active_user
u_cached[initID]					=		cached
u_cache_chance[initID]				=		cache_chance
u_cache_notification[initID]		=		cache_notification
u_cache_message[initID]				=		cache_message
u_cachenow[initID]					=		cachenow

u_pyFound[initID]					=		pyFound
u_fontFound[initID]					=		fontFound
u_viewerprocessFound[initID]		=		viewerprocessFound