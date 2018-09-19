# QuickShortcutEditor v1.0 - Max van Leeuwen
#
# Change shortcuts in the accompanied 'change_shortcuts_here.txt'-file.


import nuke
import os

ShortcutEditorText = "[QuickShortcutEditor v1.0] "

def loadUserprefs(userprefsPath):
	scList = []
	if (os.path.isfile(userprefsPath)):
		with open(userprefsPath) as f:
			lines = f.readlines()

		i = 0
		for line in lines:
			if not ('#' in line[:2]):
				line = line.replace('\n', '')
				columns = line.split('\t')

				scEntry = []

				for column in [column for column in columns if (column != '' and column != ' ')]:
					scEntry.append(column)

				args = len(scEntry)
				if (args > 3):
					print (ShortcutEditorText + "Error: Could not read line " + str(i))
				elif (args == 3):
					scList.append(scEntry)
				elif (args == 2):
					scEntry.insert(0, '0')
					scList.append(scEntry)
				elif (args < 2):
					pass

			i += 1

	else:
		print (ShortcutEditorText + "Error: File does not exist")

	return scList


def assign(scContext, scKey, scPath):
	try:
		scMenutype = scPath.split('/')[0]
		scPathAftertype = scPath.replace(scMenutype, '')[1:]

		menu = nuke.menu(scMenutype)
		command = menu.findItem(scPathAftertype).script()

		if nuke.env['NukeVersionMajor'] < 9:
			menu.addCommand(scPathAftertype, command, scKey)
		else:
			menu.addCommand(scPathAftertype, command, scKey, shortcutContext=int(scContext))
	except:
		print (ShortcutEditorText + "Error: Could not assign shortcut to: " + scPath)


def assignfromFile(userprefsPath):
	scList = loadUserprefs(userprefsPath)

	i = 0
	for sc in scList:
		assign(scList[i][0], scList[i][1].replace(' ', ''), scList[i][2])
		i += 1