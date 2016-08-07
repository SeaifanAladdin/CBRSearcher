import cv2
from cv2 import cv
import os
import urllib
import numpy as np


import CBRAlbum

from Match import Match


class ImageAnalyzer():
    def __init__(self, slide, templates):
        self.slide = slide
        if ".gif" in slide.loc: raise RuntimeError("{0} is a .gif".format(slide))

        self.path = slide.loc
        if CBRAlbum.IMGUR in self.path:
            req = urllib.urlopen(self.path)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            self.image = cv2.imdecode(arr,-1)
        else:
            self.image = cv2.imread(self.path)
        
        self.matches = []

        self._matchTemplates(templates)

    def getMatchDetails(self,skipNoMatches=True,extraInfo=False):
        matchCount = ""
        for m in self.matches:
            if m.countMatches() ==0 and skipNoMatches: continue
            matchCount += "Found {0} matches with {1}\n".format(m.countMatches(), m.template)
            if extraInfo:  
                matchDetails = m.getMatchDetails()
                for detail in matchDetails:
                    matchCount+="\t Found at ({0},{1}) with value of {2}\n".format(*detail)
        return matchCount        
    def _matchTemplates(self, templates):
        if type(templates) is list:
            for template in templates:
                self._matchTemplate(template)
        else:
            self._matchTemplate(template)

    def _matchTemplate(self, template):
        self.matches.append(Match(self.image, template))

    def showImage(self):
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
        cv2.imshow("Image", self.image)
        
    def showMatches(self):
        newImage = self.image.copy()
        isNew = False;
        for m in self.matches:
            m.addMatchToImage(newImage)
            if m.matchFound: isNew=True
        if isNew:
            cv2.namedWindow("Matches", cv2.WINDOW_NORMAL)
            cv2.imshow("Matches", newImage)
            cv2.waitKey(0)

    def saveMatches(self, loc, forceSave=False):
        newImage = self.image.copy()
        isNew = False;
        for m in self.matches:
            m.addMatchToImage(newImage)
            if m.matchFound: isNew=True
        if isNew or forceSave:
            directory = loc[:-loc[::-1].find("/")]
            if not os.path.exists(directory):
                os.makedirs(directory)
            cv2.imwrite(loc, newImage)

  
    
