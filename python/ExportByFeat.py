# -*- coding: utf-8 -*-
"""
@author: Rodrigo E. Principe

email: fitoprincipe82 at gmail
twitter: @fitoprincipe
github: https://github.com/gee-community/gee_tools
linkedin: https://www.linkedin.com/in/rodrigo-esteban-principe-93066754/
"""
import ee
ee.Initialize()

def ExportByFeat(img, fc, prop, folder, scale=1000):
    """
    Export an image clipped by features (Polygons)
    
    Parameters:
    | **img** = image to clip (ee.Image)
    | **fc** = feature collection (ee.FeatureCollection)
    | **prop** = name of the property of the features to paste in the image (str)
    | **folder** = same as ee.Export (str)
    | **scale** = same as ee.Export (int) default to 1000
    """

    featlist = fc.getInfo()["features"]
    name = img.getInfo()["id"].split("/")[-1]
    
    def unpack(thelist):
        unpacked = []
        for i in thelist:
            unpacked.append(i[0])
            unpacked.append(i[1])
        return unpacked
    
    for f in featlist:
        geomlist = unpack(f["geometry"]["coordinates"][0])
        geom = ee.Geometry.Polygon(geomlist)
        
        feat = ee.Feature(geom)
        dis = f["properties"][prop]
        
        if type(dis) is float:
            disS = str(int(dis))
        elif type(dis) is int:
            disS = str(dis)
        elif type(dis) is str:
            disS = dis
        else:
            print "unknown property's type"
            break
        
        task= ee.batch.Export.image.toDrive(
        image=img,
        description= name+"_"+disS,
        folder= folder,
        fileNamePrefix= name+"_"+disS,
        region= feat.geometry().bounds().getInfo()["coordinates"],
        scale= scale)
        
        task.start()
        print "exporting {0} {1}..".format(name, disS)