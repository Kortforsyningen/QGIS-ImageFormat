# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ImF_dialog_base.ui'
#
# Created: Wed May 25 09:53:21 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ImageFormatDialogBase(object):
    def setupUi(self, ImageFormatDialogBase):
        ImageFormatDialogBase.setObjectName(_fromUtf8("ImageFormatDialogBase"))
        ImageFormatDialogBase.resize(412, 551)
        self.groupBox = QtGui.QGroupBox(ImageFormatDialogBase)
        self.groupBox.setGeometry(QtCore.QRect(10, 210, 371, 151))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 286, 111))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBoxRawtiff = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxRawtiff.setObjectName(_fromUtf8("checkBoxRawtiff"))
        self.verticalLayout.addWidget(self.checkBoxRawtiff)
        self.checkBoxTiffJpeg = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxTiffJpeg.setObjectName(_fromUtf8("checkBoxTiffJpeg"))
        self.verticalLayout.addWidget(self.checkBoxTiffJpeg)
        self.checkBoxJpeg = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxJpeg.setObjectName(_fromUtf8("checkBoxJpeg"))
        self.verticalLayout.addWidget(self.checkBoxJpeg)
        self.checkBoxJpeg2000 = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxJpeg2000.setObjectName(_fromUtf8("checkBoxJpeg2000"))
        self.verticalLayout.addWidget(self.checkBoxJpeg2000)
        self.checkBoxGDAL = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxGDAL.setObjectName(_fromUtf8("checkBoxGDAL"))
        self.verticalLayout.addWidget(self.checkBoxGDAL)
        self.groupBox_2 = QtGui.QGroupBox(ImageFormatDialogBase)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 110, 371, 81))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.outDir = QtGui.QLineEdit(self.groupBox_2)
        self.outDir.setGeometry(QtCore.QRect(22, 30, 291, 21))
        self.outDir.setObjectName(_fromUtf8("outDir"))
        self.pushButton_Output = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_Output.setGeometry(QtCore.QRect(320, 30, 31, 21))
        self.pushButton_Output.setObjectName(_fromUtf8("pushButton_Output"))
        self.groupBox_1 = QtGui.QGroupBox(ImageFormatDialogBase)
        self.groupBox_1.setGeometry(QtCore.QRect(20, 20, 371, 81))
        self.groupBox_1.setObjectName(_fromUtf8("groupBox_1"))
        self.inDir = QtGui.QLineEdit(self.groupBox_1)
        self.inDir.setGeometry(QtCore.QRect(20, 30, 291, 21))
        self.inDir.setObjectName(_fromUtf8("inDir"))
        self.pushButton_Input = QtGui.QPushButton(self.groupBox_1)
        self.pushButton_Input.setGeometry(QtCore.QRect(320, 30, 31, 21))
        self.pushButton_Input.setObjectName(_fromUtf8("pushButton_Input"))
        self.checkBoxFolder = QtGui.QCheckBox(self.groupBox_1)
        self.checkBoxFolder.setGeometry(QtCore.QRect(20, 60, 141, 17))
        self.checkBoxFolder.setObjectName(_fromUtf8("checkBoxFolder"))
        self.button_box_execute = QtGui.QDialogButtonBox(ImageFormatDialogBase)
        self.button_box_execute.setGeometry(QtCore.QRect(40, 500, 341, 32))
        self.button_box_execute.setOrientation(QtCore.Qt.Horizontal)
        self.button_box_execute.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.button_box_execute.setObjectName(_fromUtf8("button_box_execute"))
        self.groupBox_3 = QtGui.QGroupBox(ImageFormatDialogBase)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 380, 371, 81))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.radioButtonUTM32 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButtonUTM32.setGeometry(QtCore.QRect(30, 20, 131, 17))
        self.radioButtonUTM32.setObjectName(_fromUtf8("radioButtonUTM32"))
        self.radioButtonUTM33 = QtGui.QRadioButton(self.groupBox_3)
        self.radioButtonUTM33.setGeometry(QtCore.QRect(30, 50, 151, 17))
        self.radioButtonUTM33.setObjectName(_fromUtf8("radioButtonUTM33"))
        self.checkBox_openwin = QtGui.QCheckBox(ImageFormatDialogBase)
        self.checkBox_openwin.setGeometry(QtCore.QRect(20, 470, 191, 17))
        self.checkBox_openwin.setObjectName(_fromUtf8("checkBox_openwin"))

        self.retranslateUi(ImageFormatDialogBase)
        QtCore.QObject.connect(self.button_box_execute, QtCore.SIGNAL(_fromUtf8("accepted()")), ImageFormatDialogBase.accept)
        QtCore.QObject.connect(self.button_box_execute, QtCore.SIGNAL(_fromUtf8("rejected()")), ImageFormatDialogBase.reject)
        QtCore.QMetaObject.connectSlotsByName(ImageFormatDialogBase)

    def retranslateUi(self, ImageFormatDialogBase):
        ImageFormatDialogBase.setWindowTitle(_translate("ImageFormatDialogBase", "ImF", None))
        self.groupBox.setTitle(_translate("ImageFormatDialogBase", "Ortophoto format", None))
        self.checkBoxRawtiff.setText(_translate("ImageFormatDialogBase", "Raw tiff", None))
        self.checkBoxTiffJpeg.setText(_translate("ImageFormatDialogBase", "TiffJpeg with worldfile (tfw)", None))
        self.checkBoxJpeg.setText(_translate("ImageFormatDialogBase", "Jpeg with worldfile (wld) and XML", None))
        self.checkBoxJpeg2000.setText(_translate("ImageFormatDialogBase", "Jpeg2000 with XML", None))
        self.checkBoxGDAL.setText(_translate("ImageFormatDialogBase", "GeoTiff with GDAL library file (vrt) (made from ovr-file)", None))
        self.groupBox_2.setTitle(_translate("ImageFormatDialogBase", "Save ortophotos to:", None))
        self.pushButton_Output.setText(_translate("ImageFormatDialogBase", "...", None))
        self.groupBox_1.setTitle(_translate("ImageFormatDialogBase", "Read raw photos from:", None))
        self.inDir.setToolTip(_translate("ImageFormatDialogBase", "<html><head/><body><p><br/></p></body></html>", None))
        self.inDir.setWhatsThis(_translate("ImageFormatDialogBase", "<html><head/><body><p>Select a single file. All files in dir will be used.</p></body></html>", None))
        self.pushButton_Input.setText(_translate("ImageFormatDialogBase", "...", None))
        self.checkBoxFolder.setText(_translate("ImageFormatDialogBase", "Choose folder of images", None))
        self.groupBox_3.setTitle(_translate("ImageFormatDialogBase", "Coordinate system", None))
        self.radioButtonUTM32.setText(_translate("ImageFormatDialogBase", "UTM32  EPSG: 25832", None))
        self.radioButtonUTM33.setText(_translate("ImageFormatDialogBase", "UTM33  EPSG: 25833", None))
        self.checkBox_openwin.setText(_translate("ImageFormatDialogBase", "Open image location in new window", None))

