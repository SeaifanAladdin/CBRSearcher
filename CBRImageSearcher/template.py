import cv2
from cv2 import cv
import os

class Template():
    __location__ = os.getcwd()
    def __init__(self, url, threshold, colour = (0, 0, 255), setGrayScale=True, setCanny=True):
        if url[0] == ".":
            self.url = self.__location__ + url[1:]
        else:
            self.url = url
        self.colour = colour
        self.template = cv2.imread(self.url)
        if self.template == None:
            raise RuntimeError("Template not found")
        self.threshold = threshold
        self.grayScale = setGrayScale
        if setGrayScale:
            self.template = cv2.cvtColor(self.template, cv2.COLOR_BGR2GRAY)
        if setCanny:
            self.template = cv2.Canny(self.template, 50, 200)
        (tH, tW) = self.template.shape[:2]
        self.shape = (tH, tW)
    def showTemplate(self):
        cv2.imshow("template", self.template)
        cv2.waitKey(0)

    def getShape(self):
        return self.shape
        
    def __call__(self):
        return self.template

    def __str__(self):
        return self.url.split("/")[-1]


class LegionTemplate(Template):
    __location__ = os.path.dirname(os.path.realpath(__file__))
    URL =  "./../templates/legion_logo.jpeg"
    def __init__(self):
        Template.__init__(self, self.URL, 3750000., setGrayScale=False)

    def __str__(self):
        return "Legion"

class BallistaTemplate(Template):
    __location__ = os.path.dirname(os.path.realpath(__file__))
    URL =  "./../templates/ballista_logo.jpeg"
    def __init__(self):
        Template.__init__(self, self.URL, 5350000., colour=(0,255,0), setGrayScale=False)
    def __str__(self):
        return "Ballista"
