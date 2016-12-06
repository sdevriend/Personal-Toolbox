
#option: --rm0.5
import sys


def alignPhotos(chunk):
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, preselection=PhotoScan.NoPreselection, 
                      filter_mask=True, keypoint_limit=0, tiepoint_limit=10000)
    chunk.alignCameras()

def buildDense(chunk):
    chunk.buildDenseCloud(quality=PhotoScan.HighQuality, filter=PhotoScan.MediumFiltering)

def buildmodel(chunk):
    chunk.buildModel()

def buildtexture(chunk):
    chunk.buildTexture()




def main(args):
    doc = PhotoScan.app.document
    docpath = doc.path
    basepath = docpath.split("/")
    samplename = basepath.pop(-1).rstrip(".psx")
    for chunk in doc.chunks:
        if chunk.label == str(samplename + "_raw"):
            raw_chunk = chunk
    alignPhotos(raw_chunk)
    raw_chunk.estimateImageQuality()
    if "--rm0.5" in args:
        for camera in raw_chunk.cameras:
    	    if camera.photo.meta['Image/Quality'] < 0.5:
                camera.enabled
        print("Doe Edwin spul")
        Corr_Chunk = raw_chunk.copy()
        alignPhotos(Corr_Chunk)
        buildDense(Corr_Chunk)
        buildmodel(Corr_Chunk)
        buildtexture(Corr_Chunk)
    buildDense(raw_chunk)
    buildmodel(raw_chunk)
    buildtexture(raw_chunk)
        



if __name__ == "__main__":
    main(sys.argv)