import nukescripts
import nuke
for w in nuke.allNodes("Write"):
    w.setSelected(True)
nukescripts.version_up()
nukescripts.script_version_up()
for w in nuke.allNodes("Write"):
    w.setSelected(False)