# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Heading Calculator
                                 A Standalone Desktop Application
 This tool performs calculation of heading angle for a list of photos taken
 by fix-wing drones.
                              -------------------
        begin                : 2020-09-01
        git sha              : 
        copyright            : (C) 2020 by Chubu University
        email                : ts18851@chubu.ac.jp
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from pyexiftool import ExifTool

# index of parameters in return value of ProcessMetadata class functions format_tag_path, format_tag_index
NTAGS = 12 # number of tags
IMAGE_WIDTH = 0
IMAGE_HEIGHT = 1
FOCAL_LENGTH = 2
LATITUDE = 3
LONGITUDE = 4
GPS_ALT = 5
BARO_ALT = 6
GROUND_ALT = 7
HEADING = 8
ROLL = 9
PITCH = 10
MODEL = 11


class ProcessMetadata:
    def __init__(self, photos, tags=None):
        
        # if no tags is specified, use the following tags
        if not tags:
            tags = ["exif:gpslatitude", "exif:gpslongitude", "exif:gpslatituderef", \
                "exif:gpslongituderef", "exif:gpsaltitude", "exif:model", \
                "exif:focallength", "file:imagewidth", "file:imageheight", \
                "xmp:relativealtitude", "xmp:groundaltitude", \
                "xmp:gimbalyawdegree", "xmp:gimbalrolldegree", "xmp:gimbalpitchdegree"]
                
        # get tags
        metadata = None
        with ExifTool() as et:
            metadata = et.get_tags_batch(tags, photos)
            metadata =  [{k.lower(): v for k, v in d.items()} for d in metadata]
        
        self.metadata = metadata
    
    # get tag value for a single photo, search based on photo path
    def filter_tag_imgpath(self, path, tag):
        
        try:
            for d in self.metadata:
                if d['sourcefile'] == path:
                    return d[tag]
            return None
        except:
            return None
        
    # get tag value for a single photo, search based on index
    def filter_tag_index(self, idx, tag):
        
        try:
            return self.metadata[idx][tag]
        except:
            return None
        
    # check for barometer altitude existence
    def has_baro_altitude(self, ):
        
        try:
            baroalt = self.filter_tag_index(0, 'xmp:relativealtitude')
            if baroalt:
                return True
            else:
                return False
        except:
            return False
    
    # format return array
    def format_return(self, iw, ih, fl, lat, lon, gpsalt, baroalt, groundalt, heading, roll, pitch, model):
        
        result = [0] * NTAGS
        
        result[IMAGE_WIDTH] = iw
        result[IMAGE_HEIGHT] = ih
        result[FOCAL_LENGTH] = fl
        result[LATITUDE] = lat
        result[LONGITUDE] = lon
        result[GPS_ALT] = gpsalt
        result[BARO_ALT] = baroalt
        result[GROUND_ALT] = groundalt
        result[HEADING] = heading
        result[ROLL] = roll
        result[PITCH] = pitch
        result[MODEL] = model
        
        return result
        
    # prepare input data for single uav photo georeference
    def format_tag_path(self, path):
        
        try:
            # image width
            iw = self.filter_tag_imgpath(path, 'file:imagewidth')
            if iw:
                iw = int(iw)
            # image height   
            ih = self.filter_tag_imgpath(path, 'file:imageheight')
            if ih:
                ih = int(ih)
            # focal length 
            fl = self.filter_tag_imgpath(path, 'exif:focallength')
            if fl:
                fl = float(fl / 1000)
            # GPS latitude     
            lat = self.filter_tag_imgpath(path, 'exif:gpslatitude')
            if lat:
                lat = float(lat)
            # GPS longitude        
            lon = self.filter_tag_imgpath(path, 'exif:gpslongitude')
            if lon:
                lon = float(lon)
            # GPS altitude          
            gpsalt = self.filter_tag_imgpath(path, 'exif:gpsaltitude')
            if gpsalt:
                gpsalt = float(gpsalt)
            # barometer altitude        
            baroalt = self.filter_tag_imgpath(path, 'xmp:relativealtitude')
            if baroalt:
                baroalt = float(baroalt)
            # ground altitude        
            groundalt = self.filter_tag_imgpath(path, 'xmp:groundaltitude')
            if groundalt:
                groundalt = float(groundalt)
            # heading angle      
            heading = self.filter_tag_imgpath(path, 'xmp:gimbalyawdegree')
            if heading:
                heading = float(heading)
            # roll angle          
            roll = self.filter_tag_imgpath(path, 'xmp:gimbalrolldegree')
            if roll:
                roll = float(roll)
            # pitch angle     
            pitch = self.filter_tag_imgpath(path, 'xmp:gimbalpitchdegree')
            if pitch:
                pitch = float(pitch)
            # camera model name
            model = self.filter_tag_imgpath(path, 'exif:model')
            
            return self.format_return(iw, ih, fl, lat, lon, gpsalt, baroalt, groundalt, heading, roll, pitch, model)
        
        except:
            return None
        
    # prepare input data for single uav photo georeference
    def format_tag_index(self, idx):
        
        try:
            # image width           
            iw = self.filter_tag_index(idx, 'file:imagewidth')
            if iw:
                iw = int(iw)
            # image height       
            ih = self.filter_tag_index(idx, 'file:imageheight')
            if ih:
                ih = int(ih)
            # focal length     
            fl = self.filter_tag_index(idx, 'exif:focallength')
            if fl:
                fl = float(fl / 1000)
            # GPS latitude         
            lat = self.filter_tag_index(idx, 'exif:gpslatitude')
            if lat:
                lat = float(lat)
            # GPS longitude         
            lon = self.filter_tag_index(idx, 'exif:gpslongitude')
            if lon:
                lon = float(lon)
            # GPS altitude           
            gpsalt = self.filter_tag_index(idx, 'exif:gpsaltitude')
            if gpsalt:
                gpsalt = float(gpsalt)
            # barometer altitude          
            baroalt = self.filter_tag_index(idx, 'xmp:relativealtitude')
            if baroalt:
                baroalt = float(baroalt)
            # ground altitude         
            groundalt = self.filter_tag_index(idx, 'xmp:groundaltitude')
            if groundalt:
                groundalt = float(groundalt)
            # heading angle        
            heading = self.filter_tag_index(idx, 'xmp:gimbalyawdegree')
            if heading:
                heading = float(heading)
            # roll angle          
            roll = self.filter_tag_index(idx, 'xmp:gimbalrolldegree')
            if roll:
                roll = float(roll)
            # pitch angle      
            pitch = self.filter_tag_index(idx, 'xmp:gimbalpitchdegree')
            if pitch:
                pitch = float(pitch)
            # camera model name
            model = self.filter_tag_index(idx, 'exif:model')
            
            return self.format_return(iw, ih, fl, lat, lon, gpsalt, baroalt, groundalt, heading, roll, pitch, model)
        
        except:
            return None