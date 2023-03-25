from PyQt5.QtCore import QEvent,QPoint
from PyQt5 import QtWidgets as qt
from PyQt5 import QtGui as gui
from PyQt5 import QtCore
from QRCODEGenUI import Ui_MainWindow as ui
import os
from threading import *

class Window(qt.QMainWindow):


    def __init__(self):
        super(Window, self).__init__()

        self.ui = ui()
        self.ui.setupUi(self) # Initalize UI

        self.ui.pushButton.clicked.connect(self.thread)
        
        
    def GenerateQRCode(self):
        
        font = gui.QFont()
        font.setPointSize(13)
        self.ui.label_5.setFont(font)
        self.ui.label_5.setText("Generating...")

        try:

            import qrcode,datetime
            from textwrap import wrap
            from qrcode.image.styledpil import StyledPilImage
            from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
            from qrcode.image.styles.colormasks import RadialGradiantColorMask
            
            def hex2dec(hexval):
                h = hexval[+1:]
                return (int(wrap(h,2)[0],base=16),int(wrap(h,2)[1],base=16),int(wrap(h,2)[2],base=16))
            
            def filenameGen():
                fnm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fnm = fnm.replace(':','-')
                fnm = 'QRCODEGen_'+fnm.replace(' ','_')+'.png'
                return fnm
            
            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)

            qr.add_data(self.ui.plainTextEdit.toPlainText())
            
            img_1 = qr.make_image(image_factory=StyledPilImage,
                    color_mask=RadialGradiantColorMask(back_color=hex2dec(self.ui.lineEdit.text()),
                    center_color=hex2dec(self.ui.lineEdit_2.text()),edge_color=hex2dec(self.ui.lineEdit_3.text())))
            img_2 = qr.make_image(image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                    color_mask=RadialGradiantColorMask(back_color=hex2dec(self.ui.lineEdit.text()),
                    center_color=hex2dec(self.ui.lineEdit_2.text()),edge_color=hex2dec(self.ui.lineEdit_3.text())))

            if self.ui.checkBox.isChecked() :
                type(img_2)
                filepath = os.popen('cd').read().replace('\n','')+'\\'
                filename = filepath+filenameGen()
                img_2.save(filenameGen())
                pixmap = gui.QPixmap(filename)
                self.ui.lblIMG.setPixmap(pixmap)

                font = gui.QFont()
                font.setPointSize(10)
                self.ui.label_5.setFont(font)
                self.ui.label_5.setText(f"Image saved :\n {filepath}")
            else:
                type(img_1)
                filepath = os.popen('cd').read().replace('\n','')+'\\'
                filename = filepath+filenameGen()
                img_1.save(filenameGen())
                pixmap = gui.QPixmap(filename)
                self.ui.lblIMG.setPixmap(pixmap)
                
                font = gui.QFont()
                font.setPointSize(10)
                self.ui.label_5.setFont(font)
                self.ui.label_5.setText(f"Image saved :\n {filepath}")
            
        except Exception as e:
            msg1 = qt.QMessageBox()
            msg1.setIcon(qt.QMessageBox.Warning)
            msg1.setText(str(e))
            msg1.setWindowTitle("Error")
            msg1.setStandardButtons(qt.QMessageBox.Ok)
            msg1.exec_()

    def thread(self):
        t1=Thread(target=self.GenerateQRCode)
        t1.start()


# Run Application
app = qt.QApplication([])
application = Window()
application.show()
app.exec()