import PhotoScan
import os

doc = PhotoScan.app.document
docpath = doc.path.split("/")
samplename = docpath.pop(-1).rstrip(".psx")

doc.addChunk()
doc.chunk.label = str(samplename + "_raw")

filelist = []
for root, subdirs, files in os.walk(str("/".join(docpath) + "/" + samplename)):
    for filename in files:
        if filename[-4:] == ".tif":
            filelist.append(os.path.join(root, filename).replace("\\", "/"))



doc.chunk.addPhotos(filelist)
for photo in doc.chunk.cameras:
    photo.photo.thumbnail(width=192, height=192)

doc.chunk.importMasks(method='alpha', operation='replacement')
            
            
    

