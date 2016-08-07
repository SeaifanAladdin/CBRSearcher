import cv2
from cv2 import cv
import numpy as np

class Match():
    def __init__(self, image, template):
        self.image = image
        self.template = template
        self.colour = template.colour
        self.tW, self.tH = template.getShape()
        self.matchFound=False
        gray = image.copy()
        if template.grayScale:
            gray =  cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 200)
        
        self.result =cv2.matchTemplate(edged, template(), cv2.TM_CCORR)
        self.findMatch()

    def findMatch(self):
        self.loc = np.where(self.result >=self.template.threshold)

    def countMatches(self):
        return len(self.loc[0])

    def getMatchDetails(self):
        matchDetails = []
        for pt in zip(*self.loc[::-1]):
            matchDetails = matchDetails + [[pt[0], pt[1], self.result[pt[1],pt[0]]]]
        return matchDetails

        
    def addMatchToImage(self, image):
        for pt in zip(*self.loc[::-1]):
            self.matchFound=True
            (startX, startY) = (int(pt[0]), int(pt[1]))
            (endX, endY) = (int((pt[0] + self.tW)), int((pt[1] + self.tH)))
            cv2.rectangle(image, (startX, startY), (endX, endY), self.colour, 2)
        
