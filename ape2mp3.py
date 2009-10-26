#
# This script was used to convert some FLAC/APE files to MP3
#
# Tools used: id3, lame, ffmpeg
#
# Stored here in case I will need to do this again.  There are several
# similar scripts on the net, but I chose to write my own because they
# were addressing more complicated issues and were using many more
# tools, some of which were not easy to install (not in apt
# repositories and no .deb available).
#


import os
import re
import glob
import os.path

class FileInfo:
    def __init__(self, fullName):
        mo = re.match(".*/(GB)/(\d+) - (.+)/\D*(\d+) - ([^.]*)", fullName)
        if mo == None:
            mo = re.match(".*/(GB)/(\d+) - (.+)/(\d+) ([^.]*)", fullName)
        if mo == None:
            mo = re.match(".*/(GB)/(\d+) - (.+)/(\d+)\. ([^.]*)", fullName)
        if mo == None:
            mo = re.match(".*/(GB)/(\d+) - (.+)/(\d+) GB - ([^.]*)", fullName)
        self.title = mo.groups()[4]
        self.track = mo.groups()[3]
        self.artist = mo.groups()[0]
        self.album = mo.groups()[2]
        self.year = mo.groups()[1]

def runCheck(cmd):
    if os.system(cmd) != 0:
        raise "Error from shell!"

def doDir(dirName):
    oldPath = os.getcwd()
    os.chdir(dirName)
    count = 0
    for f in glob.glob("*.ape") + glob.glob("*.flac"):
        fullName = os.getcwd() + "/" + f
        print fullName
        fi = FileInfo(fullName)
        ffmpegCmd = "ffmpeg -i \"%s\" \"%s.wav\"" % (f, f)
        mp3FileName = fi.title + ".mp3"
        lameCmd = "lame -h \"%s.wav\" \"%s\"" % (f, mp3FileName)
        id3Cmd = "id3 -g 48 -t \"%s\" -T \"%s\" -a \"%s\" -A \"%s\" -y \"%s\" \"%s\"" % (
            fi.title,
            fi.track,
            fi.artist,
            fi.album,
            fi.year,
            mp3FileName)
        rmCmd = "rm \"%s.wav\"" % (f,)
        runCheck(ffmpegCmd)
        runCheck(lameCmd)
        runCheck(id3Cmd)
        runCheck(rmCmd)
        count += 1
    os.chdir(oldPath)
    return count

sum = 0
for dirName in glob.glob("*"):    
    if os.path.isdir(dirName):
        sum += doDir(dirName)

print sum
