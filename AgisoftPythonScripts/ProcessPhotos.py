
#option: --rm0.5
import sys
import time

def alignPhotos(chunk):
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.NoPreselection, 
                      filter_mask=True, keypoint_limit=0, tiepoint_limit=10000)
    chunk.alignCameras()

def buildDense(chunk):
    chunk.buildDenseCloud(quality=PhotoScan.HighQuality, filter=PhotoScan.MildFiltering)

def buildmodel(chunk):
    chunk.buildModel()

def buildtexture(chunk):
    chunk.buildUV()
    chunk.buildTexture()


def exportdata(chunk, path):
    filename = str("/".join(path) + "/" + chunk.label + "_Automatic")
    chunk.exportModel(str(filename + ".pdf"), binary=False, format="pdf", comment="Created with Python and Agisoft")
    chunk.exportModel(str(filename + ".ply"), binary=False, format="ply", texture_format="jpg")

def main(args):
    if "--sleep" in args:
        sleeptime = args[3] # PLEASE CHANGE THIS!
        print("TIME TO SLEEP FOR", sleeptime, "seconds !")        
        time.sleep(float(sleeptime))


    doc = PhotoScan.app.document
    docpath = doc.path
    basepath = docpath.split("/")
    samplename = basepath.pop(-1).rstrip(".psx")
    for chunk in doc.chunks:
        if chunk.label == str(samplename + "_raw"):
            raw_chunk = chunk
    alignPhotos(raw_chunk)
    doc.save()
    raw_chunk.estimateImageQuality()
    if "--rm0.5" in args:
        for camera in raw_chunk.cameras:
    	    if float(camera.photo.meta['Image/Quality']) < 0.5:
                camera.enabled = False
        print("Doe Edwin spul")
        Corr_Chunk = raw_chunk.copy()
        Corr_Chunk.label = str(samplename + "_0.5Cor")
        doc.save()
        alignPhotos(Corr_Chunk)
        doc.save()
        buildDense(Corr_Chunk)
        doc.save()
        buildmodel(Corr_Chunk)
        buildtexture(Corr_Chunk)
        doc.save()
        exportdata(Corr_Chunk, basepath)
    buildDense(raw_chunk)
    doc.save()
    buildmodel(raw_chunk)
    buildtexture(raw_chunk)
    doc.save()
    exportdata(raw_chunk, basepath)
    PhotoScan.app.quit()
        



if __name__ == "__main__":
    main(sys.argv)