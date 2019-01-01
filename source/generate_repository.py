#!/usr/bin/env python

import os
import shutil
import time
import subprocess

import glob
import zipfile
import xml.etree.ElementTree as ET

def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

def buildrepo(f):
    print "Checking for location: "+f
    #folder
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)
    print "Not Found! Creating: "+d

print "-----------------------------------------------------------------------------"
print "------------------------------------START------------------------------------"
print "-----------------------------------------------------------------------------"

addonxml      = "./addons.xml"
addonxmlmd5   = "./addons.xml.md5"

for x in os.listdir('./'):
    if (os.path.isfile(x)) or ('.git' in x):
        #### Skip it
        pass
    else: 
        print("Add-on Found: "+x)
        #### Make VARS:
        dest_dir = "../repo/"+x+"/"
        tree = ET.parse('./'+x+'/addon.xml')
        root = tree.getroot()
        version = root.get('version')
        print "Version: "+version
        isrepo = False
        if x == 'repository.ember':
            isrepo = True
        #### DO:
        buildrepo(dest_dir+"*")
        for file in glob.glob('./'+x+'/*changelog.txt'):
            print 'Copying: '+file+' >>>> '+dest_dir+'changelog-'+version+'.txt'
            shutil.copy(file, dest_dir+'changelog-'+version+'.txt')
        for file in glob.glob('./'+x+'/*icon.*'):
            print 'Copying: '+file+' >>>> '+dest_dir+'icon.png'
            shutil.copy(file, dest_dir)
        for file in glob.glob('./'+x+'/*fanart.*'):
            print 'Copying: '+file+' >>>> '+dest_dir+'fanart.jpg'
            shutil.copy(file, dest_dir)
        addon_zip = '../repo/'+x+'/'+x+'-'+version+'.zip'
        if not os.path.exists(addon_zip):
            print("Compressing "+x+'-'+version+'.zip...')
            zipf = zipfile.ZipFile('../repo/'+x+'/'+x+'-'+version+'.zip', 'w', zipfile.ZIP_DEFLATED)
            zipdir(x, zipf)
            zipf.close()
        else:
            print("!WARNING! Repository already contains "+x+'-'+version+'.zip. You will need to remove this first or increase the addons version number if you wish to overwirte the current version.')
        print("Add-on '"+x+"' Successfully Processed")
        print("")
        if isrepo:
            buildrepo("../downloads/*")
            print("Copy Repository '"+x+"' To Downloads DIR")
            shutil.copy('../repo/'+x+'/'+x+'-'+version+'.zip', '../downloads/'+x+'.zip')
            

shutil.copy(addonxml, "../repo/")
shutil.copy(addonxmlmd5, "../repo/")
os.remove(addonxml)
os.remove(addonxmlmd5)

#add version numbers to zip and changelog


print "---------------------------------------------------------------------------"
print "------------------------------------END------------------------------------"
print "---------------------------------------------------------------------------"

