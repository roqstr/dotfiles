from subprocess import call, check_output, Popen
from os import walk
from PIL import ImageFilter, Image
from colorparser import execute_gcolorchange
import os.path
import random
import fileinput
import shutil
import re
import signal

files = []

walldir = "/home/marco/.wallpapers/"
slimbg = "/usr/share/slim/themes/blurry-clean/background.png"
captainconf = "/home/marco/.config/captain/captainrc"

for( dirpath, dirnames, filenames ) in walk( walldir ):
    files.extend( filenames )


files = [ elem for elem in files if not ".Xres" in elem ]
files = [ elem for elem in files if not ".sample" in elem ]
files = [ elem for elem in files if not ".colors" in elem ]
files = [ elem for elem in files if not ".current" in elem ]
files = [ elem for elem in files if not ".sh" in elem ]

x = random.randint(0, len(files) - 1)
file = "." + files[x] + ".Xres" 
#for setting a random wallpaper
call( [ "wp", "change", files[x] ] )
#for setting a random colorscheme that fits
call( [ "xrdb", "-merge", walldir + file ] )
execute_gcolorchange( files[x] )

inputString = """#!/bin/bash 
wpcscript change """ + files [x] + " && xrdb -merge /home/marco/.wallpapers/." + files [x] + ".xres"
text_file = open(walldir + "wp_init.sh", "w")
text_file.write(inputString)
text_file.close()

shutil.copy(walldir + files[x], slimbg)
im = Image.open(slimbg)
imBlurred = im.filter(ImageFilter.GaussianBlur(10.0)) 
imBlurred.save(slimbg, "PNG")

colorFile = open('.main_colors',"r")
rawColor = colorFile.read()
colorFile.close()
colors = re.findall(r'[a-fA-F0-9]{6}', rawColor) #[0] is foreground, [1] is background
	
captainrc = open(captainconf, "r")
captainrcContent = captainrc.read()
captainrc.close()

rgbColors = []
argbColors = []
for color in colors:
    rgbColors.append( "#" + color )
    argbColors.append( "#FF" + color )


captainrcContent = re.sub(r'background = "#[a-fA-F0-9]{8}"', 'background = "' + argbColors[1]  + '"' , captainrcContent)
captainrcContent = re.sub(r'foreground = "#[a-fA-F0-9]{8}"', 'foreground = "' + argbColors[0] + '"', captainrcContent)

captainrc = open(captainconf, "w")
captainrc.write(captainrcContent)
captainrc.close()

os.kill(int(check_output(["pidof","lemonbar"])), signal.SIGTERM) 
Popen( 'captain', shell=True) 
