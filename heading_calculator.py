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

import csv
from math import atan2, sqrt
from os import listdir
from os.path import basename, join, isfile, exists
from datetime import datetime
import exifread

from process_metadata import *
from pyexiftool import ExifTool


def getPhotos(folder, exts=('.jpg')):
    """
    Get a list of photos within the folder.

    Parameters
    ----------
    folder : string
        Full path to the folder containing photos.
    exts : tuple, optional
        Supported photo extensions. The default is ('.jpg').

    Returns
    -------
    imgs : list
        A list of photos matched with the search criteria.

    """

    # convert folder variable to string
    folder = str(folder)

    # get photos
    imgs = []
    if exists(folder):
        imgs = [join(folder, f) for f in listdir(folder) if (isfile(join(folder, f)) and f.lower().endswith(exts))]

    # [] if no photos found
    return imgs

def getDateExif(filepath):
    """
    Extract datetime of the photo and format it.

    Parameters
    ----------
    filepath : string
        Full path to the photo.

    Returns
    -------
    date : string
        Formatted date of the photo. The format is '%Y:%m:%d %H:%M:%S'

    """

    with open(filepath, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
        str_date = str(tags["EXIF DateTimeOriginal"])
        date = datetime.strptime(str_date , '%Y:%m:%d %H:%M:%S')

    return date

def headingCalSingle(x1, y1, x2, y2):
    """
    Calculate heading angle in reference to the north of current photo.

    Parameters
    ----------
    x1 : float
        GPS Longitude of the photo taken right before current photo.
    y1 : float
        GPS Latitude of the photo taken right before current photo.
    x2 : float
        GPS Longitude of the photo taken right after current photo.
    y2 : float
        GPS Latitude of the photo taken right after current photo.

    Returns
    -------
    heading : float
        Heading angle in reference to the north of current photo.

    """

    # compute heading vector
    hx = x2 - x1
    hy = y2 - y1

    # compute heading angle to north
    northx, northy = 0, 1
    dot = hx*northx + hy*northy
    det = hx*northy - hy*northx
    heading = atan2(det, dot) * (180 / 3.1415926535897)

    return heading

def formatResult(result):
    """
    Format the processing result of function headingCalculator to be displayed as log in the main UI.

    Parameters
    ----------
    result : 2D list
        Contains photo name, heading, Latitude, Longitude for each photo.

    Returns
    -------
    log : string
        Formatted string as log.

    """

    log = list()
    len_s = len(result)

    log.append("Calculated heading for: {0} photos:".format(len_s))
    log.append("----------")
    for i in range(0, len_s):
        r_ = "{0}: {1}".format(basename(result[i][0]), result[i][1])
        log.append(r_)

    log = "\n".join(str(x) for x in log)
    log = log + "\n"
    return log

def distanceCal(x1, y1, x2, y2):
    """
    Calculate distance between two points in 2D system

    Parameters
    ----------
    x1 : float
        X coordinate of 1st point.
    y1 : float
        Y coordinate of 1st point.
    x2 : float
        X coordinate of 2nd point.
    y2 : float
        Y coordinate of 2nd point.

    Returns
    -------
    float
        Distance between the two points.

    """

    return sqrt((x1-x2)**2 + (y1-y2)**2)

def headingCalculator(folder, imgexts, progress_callback):
    """
    Calculate heading angle for suitable photos within the folder.

    Parameters
    ----------
    folder : string
        Full path to the folder containing photos.
    imgexts : tuple
        Supported photo extensions.
    progress_callback : object
        Object to update progress to the main UI.

    Raises
    ------
    Exception
        1. Less than 3 photos found in the folder -> cannot calculate heading angle.
        2. Failed calling batch update exiftool -> exiftool is not working.

    Returns
    -------
    dict
        Contains two elements:
            - heading: a list of heading angles.
            - avgdist: average distance between photos
            - msg: log to be displayed in the main UI.

    """

    # get photos
    photos = getPhotos(folder, imgexts)
    n_photos = len(photos)

    # if photos is empty or less than 3, then halt processing
    if n_photos < 3:
        raise Exception('At least 3 photos are required to calculate heading!')

    # this variable is used to keep track of progress
    N = n_photos - 2

    # sort photos by taken time
    photo_dates = [getDateExif(i) for i in photos]
    photo_timestamps = [int(x.timestamp()) for x in photo_dates]

    flights = list()
    flights.append(photos)
    flights.append(photo_timestamps)
    flights = [list(i) for i in zip(*flights)]
    flights.sort(key=lambda x : x[1] , reverse = False)

    # initialize process metadata object
    #proobj = ProcessMetadata(flights[:,0])
    flist = [i[0] for i in flights]
    proobj = ProcessMetadata(flist)

    # calculate heading and write it back to the image
    result = list()
    update_txt = list()
    distl = list()
    for i in range(1, n_photos-1):

        # if photo has heading already, skip to next
        this_spec = proobj.format_tag_index(i)

        img1_spec = proobj.format_tag_index(i-1)
        img2_spec = proobj.format_tag_index(i+1)

        x1, y1 = img1_spec[LONGITUDE], img1_spec[LATITUDE]
        x2, y2 = img2_spec[LONGITUDE], img2_spec[LATITUDE]

        heading = headingCalSingle(x1, y1, x2, y2)
        distl.append(distanceCal(this_spec[LONGITUDE], this_spec[LATITUDE], x1, y1))

        # update txt
        #update_txt.append("{0},{1}".format(flights[i][0], heading))
        update_txt.append([flights[i][0], heading])

        # update result to log
        result.append([flights[i][0], round(heading, 2), this_spec[LONGITUDE], this_spec[LATITUDE]])

        # set progress
        percent = float(i/N) * 100
        progress_callback.emit(percent)

    # run system command to update image with ground altitude information
    ## first, create a csv file
    csvname = join(folder, "update_heading.csv")
    header_ = ["SourceFile", "GimbalYawDegree"]
    with open(csvname, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=header_, delimiter=',')
        writer.writeheader()
        for r in update_txt:
            writer.writerow({header_[0]:r[0], header_[1]:str(r[1])})

    ## then, update tags
    with ExifTool() as et:
        status = et.write_tag_batch(csvname, folder)
        if not status:
            raise Exception('Failed calling batch update exiftool: [Input folder]: {0}'.format(folder))

    # format and return log
    log = formatResult(result)

    # compute average distance between photos
    avgdist = sum(distl) / len(distl)

    return {'heading': result, 'avgdist': avgdist, 'msg': log}
