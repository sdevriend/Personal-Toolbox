"""
Script is for Agisoft PhotoScan in python 3.

The script assumes that the samples are located in a folder near the Agisoft save.
For example:
C:\Models\Sample1\Sample1.psx <- agisoft photosave file.
and moved the pictures to
C:\Models\Sample1\Sample1
I am working with rounds. So the script automaticly sets the rounds correct.
This means that a picture can be found in:
C:\Models\Sample1\Sample1\Round_1\Round_1_DSC4495.tif
"""
import PhotoScan
doc = PhotoScan.app.document
docpath = doc.path
basepath = docpath.split("/")
samplename = basepath.pop(-1).rstrip(".psx")

for chunk in doc.chunks:
    for camera in chunk.cameras:
        oldpath = camera.photo.path.split("/")
        filename = oldpath.pop(-1)
        round = oldpath.pop(-1)
        newpath = str("/".join(basepath) + "/" + samplename + "/" + round + "/" + filename)
        camera.photo.path = newpath
