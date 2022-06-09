import sys,os
import warnings
warnings.filterwarnings(action='ignore')
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow,QApplication,QSizePolicy
from retrieval import retrieval
from summarization import generate_summary
from ocr import ocr_read
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'     # tensorflow 오류 제거용



class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('./myqt01.ui', self)
        self.setWindowTitle('Tabloid Discriminator: News Retrieval Service')
        self.setAcceptDrops(True)
        self.output.setWordWrap(True)    
        self.output.setOpenExternalLinks(True)
        self.output.setTextFormat(1)
        self.ui.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            self.img_read(str(f))
    
    def img_read(self, imPath):
        text = ocr_read(imPath)
        self.input_text.setPlainText(text)
        self.output.setText(self.search(text))
        
    def button_clicked(self):
        text = self.input_text.toPlainText()
        self.set_textbox(text)
        
    def set_textbox(self, text):
        self.output.setText(self.search(text))
        
    def search(self, text):
        output = ''
        for newsFeed in retrieval(text,int(self.src_num.currentText())):
            output += '<br><br>'+generate_summary(newsFeed[1], int(self.sum_num.currentText()))+'<br>'+'<a href="'+newsFeed[0]+'">링크</a>'
        return output
    


if __name__ == '__main__':
    print('[Tabloid Discriminator] 접속을 시작합니다...')
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())