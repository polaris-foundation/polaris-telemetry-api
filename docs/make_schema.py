import codecs
import subprocess

import sadisplay

from dhos_telemetry_api.models import blood_glucose_meter, desktop, mobile

desc = sadisplay.describe(
    [blood_glucose_meter.BloodGlucoseMeter, desktop.Desktop, mobile.Mobile]
)
with codecs.open("docs/schema.plantuml", "w", encoding="utf-8") as f:
    f.write(sadisplay.plantuml(desc).rstrip() + "\n")

with codecs.open("docs/schema.dot", "w", encoding="utf-8") as f:
    f.write(sadisplay.dot(desc).rstrip() + "\n")

my_cmd = ["dot", "-Tpng", "docs/schema.dot"]
with open("docs/schema.png", "w") as outfile:
    subprocess.run(my_cmd, stdout=outfile)
