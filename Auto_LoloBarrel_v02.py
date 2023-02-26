import os
import sys
import importlib
import maya.cmds as cmds


from maya import OpenMayaUI as omui
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import re

# To add e new map or Tag
pref = {
            "BaseColor": [['Albedo', 'BaseColor', 'BaseColo'], 'outColor', 'baseColor'],
            "Roughness": [['Roughness'], 'outAlpha', 'specularRoughness'],
            "Normal": [['Normal'], 'outValue', 'normalCamera'],
            "Metallic": [['Metalness'], 'outAlpha', 'metalness'],
            "Opacity": [['Opacity'], 'outColor', 'opacity']
        }


def maya_main_window():
    '''
    Return the Maya main window widget as a Python object
    '''
    main_window_ptr = omui.MQtUtil.mainWindow()

    if sys.version_info.major >= 3:
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

class Set_PrefUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(Set_PrefUI, self).__init__(parent)
        self.qtSignal = QtCore.Signal()
        #################################################################

        self.setWindowTitle('Set Tags')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 150)

        self.mapDict2 = pref

        self.bg = QtGui.QColor(75, 75, 75)
        self.light = QtGui.QColor(100, 100, 100)
        self.dark = QtGui.QColor(45, 45, 45)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(4, 4, 4, 4)

        self.widgetTable = QtWidgets.QWidget(self)
        self.widgetTable_layout = QtWidgets.QVBoxLayout(self.widgetTable)
        self.widgetTable.setStyleSheet(f" background-color: {self.bg.name()}")
        for map in self.mapDict2:
            self.widgetTable1 = QtWidgets.QWidget(self)
            self.widgetTable_layout1 = QtWidgets.QHBoxLayout(self.widgetTable1)
            # Label
            self.mapDict2[map].append(QtWidgets.QLabel(f"{map} :"))
            self.widgetTable_layout1.addWidget(self.mapDict2[map][-1])

            # Tag list 2
            tag_list = self.mapDict2[map][0]
            self.mapDict2[map].append(QtWidgets.QLineEdit(" ".join(tag_list)))
            self.mapDict2[map][-1].setStyleSheet(f" background-color: {self.dark.name()}")
            self.widgetTable_layout1.addWidget(self.mapDict2[map][-1])
            """
            # Out 1
            self.mapDict[map].append(QtWidgets.QLineEdit(pref[map][1]))
            self.widgetTable_layout1.addWidget(self.mapDict[map][-1])

            # Map 0
            self.mapDict[map].append(QtWidgets.QLineEdit(pref[map][2]))
            self.widgetTable_layout1.addWidget(self.mapDict[map][-1])
            """
            self.widgetTable_layout.addWidget(self.widgetTable1)

        x= 125
        y= 40
        self.savebtn = QtWidgets.QPushButton(" Save ")
        self.savebtn.setFixedSize(QtCore.QSize(x, y))
        self.savebtn.clicked.connect(self.save)

        self.applybtn = QtWidgets.QPushButton(" Apply ")
        self.applybtn.setFixedSize(QtCore.QSize(x, y))
        self.applybtn.clicked.connect(self.apply)

        self.closebtn = QtWidgets.QPushButton(" Close ")
        self.closebtn.setFixedSize(QtCore.QSize(x, y))
        self.closebtn.clicked.connect(self.toggle_window_pref)

        self.widgetBtn = QtWidgets.QWidget(self)
        self.widgetBtn_layout = QtWidgets.QHBoxLayout(self.widgetBtn)
        self.widgetBtn_layout.addWidget(self.savebtn)
        self.widgetBtn_layout.addWidget(self.applybtn)
        self.widgetBtn_layout.addWidget(self.closebtn)
        self.widgetBtn_layout.setContentsMargins(4, 4, 4, 4)

        self.warn = QtWidgets.QLabel(" Not case sensitive")
        self.warn.setStyleSheet(
            f"color: {QtGui.QColor(250, 250, 250).name()}; background-color: {QtGui.QColor(200, 75, 75).name()};"
            f" padding: 6px;"
            f" font: bold 12px;"
            f" border-style: solid;"
            f" border-width: 2px;"
            f" border-radius: 10px;"
            f"border-color: {QtGui.QColor(100, 50, 50).name()}")

        self.mainLayout.addWidget(self.warn)
        self.mainLayout.addWidget(self.widgetTable)
        self.mainLayout.addWidget(self.widgetBtn)

    def apply(self):
        for map in pref:
            # Tag list
            newTag = self.mapDict2[map][-2].text().upper().split(" ")
            self.setTag(map, newTag)
            """
            # Out
            newTag = self.mapDict[map][-2].text().upper().split(" ")
            self.setTag(map, newTag)
            # Map
            newTag = self.mapDict[map][-2].text().upper().split(" ")
            self.setTag(map, newTag)
            """

    def save(self):
        for map in pref:
            # Tag list
            newTag = self.mapDict[map][-2].text().upper().split(" ")
            self.setTag(map, newTag)
            """
            # Out
            pref[map][1] = self.mapDict[map][1].text()
            # Map
            pref[map][2] = self.mapDict[map][0].text()
            """

    def setTag(self, key: str, val: list):
        """
            Set the Tag
        """
        pref[key][1] = val

    def setOut(self, key: str, val: str):
        """
            Set the Tag
        """
        pref[key][2] = val

    def setMap(self, key: str, val: str):
        """
            Set the Tag
        """
        pref[key][3] = val

    def close(self):
        self.deleteLater()

    def toggle_window_pref(self):
        if self.isVisible():
            self.hide()

        else:
            self.show()


