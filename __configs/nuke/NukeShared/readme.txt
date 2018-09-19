NukeShared v1.9 - Max van Leeuwen - maxvanleeuwen.com/nukeshared



Installation:

1. 	Place the entire 'NukeShared'-folder somewhere you like. Could be on a server, if you want to have multiple computers load their plugins from it.


2.	On each computer you want to be linked with this repository, add the following line to your .nuke/init.py file (or create the file if it doesn't exist):

		nuke.pluginAddPath("path/to/NukeShared")

	The .nuke folder can be found here:

		Linux: /home/<user>/.nuke
		Mac OS X: /Users/<user>/.nuke
		Windows: \Users\<user>\.nuke


3.	That's it! Now you can start filling up the library in the NukeShared/Repository/ folder.
	Additional settings for NukeShared can be found in the NukeShared/Required/init.py-file,
	and more information can be found on my website: maxvanleeuwen.com/nukeshared.