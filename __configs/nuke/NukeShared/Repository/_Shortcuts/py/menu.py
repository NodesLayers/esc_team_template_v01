# QuickShortcutEditor v1.0 - Max van Leeuwen

import QuickShortcutEditor
import os

thisScript = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QuickShortcutEditor.assignfromFile(thisScript.replace('\\', '/') + '/change_shortcuts_here.txt')