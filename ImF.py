# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImageFormat
                                 A QGIS plugin
 Image Formatter
                              -------------------
        begin                : 2016-05-10
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Mafal / sdfe
        email                : mafal@sdfe.dk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from ImF_dialog import ImageFormatDialog
import os
import subprocess
from os import listdir
from os.path import isfile, join


class ImageFormat:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ImageFormat_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = ImageFormatDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&ImF')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'ImageFormat')
        self.toolbar.setObjectName(u'ImageFormat')

        self.dlg.pushButton_Input.clicked.connect(self.showFileSelectDialogInput)
        self.dlg.pushButton_Output.clicked.connect(self.showFileSelectDialogOutput)
        # self.dlg.button_box_execute.connect(self.run)
        #self.dlg.inDir.setText('C:\Users\B020736\Documents\\tiff2jpg\\tiffs')
        #self.dlg.outDir.setText('C:\Users\B020736\Documents\\tiff2jpg\Images')
        self.dlg.radioButtonUTM32.setChecked(True)

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ImageFormat', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    #def showFileSelectDialogInput(self):
    #    fname = QFileDialog.getOpenFileName(self.dlg, 'Read File', self.dlg.inDir.text(),
    #                                        'TIF file (*.tif);;All files (*.*)')
    #    self.dlg.inDir.setText(fname)
    def showFileSelectDialogInput(self):
        if self.dlg.checkBoxFolder.isChecked():
            fname = QFileDialog.getExistingDirectory( None, 'Open Dir', str(self.dlg.inDir.text()))
            self.dlg.inDir.setText(fname)


        elif not self.dlg.checkBoxFolder.isChecked():
            fname = QFileDialog.getOpenFileName(self.dlg, 'Read File', self.dlg.inDir.text(),'TIF file (*.tif);;All files (*.*)')
            self.dlg.inDir.setText(fname)


    def showFileSelectDialogOutput(self):
        fname = QFileDialog.getExistingDirectory()
        self.dlg.outDir.setText(fname)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ImageFormat/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'ImF'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&ImF'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            outpath = str(self.dlg.outDir.text())
            tempoutpath = str.replace(outpath, "/", "\\")
            scriptoutpath = tempoutpath + "\\Images"
            if self.dlg.radioButtonUTM32.isChecked():
                EPSG = "25832"

            if self.dlg.radioButtonUTM33.isChecked():
                EPSG = "25833"

            if self.dlg.checkBoxFolder.isChecked():
                path = self.dlg.inDir.text()
                onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
                filenr = ""
                #for f in onlyfiles:
                #    filenr += 1
                #    tiffname = f
                #    truncname = os.path.splitext(tiffname)[0]
                if self.dlg.checkBoxTiffJpeg.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "TiffJpeg" + str(filenr) + ".bat", "a") as bat_file:
                        bat_file.write(
                            "REM @ECHO OFF\n" + "set GDAL_CACHEMAX=700\n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir TiffJpeg\n" + "SETLOCAL EnableDelayedExpansion\n\n" +
                            "SET inpath="+self.dlg.inDir.text()+"\\" + "\n" + "SET outpath=" + self.dlg.outDir.text() + "\TiffJpeg" + "\\" + "\n" +
                            "FOR /F %%i IN ('DIR /B %inpath%*.tif') DO (\n\n" + "    SET infile=%%i\n" + "    SET outfile=!infile:.tif=.tif!\n\n" +
                            "    \"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" +"\" " + "-b 1 -b 2 -b 3 -b 4 -of GTIFF -a_srs EPSG:" + EPSG +
                            " -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=RGB -co TILED=YES " + " %inpath%!infile! %outpath%!outfile!" + "\n)\n" + "DEL TiffJpeg"+ str(filenr) + ".bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run"+ str(filenr) + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"TiffJpeg"+str(filenr)+".bat\"" + "\n" + "DEL Run"+str(filenr)+".bat")

                    os.system(tempoutpath + "\Run"+str(filenr)+".bat")

                if self.dlg.checkBoxRawtiff.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Rawtiff" + str(filenr) + ".bat", "a") as bat_file:
                        bat_file.write(
                            "REM @ECHO OFF\n" + "set GDAL_CACHEMAX=700\n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir RawTiff\n" + "SETLOCAL EnableDelayedExpansion\n\n" +
                            "SET inpath=" + self.dlg.inDir.text() + "\\" + "\n" + "SET outpath=" + self.dlg.outDir.text() + "\RawTiff" + "\\" + "\n\n" +
                            "FOR /F %%i IN ('DIR /B %inpath%*.tif') DO (\n\n" + "    SET infile=%%i\n" + "    SET outfile=!infile:.tif=.tiff!\n\n" +
                            "    \"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -b 4 -a_srs EPSG:" + EPSG + 
							" -of GTIFF -scale -co TFW=YES -co TILED=YES -co PHOTOMETRIC=RGB -co BIGTIFF=IF_NEEDED -co COMPRESS=NONE -co ALPHA=UNSPECIFIED " +
							" %inpath%!infile! %outpath%!outfile!" + "\n)\n" + "DEL Rawtiff" + str(filenr) + ".bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run1" + str(filenr) + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Rawtiff" + str(filenr) + ".bat\"" + "\n" + "DEL Run1" + str(filenr) + ".bat")

                    os.system(tempoutpath + "\Run1" + str(filenr) + ".bat")

                if self.dlg.checkBoxJpeg.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Jpeg" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "REM @ECHO OFF\n" + "set GDAL_CACHEMAX=700\n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir Jpeg\n" + "SETLOCAL EnableDelayedExpansion\n\n" +
                            "SET inpath=" + self.dlg.inDir.text() + "\\" + "\n" + "SET outpath=" + self.dlg.outDir.text() + "\Jpeg" + "\\" + "\n\n" +
                            "FOR /F %%i IN ('DIR /B %inpath%*.tif') DO (\n\n" + "    SET infile=%%i\n" + "    SET outfile=!infile:.tif=.jpeg!\n\n" +
                            "    \"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + " -b 1 -b 2 -b 3 -a_srs EPSG:25832 -of JPEG -scale -co worldfile=yes " +
							" %inpath%!infile! %outpath%!outfile!" + "\n)\n" + "DEL Jpeg"+str(filenr)+".bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run2" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Jpeg"+str(filenr)+".bat\"" + "\n" + "DEL Run2"+str(filenr)+".bat")

                    os.system(tempoutpath + "\Run2"+str(filenr)+".bat")

                if self.dlg.checkBoxJpeg2000.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Jpeg2000" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "REM @ECHO OFF\n" + "set GDAL_CACHEMAX=700\n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir Jpeg2000\n" + "SETLOCAL EnableDelayedExpansion\n\n" +
                            "SET inpath=" + self.dlg.inDir.text() + "\\" + "\n" + "SET outpath=" + self.dlg.outDir.text() + "\Jpeg2000" + "\\" + "\n\n" +
                            "FOR /F %%i IN ('DIR /B %inpath%*.tif') DO (\n\n" + "    SET infile=%%i\n" + "    SET outfile=!infile:.tif=.jp2!\n\n" +
                            "    \"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -a_srs EPSG:25832 -of JP2OpenJPEG -scale " +
							" %inpath%!infile! %outpath%!outfile!" + "\n)\n" + "DEL Jpeg2000"+str(filenr)+".bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run3" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Jpeg2000"+str(filenr)+".bat\"" + "\n" + "DEL Run3"+str(filenr)+".bat")

                    os.system(tempoutpath + "\Run3"+str(filenr)+".bat")

                if self.dlg.checkBoxGDAL.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "GDAL_overlay" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "REM @ECHO OFF \n" + "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir TiffJpeg_ovr \n" + "SETLOCAL EnableDelayedExpansion\n\n" + 
							"SET inpath=" + self.dlg.inDir.text() + "\\" + "\n" + "SET outpath=" + self.dlg.outDir.text() + "\TiffJpeg_ovr" + "\\" + "\n\n" +
                            "FOR /F %%i IN ('DIR /B %inpath%*.tif') DO (\n\n" + "    SET infile=%%i\n" + "    SET outfile=!infile:.tif=.tif!\n" + "    SET vrtfile=!infile:.tif=.vrt!\n\n" +
							"\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -b 4 -of GTIFF -a_srs EPSG:25832 -co TFW=YES -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=RGB -co TILED=YES " + 
							" %inpath%!infile! %outpath%!outfile!\n\n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdalbuildvrt.exe" + "\" " + "%outpath%!vrtfile! %outpath%!infile!\n" + 
							"\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdaladdo.exe" + "\" " + "%outpath%!vrtfile! " + "-r average -ro --config GDAL_CACHEMAX 900 --config COMPRESS_OVERVIEW JPEG --config JPEG_QUALITY_OVERVIEW 85 --config PHOTOMETRIC_OVERVIEW RGB --config INTERLEAVE_OVERVIEW PIXEL --config BIGTIFF_OVERVIEW YES 2 4 10 25 50 100 200 500 1000" +
							"\n\n" + "DEL %outpath%!vrtfile!\n)\n" + "cd TiffJpeg_ovr\n" + "rename *.vrt.ovr *.\n" + "rename *.vrt *.tif.ovr\n" + " cd ..\n" + "DEL GDAL_overlay.bat") 

                    with open(self.dlg.outDir.text() + "\\" + "Run5" +str(filenr)+ ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"GDAL_overlay"+str(filenr)+".bat\"" + "\n" + "DEL Run5"+str(filenr)+".bat")

                    os.system(tempoutpath + "\Run5"+str(filenr)+".bat")

                    if self.dlg.checkBox_openwin.isChecked():
                        subprocess.call("explorer " + scriptoutpath, shell=True)

            if not self.dlg.checkBoxFolder.isChecked():
                outpath = str(self.dlg.outDir.text())
                tiffname = os.path.basename(os.path.normpath(self.dlg.inDir.text()))
                truncname = os.path.splitext(tiffname)[0]
                tempoutpath = str.replace(outpath, "/", "\\")
                scriptoutpath = tempoutpath + "\\Images"

                if self.dlg.checkBoxTiffJpeg.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "TiffJpeg" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir TiffJpeg \n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -b 4 -of GTIFF -a_srs EPSG:" + EPSG + " -co TFW=YES -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=RGB -co TILED=YES " + self.dlg.inDir.text() + " TiffJpeg/" + tiffname + "\n" + "DEL TiffJpeg.bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run1" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"TiffJpeg.bat\"" + "\n" + "DEL Run1.bat")

                    os.system(tempoutpath + "\Run1.bat")

                if self.dlg.checkBoxRawtiff.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Rawtiff" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir RawTiff \n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -b 4 -a_srs EPSG:" + EPSG + " -of GTIFF -scale -co TFW=YES -co TILED=YES -co PHOTOMETRIC=RGB -co BIGTIFF=IF_NEEDED -co COMPRESS=NONE -co ALPHA=UNSPECIFIED " + self.dlg.inDir.text() + " RawTiff/" + truncname + ".tiff" + "\n" + "DEL Rawtiff.bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run2" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Rawtiff.bat\"" + "\n" + "DEL Run2.bat")

                    os.system(tempoutpath + "\Run2.bat")

                if self.dlg.checkBoxJpeg.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Jpeg" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir Jpeg \n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + " -b 1 -b 2 -b 3 -a_srs EPSG:25832 -of JPEG -scale -co worldfile=yes " + self.dlg.inDir.text() + " Jpeg/" + truncname + ".jpg" + "\n" + "DEL Jpeg.bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run3" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Jpeg.bat\"" + "\n" + "DEL Run3.bat")

                    os.system(tempoutpath + "\Run3.bat")

                if self.dlg.checkBoxJpeg2000.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "Jpeg2000" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir Jpeg2000 \n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -a_srs EPSG:25832 -of JP2OpenJPEG -scale " + self.dlg.inDir.text() + " Jpeg2000/" + truncname + ".jp2" + "\n" + "DEL Jpeg2000.bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run4" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"Jpeg2000.bat\"" + "\n" + "DEL Run4.bat")

                    os.system(tempoutpath + "\Run4.bat")

                if self.dlg.checkBoxGDAL.isChecked():
                    with open(self.dlg.outDir.text() + "\\" + "GDAL_overlay" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "set GDAL_CACHEMAX=700 \n" + "cd " + self.dlg.outDir.text() + "\n" + "mkdir TiffJpeg_ovr \n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdal_translate.exe" + "\" " + "-b 1 -b 2 -b 3 -b 4 -of GTIFF -a_srs EPSG:25832 -co TFW=YES -co COMPRESS=JPEG -co JPEG_QUALITY=85 -co PHOTOMETRIC=RGB -co TILED=YES " + self.dlg.inDir.text() + " TiffJpeg_ovr/" + tiffname + "\n" +
                                "cd TiffJpeg_ovr" + "\n" + "\"" + os.path.dirname(os.path.realpath(sys.argv[0])) + "\gdalbuildvrt.exe" + "\" " + truncname + ".vrt " + truncname + ".tif " + "\n" + "\"" + os.path.dirname(
                                os.path.realpath(sys.argv[0])) + "\gdaladdo.exe" + "\" " + truncname + ".vrt " "-r average -ro --config GDAL_CACHEMAX 900 --config COMPRESS_OVERVIEW JPEG --config JPEG_QUALITY_OVERVIEW 85 --config PHOTOMETRIC_OVERVIEW RGB --config INTERLEAVE_OVERVIEW PIXEL --config BIGTIFF_OVERVIEW YES 2 4 10 25 50 100 200 500 1000" + "\n" +
                                "Del *.vrt" + "\n" + "rename " + truncname + ".vrt.ovr " + truncname + ".tif.ovr" + "\n" + "cd .." + "\n" + "DEL GDAL_overlay.bat")

                    with open(self.dlg.outDir.text() + "\\" + "Run5" + ".bat", "a") as bat_file:
                        bat_file.write(
                            "cd " + self.dlg.outDir.text() + "\n" + "wscript.exe \"" + os.path.dirname(__file__) + "\invisible.vbs\" \"GDAL_overlay.bat\"" + "\n" + "DEL Run5.bat")

                    os.system(tempoutpath + "\Run5.bat")


                if self.dlg.checkBox_openwin.isChecked():
                    subprocess.call("explorer " + scriptoutpath, shell=True)
                        # Do something useful here - delete the line containing pass and
                        # substitute with your code.
                    pass

                    pass
