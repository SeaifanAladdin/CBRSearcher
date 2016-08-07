#CivBattleRoyale Searcher

Keeping track of a unit, city, or any object from the CivBattleRoyale? 
Well No need to manually go through thousands of slides. Either use the python modules or the command line interface, and this python script will do the searching for you!

----------
##Requirements
* Python 2.7
* Numpy
* OpenCV
* ...

## Usage
###Command Line Usage

Example
```
$ cd CBRSearcher
$ python CBRSearcher.py ./someLocalDirectory/ -a "albumName" -t legion -t ./CBRImageSearcher/templates/ballista_logo.jpeg  4400000. -s false -w ./matches/ -d true
```

`./someLocalDirectory/`  is a directory which contain folders of albums.
If you want to load the albums from http://civbattleroyale.imgur.com/ instead, don't include it.

`-a "albumName"` adds an album from inside `./someLocalDirectory/`  that contains images you want to search. If you did not pass in localDirectory, then albumName will be the name of the album from [here](http://civbattleroyale.imgur.com/).
If you want to pass in multiple albums,  then you can add multiple `-a "albumName"`arguments. For example,
```
$ python CBRSearcher.py -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 67" -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 66" -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 61"  .....
```

Now you'll need to add templates. This will be the object you want to find in the slides you added. An example  is the Roman Ballista template


![](https://raw.githubusercontent.com/SeaifanAladdin/CBRSearcher/master/templates/ballista_logo.jpeg" Ballista Template")

To add a template, use
`-t pathToTemplate  threshold`
`pathToTemplate` is the path to the template you're interested in. 

Since I've already included the Ballista Template, we can set `pathToTemplate = ./templates/ballista_logo.jpeg `
When doing the matching, we want a `threshold` value high enough to avoid incorrect matches, yet low enough to avoid missing matches that we do want.  With images you know have matches, you can play around with `threshold` and determine which gives you your ideal matches.  The `-d` option is there to give you more details, which can be used to help with this.

Alternatively, you can use `-t legion` or/and `-t ballista`, where I've already selected the ideal threshold value for you.

Set the `-s` option if you want to show matches or not.

Finally `-w ./matches/` will save your matches to the directory `./matches/`. If you do not want to save, leave out the option.

An example of searching for the Roman Ballista and Legion on part 67, 66, and 61:
```
$ cd CBRSearcher
$ python CBRSearcher.py -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 67" -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 66" -a "The Official /r/Civ 60+ Civ Battle Royale! | Part 61" -t legion -t ballista -s false -w ./matches/
```


###Module Usage

An example of searching for the Roman Ballista and Legion:
```python
##Imports
from CBRSearcher import CBRSearcher
import CBRImageSearcher.template as template

##Let's add all of the albums in civbattleroyale.imgur.com
cbr = CBRSearcher()
cbr.addAllAlbums()

##Let's add our templates
legion = template.LegionTemplate()
ballista = template.BallistaTemplate()
templates = [legion, ballista]
cbr.addTemplates(templates)

##Now let's find our matches!
writeTo = "./matches/"
show = False
cbr.findMatches(show, writeTo)
```

####More Information
To create a CBRSearcher instance:
```python
from CBRSearcher import CBRSearcher
cbr = CBRSearcher(localDirectory) 
```
where `localDirectory` is a directory which contain folders of albums.
If you want to load the albums from http://civbattleroyale.imgur.com/ instead, don't pass any parameters. 
```python
from CBRSearcher import CBRSearcher
##Will load from http://civbattleroyale.imgur.com/
cbr = CBRSearcher() 
```

Next you'll need to load the albums from the directory.
```python
cbr.addAlbums(albumName)
```
 `albumName` will be the name of the folder inside `localDirectory` that contains images you want to search. If you did not pass in `localDirectory`, then `albumName` will be the name of the album from [here](http://civbattleroyale.imgur.com/).
`albumName` can also be a list. For example
```python
albumNames = [
"The Official /r/Civ 60+ Civ Battle Royale! | Part 67", 
"The Official /r/Civ 60+ Civ Battle Royale! | Part 66", 
"The Official /r/Civ 60+ Civ Battle Royale! | Part 61"]
cbr.addAlbums(albumNames)
```

If you want to add all of the albums, call `cbr.addAllAlbums()`. Note, this will take a few minutes if you're adding the albums from imgur.

Next, you'll want to create your template. This will be the object you want to find in the slides you'll create. An example  is the Roman Ballista template

![](https://raw.githubusercontent.com/SeaifanAladdin/CBRSearcher/master/templates/ballista_logo.jpeg" Ballista Template")
To create a template
```python
import CBRImageSearcher.template as template
ballista = template.Template(pathToTemplate, threshold) 
```
Since I've already included the Ballista Template, we can set `pathToTemplate = "./templates/ballista_logo.jpeg"` 
When doing the matching, we want a `threshold` value high enough to avoid incorrect matches, yet low enough to avoid missing matches that we do want.  With images you know have matches, you can play around with `threshold` and determine which gives you your ideal matches.  I have also included `cbr.setPrintOptions(skipNoMatches=True, extraInfo=False)`if you require more detailed information. 

With the ballista, I found my ideal threshold value to be `threshold=4400000.`

There are also other parameters such as `colour`, `setGrayScale`, `setCanny`.
`colour` is the colour of the box that you'll want to trace over your match
`setGrayScale` will set your template (and the slides it's matching against) to grayscale. 
`setCanny` which will keep only the corners and edges it can find in your template (and the slides it's matching against).

For your convenience, there are templates already prepared for you. They can be created by
```python
import CBRImageSearcher.template as template
legion = template.LegionTemplate()
ballista = template.BallistaTemplate()
```
You can add them by
```python
templates = [legion, ballista]
cbr.addTemplatesToAll(templates)
```

Once you have everything ready, use the cbr.findMatches method
```python
cbr.findMatches(show, writeTo)
```
`show` is a boolean which is set to `True` by default. This will show you the image with the matches. `writeTo` is a path to a directory where you want to save your matches. If you don't want to save your matches, then you can remove it.

### Tests and bugs
Limitted testing has been done, and any reports on bugs will be appreciated. 

I have not tested this with python 3, and there may be required python packages that I have forgotten to include

### Support CivBattleRoyale
[reddit subredit](https://www.reddit.com/r/civbattleroyale)

Any help with improving this will be greatly appreciated

