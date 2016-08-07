from CBRSlideAnalyzer import ImageAnalyzer

class CBRSlide():
    def __init__(self, loc, slideNum):
        self.loc = loc
        self.slideNum = slideNum
        self.templates = []

        self.setPrintOptions()
        
    def addTemplates(self, templates):
        if type(templates) is list:
            self.templates = self.templates + templates
        else:
            self.templates.append(templates)
            
    def setPrintOptions(self, skipNoMatches=True,extraInfo=False):
        self.extraInfo = extraInfo
        self.skipNoMatches = skipNoMatches
        
    
    def removeAllTemplates(self):
        self.templates = []

    def startAnalyzing(self):
        analyser = ImageAnalyzer(self, self.templates)
        return analyser

    def findMatches(self, showMatches=False, saveMatchesTo=None, printInfo=True):
        try:
            imageAnalyzer = self.startAnalyzing()
        except RuntimeError as e:
            print "Skipping: {0}".format(e)
            return
            
        if printInfo:
            matchMessage = imageAnalyzer.getMatchDetails(self.skipNoMatches,self.extraInfo)
            if matchMessage == "" and self.skipNoMatches:
                pass
            else:
                msg = "Matches at {0}".format(self)
                matchMessage = matchMessage.replace("\n", "\n\t")
                msg += "\n\t" + matchMessage
                print msg

        if saveMatchesTo is not None:
            saveMatchesTo += " {0}.{1}".format(str(self), self.loc.split(".")[-1])
        
        if showMatches:
            imageAnalyzer.showMatches()
        if saveMatchesTo is not None:
            imageAnalyzer.saveMatches(saveMatchesTo)
            

    def __str__(self):
        return "Slide #{0}".format(self.slideNum)
    

    
