from subprocess import call, check_output, Popen
from os import walk
from PIL import ImageFilter, Image
from colorparser import execute_gcolorchange
#from matplotlib.colors as colors
import os.path
import random
import fileinput
import shutil
import re
import signal

walldir = "/home/marco/.wallpapers/"
slimbg = "/usr/share/slim/themes/blurry-clean/background.png"
captainconf = "/home/marco/.config/captain/captainrc"
xres = "/home/marco/.Xresources"

files = []
rgbColors = []
argbColors = []
rofiColors = []
try:
     os.kill(int(check_output(["pidof","lemonbar"])), signal.SIGTERM) 
     os.kill(int(check_output(["pidof","rofi"])), signal.SIGTERM)
except:
    print("Could not kill rofi & captain")

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


#SLIM
shutil.copy(walldir + files[x], slimbg)
im = Image.open(slimbg)
imBlurred = im.filter(ImageFilter.GaussianBlur(10.0)) 
imBlurred.save(slimbg, "PNG")

colorFile = open('.main_colors',"r")
rawColor = colorFile.read()
colorFile.close()
colors = re.findall(r'[a-fA-F0-9]{6}', rawColor) #[0] is foreground, [1] is background

#CAPTAIN	
captainrc = open(captainconf, "r")
captainrcContent = captainrc.read()
captainrc.close()
for color in colors:
    rgbColors.append( "#" + color )
    argbColors.append( "#FF" + color )
    rofiColors.append( "argb:AA" + color )

clouds = "#ffecf0f1"
darkbg = "#ff222222"

#colors.hex2color(clouds)
#colors.hex2color(midnight)



captainrcContent = re.sub(r'background = "#[a-fA-F0-9]{8}"', 'background = "' + darkbg  + '"' , captainrcContent)
captainrcContent = re.sub(r'foreground = "#[a-fA-F0-9]{8}"', 'foreground = "' + argbColors[0] + '"', captainrcContent)
captainrc = open(captainconf, "w")
captainrc.write(captainrcContent)
captainrc.close()

xresources = open(xres, "r")
xresContent = xresources.read()
xresources.close()

#ROFI
xresContent = re.sub(r'rofi.color-window: argb:.{8},', 'rofi.color-window: ' + rofiColors[1] + ',', xresContent)
xresContent = re.sub(r'rofi.color-active: argb:.{8},', 'rofi.color-active: ' + rofiColors[0] + ',', xresContent)
#manipulate rofi colors
xresources=open(xres, "w")
xresources.write(xresContent)
xresources.close()

call( [ "xrdb", "-merge", xres ] )
Popen( 'captain', shell=True)
Popen( 'rofi', shell=True)