class Auto_LoloBarrelUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(Auto_LoloBarrelUI, self).__init__(parent)
        self.qtSignal = QtCore.Signal()
        #################################################################

        self.window1 = Set_PrefUI()

        self.setWindowTitle('Auto Lolo Barrel v0.2')
        self.setWindowFlags(QtCore.Qt.Tool)
        self.resize(300, 150)

        self.bg = QtGui.QColor(75, 75, 75)
        self.light = QtGui.QColor(100, 100, 100)
        self.dark = QtGui.QColor(45, 45, 45)


        # Map list to modify to add a new one
        #       "Name" : [ ['Tag1','Tag2'], out, map ]
        #
        self.mapDict = pref
        for mapDict in self.mapDict:
            self.mapDict[mapDict].append(False)

        self.menubar = QtWidgets.QMenuBar()
        self.editMenu = QtWidgets.QMenu('Edit')
        self.helpMenu = QtWidgets.QMenu('Help')
        self.menubar.addMenu(self.editMenu)
        self.menubar.addMenu(self.helpMenu)

        button_action = QtWidgets.QAction('Tags', self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.toggle_window_pref)
        self.editMenu.addAction(button_action)

        self.pathLabel = QtWidgets.QLabel("Path :")
        self.path = QtWidgets.QLineEdit('')
        self.path.setStyleSheet("QWidget { background-color: %s }" % self.dark.name())
        self.allpath = QtWidgets.QCheckBox('allpath')

        self.fialdial = QtWidgets.QPushButton("")
        self.fialdial.setIcon(QtGui.QIcon(r':/folder-closed.png'))
        self.fialdial.setStyleSheet("QWidget { background-color: %s }" % self.light.name())
        #self.fialdial.setIconSize(QtCore.QSize(151, 150))

        self.mapLabel = QtWidgets.QLabel("Map :")
        self.setAll = QtWidgets.QCheckBox('All')
        self.setAll.setChecked(True)
        for map in self.mapDict:
            self.mapDict[map].insert(0, QtWidgets.QCheckBox(map))
        self.setDisplacement = QtWidgets.QCheckBox('Displacement')


        self.titleMode = QtWidgets.QLabel("Mode :")
        self.mode = QtWidgets.QComboBox()
        self.mode.setStyleSheet("QWidget { background-color: %s }" % self.light.name())
        self.mode.addItem('Link Texture', userData=0)
        self.mode.addItem('Create Shader', userData=1)


        self.connectMap = QtWidgets.QPushButton("Apply")
        self.connectMap.setFixedSize(QtCore.QSize(350, 50))

        # Layout
        #
        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.mainLayout.setContentsMargins(4, 4, 4, 4)

        ## Path
        self.widgetPath = self.HColumn([self.pathLabel, self.path, self.fialdial])
        self.widgetPath.setStyleSheet(
            f" background-color: {self.bg.name()};"
            f" padding: 6px;"
            f" font: bold 12px;"
            f" border-width: 2px;"
            f" border-radius: 10px;"
            f"border-color: {QtGui.QColor(5, 5, 5).name()}")

        ## Checkbox
        self.widgetCheckbox = QtWidgets.QWidget(self)
        self.widgetCheckbox_layout = QtWidgets.QVBoxLayout(self.widgetCheckbox)


        self.widgetCheckbox_layout.addWidget(self.setAll)
        self.split = QtWidgets.QLabel("-------------------------------------------------------------------------------")
        self.widgetCheckbox_layout.addWidget(self.split)
        self.widgetCheckboxIndent = QtWidgets.QWidget(self)
        self.widgetCheckboxIndent_layout = QtWidgets.QVBoxLayout(self.widgetCheckboxIndent)
        for map in self.mapDict:
            self.widgetCheckboxIndent_layout.addWidget(self.mapDict[map][0])
        self.widgetCheckbox_layout.addWidget(self.widgetCheckboxIndent)
        self.split2 = QtWidgets.QLabel("-------------------------------------------------------------------------------")
        self.widgetCheckbox_layout.addWidget(self.split2)

        self.warn = QtWidgets.QLabel(" Activer les subdiv catclark si usage du Displacment")
        self.widgetCheckbox_layout.addWidget(self.warn)
        self.warn.setStyleSheet(f"color: {QtGui.QColor(250, 250, 250).name()}; background-color: {QtGui.QColor(200, 75, 75).name()};"
                                f" padding: 6px;"
                                f" font: bold 12px;"
                                f" border-style: solid;"
                                f" border-width: 2px;"
                                f" border-radius: 10px;"
                                f"border-color: {QtGui.QColor(100, 50, 50).name()}")

        self.widgetCheckbox_layout.addWidget(self.setDisplacement)
        self.widgetCheckbox.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        ## Mode
        self.widgetMode = self.HColumn([self.titleMode, self.mode])
        self.widgetMode.setStyleSheet("QWidget { background-color: %s }" % self.bg.name())

        self.mapLabel.setStyleSheet("QWidget { background-color: %s }" % self.light.name())
        self.mapLabel.setMargin(10)

        # Add to main Layout
        self.mainLayout.addWidget(self.menubar)

        self.mainLayout.addWidget(self.widgetPath)
        self.mainLayout.addWidget(self.allpath)

        self.temp = QtWidgets.QLabel("   ")
        self.mainLayout.addWidget(self.temp)
        self.mainLayout.addWidget(self.mapLabel)
        self.mainLayout.addWidget(self.widgetCheckbox)

        self.mainLayout.addWidget(self.widgetMode)
        self.mainLayout.addWidget(self.connectMap)

        #  Connect Button
        self.fialdial.clicked.connect(self.openFileDial)
        self.connectMap.clicked.connect(self.Apply)


    #
    # Functions
    #

    # Ui functions
    #

    def toggle_window_pref(self, checked):
        if self.window1.isVisible():
            self.window1.hide()

        else:
            self.window1.show()


    def openFileDial(self):
        newpath = cmds.fileDialog2(fileFilter="All Files (*.*)", dialogStyle=2, fileMode=2)[0]
        self.path.setText(newpath)
        self.path.update()

    def HColumn(self, widget_list):
        """ Create a H column layout adding the widgets specified

                Args:
                    list widget_list : list of the widgets to add

                Returns:
                    a widget with a Hlayout containing spécified widgets
        """

        widget = QtWidgets.QWidget(self)
        widget_layout = QtWidgets.QHBoxLayout(widget)
        for widgets in widget_list:
            widget_layout.addWidget(widgets)

        return widget


    def closeEvent(self, event):
        self.window1.close()
        event.accept()


    # Scripts functions
    #


    def checkdoss(self, path, allpath: bool):
        """
            Check doss in given path n

                return: text_for_shd list: texture found

        """
        text_for_shd = []

        # Check doss in path
        for doss in os.listdir(path):
            dosspath = path + '\\' + doss

            if os.path.isdir(dosspath):
                if allpath:
                    self.checkdoss(dosspath)

            else:
                if self.sg_name.upper() in doss.upper():
                    text_for_shd.append(doss)
                elif self.shd_name.upper() in doss.upper():
                    text_for_shd.append(doss)
                else:
                    continue

        return text_for_shd

    def Apply(self):
        mode = self.mode.currentData()
        to_create_list =[]
        if mode == 0:
            #Link Texture
            self.ConnectMap()
        elif mode == 1:
            #Create Shader
            path = self.path.text()
            for texture_name in os.listdir(path):
                for x in self.mapDict["BaseColor"][1]:
                    if x.upper() in texture_name.upper():
                        name = re.search(f".+?(?={x.upper()})", texture_name.upper())
                        if not name[0] in to_create_list:
                            to_create_list.append(name[0])

            # check if shader doesn't already exist in scene
            for name in to_create_list:
                if not cmds.objExists(name):
                    # Create Shader
                    shader = self.CreateShader(name)

                    # select shader n run connect map
                    cmds.select(shader)
                    self.ConnectMap()

                else:
                    cmds.warning(f'Conflict Names, rename existing shader {name} or rename texture map of given path')
                    continue


    def CreateShader(self, name, node_type="aiStandardSurface"):
        material = cmds.shadingNode(node_type, name=name, asShader=True)
        sg = cmds.sets(name="%sSG" % name, empty=True, renderable=True, noSurfaceShader=True)
        cmds.connectAttr("%s.outColor" % material, "%s.surfaceShader" % sg)
        return material

    def ConnectMap(self, *args):

        path = self.path.text()
        allpath = self.allpath.isChecked()


        # Check for Checkbox state
        AllCheck = self.setAll.isChecked()
        if AllCheck:
            Check = True
        else:
            for key in self.mapDict:
                Check = self.mapDict[key][0].isChecked()

        DisplacementCheck = self.setDisplacement.isChecked()


        # Start
        sl = cmds.ls(sl=1)
        if not sl:
            cmds.error('Please select a shader to link to')

        for s in sl:
            self.shd_name = s
            self.sg_name = cmds.listConnections(s, d=True, s=False)[-1]

            for mapDict in self.mapDict:
                self.mapDict[mapDict][-1] = True
            self.DisplacementDone = 0

            self.text_for_shd = []
            self.map = ''
            self.out = ''

            # Check already Connected files  of the shader
            # Add a force connection option
            for i in self.list(s):
                for mapDict in self.mapDict:
                    if mapDict.upper() in i.upper():
                        Check = False


            if 'DISPLACEMENT' in cmds.listConnections(self.sg_name, s=True)[-1].upper():
                DisplacementCheck = False

            # Check doss in path
            self.text_for_shd = self.checkdoss(path, allpath)

            # Assign map
            for texture in self.text_for_shd:
                textureUpper = texture.upper()

                self.map = 'skip'

                for mapDict in self.mapDict:
                    tag_list = self.mapDict[mapDict][1]
                    mapOut = self.mapDict[mapDict][2]
                    map = self.mapDict[mapDict][3]
                    done = self.mapDict[mapDict][-1]

                    for x in tag_list:
                        if x.upper() in textureUpper and done is True and Check is True:
                            self.out = mapOut
                            self.map = map

                            self.mapDict[mapDict][-1] = False

                # Add Displacement options
                for x in ['DISPLACEMENT', 'HEIGHT']:
                    if x in textureUpper and self.DisplacementDone == 0 and DisplacementCheck is True:
                        self.out = 'displacement'
                        self.map = 'displacementShader'

                        self.DisplacementDone = 1

                # Connect
                self.createNodeFile(texture)

    def createNodeFile(self, texture):
        """
            Create the nodes and link them to the shader

        """
        if self.map == 'skip':
            return

        # CREATE
        nodeFile = cmds.shadingNode("file", asTexture=True, name="file_{}_{}".format(self.shd_name, self.map))
        cmds.setAttr("{}.uvTilingMode".format(nodeFile), 3)
        if self.out == 'outAlpha':
            cmds.setAttr("{}.alphaIsLuminance".format(nodeFile), 1)

        path = self.path.text()
        path_Text = (path + '\\' + texture)
        cmds.setAttr("{}.fileTextureName".format(nodeFile), path_Text, type='string')

        # CONNECT
        if self.map == 'normalCamera':
            # ADD AInormal
            ainormal = cmds.shadingNode("aiNormalMap", asTexture=True, name="aiNormalMap_{}".format(self.shd_name))
            cmds.connectAttr('{}.outColor'.format(nodeFile), '{}.input'.format(ainormal))
            cmds.connectAttr('{}.outValue'.format(ainormal), '{}.{}'.format(self.shd_name, self.map))
        elif self.map == 'displacementShader':
            # ADD Displacement Shader
            displace = cmds.shadingNode("displacementShader", asShader=True, name="displacementShader_{}".format(self.shd_name))
            cmds.connectAttr('{}.outColorR'.format(nodeFile), '{}.displacement'.format(displace))
            cmds.connectAttr('{}.displacement'.format(displace), '{}.{}'.format(self.sg_name, self.map))
        else:
            cmds.connectAttr('{}.{}'.format(nodeFile, self.out), '{}.{}'.format(self.shd_name, self.map))


    def list(self, shd):
        x = cmds.listConnections(shd, d=False, s=True)
        if x == None:
            x = []
        return (x)

