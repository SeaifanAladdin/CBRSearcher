import sys

import lxml.html
import os
from CBRImageSearcher.CBRAlbum import CBRAlbum, CBRIMGURALBUM
import CBRImageSearcher.template as template

import numpy as np

CBRIMGUR = "http://civbattleroyale.imgur.com/"
CBRIMGURALBUM = CBRIMGURALBUM + "{0}"

class CBRSearcher():
    def __init__(self, rootLocation=None):
        if rootLocation == None:
            rootLocation = CBRIMGUR
        self.loc = rootLocation
            
        self.albums = []
        self.__albumDir = self.__loadAlbumDir()

    def addTemplatesToAll(self, templates):
        for album in self.albums:
            album.addTemplatesToAll(templates)

    def addTemplateToAllInAlbum(self, albumNames, templates):
        albums = getAlbum(albumNames)
        if type(albums) is list:
            for a in albums:
                a.addTemplatesToAll(templates)
        else:
            albums.addTemplatesToAll(templates)

    def addTemplateToSlideInAlbum(self, albumName, slideNum, templates):
        album = getAlbum(albumName)
        if type(album) is list:
            for a in album:
                a.addTemplates(slideNum, templates)
        else:
            album.addTemplates(slideNum, templates)


    def getAlbum(self, name):
        if type(name) is list:
            albums = []
            for n in name:
                for album in self.albums:
                    if str(n) in album.name:
                        albums.append(album)
                        break
            return albums
        else:
            for album in self.albums:
                if str(name) in album.name:
                    return album
   
        
    def addAllAlbums(self, addAllSlides=True):
        self.albums = []
        if self.loc == CBRIMGUR:
            for a in self.__albumDir.keys():
                self.__addAlbum(a,addAllSlides)
        else:
            ##TODO
            ##Do the same but for a directory
            pass
    def __addAlbum(self,name, addAllSlides):
        if name in self.__albumDir.keys():
            album = CBRAlbum(name,self.__albumDir[name])
            self.albums.append(album)
            if addAllSlides:
                album.addAllSlides()
        else:
            pass ##Raise a warning
    def addAlbums(self, albumName, addAllSlides=True):
        if type(albumName) is list:
            for name in albumName:
                self.__addAlbum(name,addAllSlides)
        else:
            self.__addAlbum(albumName, addAllSlides)

    def __loadAlbumDir(self):        
        albums = {}
        if self.loc == CBRIMGUR:
            t = lxml.html.parse(self.loc)
            elements = t.find(".//body").get_element_by_id("content").getchildren()[0].getchildren()[0].get_element_by_id("items").getchildren()
            for e in elements:
                albumID, albumName = e.values()[:2]
                albumID = albumID.split("-")[1]
                albumPath = CBRIMGURALBUM.format(albumID)
                albums[albumName] = albumPath
        else:
            album = np.array(os.walk(self.loc).next()[1])
            for s in album:
                albums[s] = self.loc + s
            
        return albums
    

    def findMatches(self, showMatches=True, saveMatchesTo=None):
        for album in self.albums:
            album.findMatches(showMatches,saveMatchesTo)

    def setPrintOptions(self, skipNoMatches=True,extraInfo=False):
        for album in self.albums:
            album.setPrintOptions(skipNoMatches, extraInfo)

                

if __name__=="__main__":
    args = sys.argv
    
    OPTIONS = ["-t", "-a", "-w", "-s", "-d"]
    cbr = None
    templates = []
    albums = []
    show = True
    writeTo = None
    detailedPrint = False
    for i in range(1,len(args)):
        if i == 1:
            loc=None
            if args[i] not in OPTIONS:
                loc = args[i]
            cbr = CBRSearcher(loc)
            
        if args[i] == OPTIONS[0]:
            if args[i+1].lower() == "legion":
                templates.append(template.LegionTemplate())
            elif args[i+1].lower() == "ballista":
                templates.append(template.BallistaTemplate())
            else:
                templates.append(template.Template(args[i+1], float(args[i+2])))
        elif args[i] == OPTIONS[1]:
            albums.append(args[i+1])
        elif args[i] == OPTIONS[2]:
            writeTo = args[i+1]
        elif args[i] == OPTIONS[3]:
            if args[i+1].lower() == "false" or args[i+1] == "0":
                show = False
        elif args[i] == OPTIONS[4]:
            if args[i+1].lower() == "true" or args[i+1] == "1":
                detailedPrint = True
    if albums == []:
        print "Please wait..."
        cbr.addAllAlbums()
    else:
        cbr.addAlbums(albums)
    cbr.addTemplatesToAll(templates)
    cbr.setPrintOptions(not detailedPrint, detailedPrint)
    cbr.findMatches(show, writeTo)
    
