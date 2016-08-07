from imguralbum import ImgurAlbumDownloader
from CBRSlide import CBRSlide
import os

IMGUR= "http://imgur.com/"
CBRIMGURALBUM = IMGUR + "a/"

class CBRAlbum():
    def __init__(self, name, loc):
        self.name = name
        self.__currPos = -1
        self.loc = loc
        self.slides = []
        self.__slidesLoc = self._loadSlidesDir()

        self.setPrintOptions()
        

    def addAllSlides(self):
        slideNum = range(len(self.__slidesLoc))
        self.addSlides(slideNum)
         
    def addTemplatesToAll(self, templates):
        for s in self:
            s.addTemplates(templates)

    def addTemplates(self, slideNum,templates):
        if type(slideNum) is int:
            getSlide(slideNum).addTemplates(templates)
        else:
            for n in slideNum:
                getSlide(n).addTemplates(templates)
        
    def addSlides(self, slideNum=[]):
        if type(slideNum) is int:
            self.__addSlide(slideNum)
        else:
            for n in slideNum:
                self.__addSlide(n)
        return               

    def __addSlide(self, slideNum):
        if len(self.__slidesLoc) <= slideNum:
            return ##raise?
        slide = CBRSlide(self.__slidesLoc[slideNum], slideNum)
        self.slides.append(slide)

    def getSlide(self, slideNum):
        for slide in self:
            if slide.slideNum == slideNum:
                return slide
        return None

    def _loadSlidesDir(self):
        slidesLoc = []
        if  CBRIMGURALBUM in self.loc:
            iad = ImgurAlbumDownloader(self.loc)
            imageIDs = iad.imageIDs
            for i in range(len(imageIDs)):
                url = IMGUR + "".join(iad.imageIDs[i])
                slidesLoc.append(url)
            
        else:
            files = os.walk(self.loc).next()[2]
            for f in files:
                slidesLoc.append(self.loc + "/" + f)
        return slidesLoc
    
    def setPrintOptions(self, skipNoMatches=True,extraInfo=False):
        self.extraInfo = extraInfo
        self.skipNoMatches = skipNoMatches
        for s in self:
            s.setPrintOptions(skipNoMatches,extraInfo)
            

     
    def findMatches(self, showMatches=False, saveMatchesTo=None):
        message = "Searching {0}".format(self)
        print message

        if saveMatchesTo is not None:
            if saveMatchesTo[-1] != "/": saveMatchesTo += "/"
            saveMatchesTo += str(self)
        for s in self:
            s.findMatches(showMatches,saveMatchesTo)
	    
    def __iter__(self):
        self.__currPos=0
        return self
    def next(self):
        if self.__currPos >= len(self.slides):
            raise StopIteration
        else:
            s = self.slides[self.__currPos]
            self.__currPos += 1
            return s

    def __str__(self):
        return self.name.split("The Official /r/Civ 60+ Civ Battle Royale! | ")[-1]
    

