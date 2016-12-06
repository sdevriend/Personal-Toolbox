"""
Script is for Agisoft PhotoScan in python 3.
"""
import PhotoScan
doc = PhotoScan.app.document
for chunk in doc.chunks:
    for camera in chunk.cameras:
        print (camera)
