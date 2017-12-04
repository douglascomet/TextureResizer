#==============================================================================
#!/usr/bin/env python
#title           :TexturePacker.py
#description     :Script used to pack textures using Photoshop
#author          :Doug Halley
#date            :20171204
#version         :1.0
#usage           :Standalone Python Application Executed by TextureResizer.exe
#notes           :
#python_version  :2.7.14
#pyqt_version    :4.11.4
#==============================================================================

import os
import sys
import comtypes.client

from _ctypes import COMError
from PIL import Image

from PyQt4 import QtGui
from PyQt4 import QtCore

class Main(QtGui.QMainWindow):
    """
    The class that contains, defines, and creates the UI
    """

    def __init__(self, parent=None):
        """
        Class init
        """
        super(Main, self).__init__(parent)
        self.initUI()

    def initUI(self):
        """
        Creates UI
        """

        #==============================================================================
        # Global Variables
        #==============================================================================

        # window title
        self.setWindowTitle("TextureResizer")

        #==============================================================================
        # PYQT Widget Defintions
        #==============================================================================

        # main widget
        self.centralWidget = QtGui.QWidget()
        self.centralWidget.setLayout(QtGui.QVBoxLayout())

        self.addDirectory = QtGui.QPushButton("Choose Directory")

        # widget for project location radio buttons and year combobox
        self.textureSizeWidget = QtGui.QWidget()
        self.textureSizeWidget.setLayout(QtGui.QHBoxLayout())

        channelInputs_lbl = QtGui.QLabel("Channel Inputs")
        
        self.rChannel_widget = QtGui.QWidget()
        self.rChannel_widget.setLayout(QtGui.QHBoxLayout())

        self.gChannel_widget = QtGui.QWidget()
        self.gChannel_widget.setLayout(QtGui.QHBoxLayout())

        self.bChannel_widget = QtGui.QWidget()
        self.bChannel_widget.setLayout(QtGui.QHBoxLayout())

        self.aChannel_widget = QtGui.QWidget()
        self.aChannel_widget.setLayout(QtGui.QHBoxLayout())

        self.rChannel_checkBox = QtGui.QCheckBox("R Channel")
        self.gChannel_checkBox = QtGui.QCheckBox("G Channel")
        self.bChannel_checkBox = QtGui.QCheckBox("B Channel")
        self.aChannel_checkBox = QtGui.QCheckBox("A Channel")

        self.rChannel_le = QtGui.QLineEdit("")        
        self.gChannel_le = QtGui.QLineEdit("")
        self.bChannel_le = QtGui.QLineEdit("")
        self.aChannel_le = QtGui.QLineEdit("")

        channelSearchText = 'Enter Prefix or Suffix'

        self.rChannel_le.setPlaceholderText(channelSearchText)
        self.gChannel_le.setPlaceholderText(channelSearchText)
        self.bChannel_le.setPlaceholderText(channelSearchText)
        self.aChannel_le.setPlaceholderText(channelSearchText)

        self.rChannel_widget.layout().layout().addWidget(self.rChannel_checkBox)
        self.rChannel_widget.layout().layout().addWidget(self.rChannel_le)

        self.gChannel_widget.layout().layout().addWidget(self.gChannel_checkBox)
        self.gChannel_widget.layout().layout().addWidget(self.gChannel_le)

        self.bChannel_widget.layout().layout().addWidget(self.bChannel_checkBox)
        self.bChannel_widget.layout().layout().addWidget(self.bChannel_le)

        self.aChannel_widget.layout().layout().addWidget(self.aChannel_checkBox)
        self.aChannel_widget.layout().layout().addWidget(self.aChannel_le)

        # creates combobox for year
        self.textureSize_comboBox = QtGui.QComboBox()

        for x in [4096, 2048, 1024, 512, 256, 128, 64]:
            self.textureSize_comboBox.addItem(QtCore.QString(str(x)))

        self.dirName_lbl = QtGui.QLabel("")
        self.dirName_lbl.setAlignment(QtCore.Qt.AlignCenter)

        self.preProcessTextures_btn = QtGui.QPushButton("Pre-Process Textures")
        self.processTextures_btn = QtGui.QPushButton("Process Textures")

        self.textureSizeWidget.layout().layout().addWidget(channelInputs_lbl)
        self.textureSizeWidget.layout().layout().addWidget(self.textureSize_comboBox)

        # adds project widget and tools widget to central widget
        self.centralWidget.layout().addWidget(self.addDirectory)
        self.centralWidget.layout().addWidget(self.dirName_lbl)
        self.centralWidget.layout().addWidget(self.rChannel_widget)
        self.centralWidget.layout().addWidget(self.gChannel_widget)
        self.centralWidget.layout().addWidget(self.bChannel_widget)
        self.centralWidget.layout().addWidget(self.aChannel_widget)
        self.centralWidget.layout().addWidget(self.preProcessTextures_btn)
        self.centralWidget.layout().addWidget(self.processTextures_btn)
        
        # sets central widget for PyQt window
        self.setCentralWidget(self.centralWidget)

        #==============================================================================
        # PYQT Execution Connections
        #==============================================================================

        # triggers for buttons
        self.addDirectory.clicked.connect(lambda: self.getDirectory())
        self.preProcessTextures_btn.clicked.connect(
            lambda: self.preProcessTextures(str(self.dirName_lbl.text())))
        self.processTextures_btn.clicked.connect(lambda: self.textureResize(str(self.dirName_lbl.text())))

    # creates QFileDialog to find designated folder
    def getDirectory(self):
        dlg = QtGui.QFileDialog.getExistingDirectory(
            None, 'Select a folder:', 'C:\\Users\\desktop', QtGui.QFileDialog.ShowDirsOnly)

        self.dirName_lbl.setText(dlg)
        print self.dirName_lbl.text()


    # Author: A.Polino - https://code.activestate.com/recipes/577514-chek-if-a-number-is-a-power-of-two/
    def is_power2(self, num):

        # states if a number is a power of two
        return num != 0 and ((num & (num - 1)) == 0)

    def preProcessTextures(self, path):
        #import collections
        #path = "C:\\Users\\dhalley\\Desktop\\GarageScene"
        #list_of_files = collections.OrderedDict()
        count = 0

        if self.osPath(path):

            for (dirpath, dirnames, filenames) in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.targa') or filename.endswith('.TGA'):

                        print filename
                        base_file, ext = os.path.splitext(filename)
                        print base_file
                        print type(base_file)
                        OriginalFileNamePath = os.path.join(dirpath, filename)
                        print OriginalFileNamePath
                        NewFileNamePath = os.path.join(dirpath, base_file + '.tga')
                        #in order to successfully rename a file you need the file joined with the path
                        os.rename(OriginalFileNamePath, NewFileNamePath)
                        list_of_files[filename] = os.sep.join([dirpath, filename])
                        count += 1
            if count == 0:
                self.popupOkWindow("There were not any files that needed their extensions formatted")
            else:
                self.popupOkWindow(str(count) + "Files had their extenstions changed to .tga")
            # for x, y in list_of_files.iteritems():
            #     print 'File Name: ', x
            #     print 'File Path: ', y
        
        else:
            self.popupOkWindow('Invalid Path')

    def textureResize(self, path):

        psFileLocation = path #"C:\\Users\\dhalley\\Desktop\\GarageScene"

        ext = (".tga", ".png")

        # counterer for number of files
        countTileable = 0

        # variable to check size of images by
        targetSize = 512

        # list used to collect images larger than targetSize
        largerThanTargetSize = []

        testPrint = ''

        rFound = ''
        gFound = ''
        bFound = ''
        aFound = ''

        # for x in os.listdir(psFileLocation):

        #     if self.rChannel_le.text():
        #         if str(self.rChannel_le.text()) in x:
        #             print x
        #             rFound = True

        # if not rFound:
        #     self.popupOkWindow('Not Found')
                    

        # walk through directory, sub directories, and files
        for (dirname, dirs, files) in os.walk(psFileLocation):
            
            # print dirname
            # if not dirs:
            #     print 'asdfasdfasdf' + str(dirs)
            # print files

            if dirs:

                # iterate over list of subdirectories
                for d in dirs:
                    
                    # precautionary check to ensure is valid path
                    if os.path.isdir(os.path.join(dirname, d)):

                        # iterate over entries in found subdirectory
                        for x in os.listdir(os.path.join(dirname, d)):
                                
                            # check if x during iteration is a file
                            if os.path.isfile(os.path.join(os.path.join(dirname, d, x))):
                                
                                print x

            else:
                
                # iterate over list of subdirectories
                for d in files:
                                
                    # check if x during iteration is a file
                    if os.path.isfile(os.path.join(dirname, d)):

                        # check if file extension exists in extension list
                        if d.lower().endswith('.tga'):
                            
                            # print d

                            if self.rChannel_le.text():
                                if str(self.rChannel_le.text()) in d:
                                    print d
                                    rFound = os.path.join(dirname, d)

                            if self.bChannel_le.text():
                                if str(self.bChannel_le.text()) in d:
                                    print d
                                    bFound = os.path.join(dirname, d)

                            if self.gChannel_le.text():
                                if str(self.gChannel_le.text()) in d:
                                    print d
                                    gFound = os.path.join(dirname, d)

                            if self.aChannel_le.text():
                                if str(self.aChannel_le.text()) in d:
                                    print d
                                    aFound = os.path.join(dirname, d)

                if rFound and gFound and bFound and aFound:
                    osVersion = self.checkWindowsVersion()
                    print self.checkPhotoshopVersion()
                    psApp = self.launchPhotoshop(osVersion)

                    r = psApp.Open(rFound)
                    
                    r.selection.selectAll()
                    r.activeLayer.Copy()

                    blankDoc = psApp.Documents.Add(1024, 1024, 72, "new_document", 2, 1, 1)

                    # blankDoc.channels['Red'] - equivalent to calling channel by name
                    # activeChannels must receive an array
                    blankDoc.activeChannels = [blankDoc.channels['Red']]
                    blankDoc.Paste()

                    g = psApp.Open(gFound)
                    g.selection.selectAll()
                    g.activeLayer.Copy()

                    psApp.activeDocument = blankDoc
                    blankDoc.activeChannels = [blankDoc.channels['Green']]
                    blankDoc.Paste()

                    b = psApp.Open(bFound)
                    b.selection.selectAll()
                    b.activeLayer.Copy()

                    psApp.activeDocument = blankDoc
                    blankDoc.activeChannels = [blankDoc.channels['Blue']]
                    blankDoc.Paste()

                    a = psApp.Open(aFound)
                    a.selection.selectAll()
                    a.activeLayer.Copy()

                    psApp.activeDocument = blankDoc
                    blankDoc.channels.add()
                    blankDoc.Paste()
                else:
                    self.popupOkWindow('POOP')

                                # # check if file extension exists in extension list
                                # if x.lower().endswith(ext):

                                #     # define imagePath string
                                #     imagePath = os.path.join(dirname, d, x)

                                #     # use PIL to create Image object
                                #     with Image.open(imagePath) as im:
                                #         sizeOfImage = im.size

                                #     # sizeOfImage returns tuple (width, height)
                                #     # check that image is square by comparing width and height
                                #     if sizeOfImage[0] == sizeOfImage[ 1 ]:
                                        
                                #         # if width/height are equal, use either value to check if power of 2
                                #         if self.is_power2(sizeOfImage[ 0 ]):
                                #             print x + ' - ' + '{0}'.format(sizeOfImage)
                                #             countTileable = countTileable + 1

                                #             if sizeOfImage[ 0 ] > targetSize:
                                #                 testPrint = testPrint + imagePath + '\n'
                                #                 largerThanTargetSize.append(imagePath)
                                
        # osVersion = self.checkWindowsVersion()
        # print self.checkPhotoshopVersion()
        # psApp = self.launchPhotoshop(osVersion)

        # version = psApp.Version
        # print version

        # print version
        # print psApp.path

        # for x in largerThanTargetSize:
        #     test = psApp.Open(x)

        #     psApp.Application.ActiveDocument

        #     test.resizeImage(targetSize, targetSize)
            
        #     filename, file_extension = os.path.splitext(x)

        #     newFileName = filename + '_' + \
        #         str(targetSize) + file_extension
        #     self.saveTGA(osVersion, psApp, newFileName)

        #     # close original version without saving
        #     test.Close(2)

    def checkWindowsVersion(self):
        import platform
        currentPlatform = platform.platform()

        if 'Windows' in currentPlatform:
            #splits windows version based on dashes
            splitPlatformName = currentPlatform.split('-')
            #returns windows version number
            return splitPlatformName[1]
        else:
            self.popupOkWindow('Untested OS. Tool only works on Windows')

    def checkPhotoshopVersion(self):
        
        #default Photoshop install path
        if self.osPath('C:\\Program Files\\Adobe\\'):
            
            # get list of folders in default Photoshop install path
            listdir = self.getPath('C:\\Program Files\\Adobe\\')

            # determine to see if a version of Photoshop is installed
            foundItems = [x for x in listdir if 'Photoshop' in x]

            if foundItems:
                
                # check how many versions of Photoshop are installed
                if len(foundItems) == 1:
                    foundPhotoshop = str(foundItems[0])

                    # check if a CC version of Photoshop is installed
                    if 'CC' in foundPhotoshop:
                        
                        # remove spaces from version of Photoshop
                        splitPhotoshop = foundPhotoshop.split(' ')

                        # get last element from split list
                        verNumber = splitPhotoshop[-1]

                        # create empty string to store value and testing
                        version = ''

                        # version 14
                        if verNumber == 'CC':
                            version = '70'
                        elif int(verNumber):
                            # version 15
                            if verNumber == '2014':
                                version = '80'
                            # version 16
                            elif verNumber == '2015':
                                version = '90'
                            # version 17
                            elif verNumber == '2016':
                                version = '100'
                            # version 18
                            elif verNumber == '2017':
                                version = '110'
                            # version 19
                            elif verNumber == '2018':
                                version = '120'

                        if version:
                            return version
                        else:
                            self.popupOkWindow('Error getting installed Photoshop Version')
                    else:
                        # if version.startswith('12'):
                        #     version = '12'
                        # elif version.startswith('13'):
                        #     version = '13'
                        self.popupOkWindow('Non CC Version of PS')
                else:
                    self.popupOkWindow('Multiple Versions of Photoshop installed')
            else:
                self.popupOkWindow('Photoshop not installed')
        else:
            self.popupOkWindow(
                'Adobe Software not installed in default directory')


    def launchPhotoshop(self, osVer):
        
        # if osVer == '10':
        psApp = comtypes.client.CreateObject('Photoshop.Application', dynamic = True)
        psApp.Visible = True

        #Set the default unit to pixels!
        psApp.Preferences.RulerUnits = 1

        return psApp

    def saveTGA(self, osVer, doc, tgaFile, saveAlpha=False):
        
        if osVer == '10':
            tgaOptions = comtypes.client.CreateObject(
                'Photoshop.TargaSaveOptions', dynamic=True)
            tgaOptions.Resolution = 24
            tgaOptions.AlphaChannels = False
            tgaOptions.RLECompression = False

            if saveAlpha:
                tgaOptions.Resolution = 32
                tgaOptions.AlphaChannels = True

            doc.ActiveDocument.SaveAs(tgaFile, tgaOptions, True)

    def popupDetailedOkWindow(self, message):
        """ Generic popup window with an OK button and can display message based on use """

        popupWindow = QtGui.QMessageBox()

        popupWindow.setText('Textures Found')
        popupWindow.setDetailedText(str(message))
        popupWindow.setStandardButtons(QtGui.QMessageBox.Ok)

        popupWindow.exec_()

    def popupOkWindow(self, message):
        """ Generic popup window with an OK button and can display message based on use """

        popupWindow = QtGui.QMessageBox()
        popupWindow.setText(message)
        popupWindow.setStandardButtons(QtGui.QMessageBox.Ok)

        popupWindow.exec_()
    
    #get list of directories if path exists
    def getPath(self, filePath):
        if self.osPath(filePath):
            return os.listdir(filePath)

    #determine if path exists
    def osPath(self, filePath):
        #print filePath
        #print type(filePath)
        if os.path.isdir(filePath):
            return True
        else:
            return False


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWidget = Main()
    myWidget.show()
    sys.exit(app.exec_())