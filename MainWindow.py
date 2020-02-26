import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *   
from PyQt5.QtCore import *
from Canvas import *
import resources

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        QMainWindow.__init__(self)
        self.statusBar()
        self.setWindowTitle("Paint")
        
        self.canvas = Canvas(self)
        self.textEdit = QTextEdit(self)
        
        top_layout = QVBoxLayout()
        top_layout.addWidget(self.canvas)
        top_layout.addWidget(self.textEdit)
        #top_layout.addLayout( h_layout );
        
        container = QWidget()
        container.setLayout(top_layout)
        self.setCentralWidget(container)
        

        #self.setCentralWidget(self.canvas)
        self.resize(600, 500)

        bar = self.menuBar()
        fileMenu = bar.addMenu("File")

        fileToolBar = QToolBar("File")
        
        openFile = QAction(QIcon(":/icons/open.png"), "Open...", self)
        openFile.setShortcut(QKeySequence("Ctrl+O"))
        openFile.setToolTip("Open")
        openFile.setStatusTip("Open")
        fileMenu.addAction(openFile)
        fileToolBar.addAction(openFile)
        openFile.triggered.connect(self.open)
        
        saveFile = QAction(QIcon(":/icons/save.png"), "Save...", self)
        saveFile.setShortcut(QKeySequence("Ctrl+S"))
        saveFile.setToolTip("Save")
        saveFile.setStatusTip("Save")
        fileMenu.addAction(saveFile)
        fileToolBar.addAction(saveFile)
        saveFile.triggered.connect(self.save)
        
        quitFile = QAction(QIcon(":/icons/quit.png"), "Quit", self)
        quitFile.setShortcut(QKeySequence("Ctrl+W"))
        quitFile.setToolTip("Quit")
        quitFile.setStatusTip("Quit")
        fileMenu.addAction(quitFile)
        fileToolBar.addAction(quitFile)
        quitFile.triggered.connect(self.quit)
        
        self.addToolBar(fileToolBar)
        
        colorMenu = bar.addMenu("Color")
        actPen = fileMenu.addAction(QIcon(":/icons/pen.png"), "&Pen color", self.pen_color, QKeySequence("Ctrl+P"))
        actBrush = fileMenu.addAction(QIcon(":/icons/brush.png"), "&Brush color", self.brush_color, QKeySequence("Ctrl+B"))

        colorToolBar = QToolBar("Color")
        self.addToolBar( colorToolBar )
        colorToolBar.addAction( actPen )
        colorToolBar.addAction( actBrush )

        shapeMenu = bar.addMenu("Shape")
        actRectangle = fileMenu.addAction(QIcon(":/icons/rectangle.png"), "&Rectangle", self.rectangle )
        actEllipse = fileMenu.addAction(QIcon(":/icons/ellipse.png"), "&Ellipse", self.ellipse)
        actFree = fileMenu.addAction(QIcon(":/icons/free.png"), "&Free drawing", self.free_drawing)

        shapeToolBar = QToolBar("Shape")
        self.addToolBar( shapeToolBar )
        shapeToolBar.addAction( actRectangle )
        shapeToolBar.addAction( actEllipse )
        shapeToolBar.addAction( actFree )

        modeMenu = bar.addMenu("Mode")
        actMove = modeMenu.addAction(QIcon(":/icons/move.png"), "&Move", self.move)
        actDraw = modeMenu.addAction(QIcon(":/icons/draw.png"), "&Draw", self.draw)
        actSelect = modeMenu.addAction(QIcon(":/icons/select.png"), "&Select", self.select)

        modeToolBar = QToolBar("Navigation")
        self.addToolBar( modeToolBar )
        modeToolBar.addAction( actMove )
        modeToolBar.addAction( actDraw )
        modeToolBar.addAction( actSelect )

        '''
        copy = QAction(QIcon("copy.png"), "Copy", self)
        copy.setShortcut(QKeySequence("Ctrl+C"))
        copy.setToolTip("Copy")
        copy.setStatusTip("Copy")
        fileMenu.addAction(copy)
        fileToolBar.addAction(copy)
        copy.triggered.connect(self.copy)
        
        cut = QAction(QIcon("cut.png"), "Cut", self)
        cut.setShortcut(QKeySequence("Ctrl+X"))
        cut.setToolTip("Cut")
        cut.setStatusTip("Cut")
        fileMenu.addAction(cut)
        fileToolBar.addAction(cut)
        cut.triggered.connect(self.cut)

        paste = QAction(QIcon("paste.png"), "Paste", self)
        paste.setShortcut(QKeySequence("Ctrl+V"))
        paste.setToolTip("Paste")
        paste.setStatusTip("Paste")
        fileMenu.addAction(paste)
        fileToolBar.addAction(paste)
        paste.triggered.connect(self.paste)

        
        pipette = QAction(QIcon("lab.png"), "Color", self)
        pipette.setShortcut(QKeySequence("Ctrl+V"))
        pipette.setToolTip("Color")
        pipette.setStatusTip("Color")
        fileMenu.addAction(pipette)
        fileToolBar.addAction(pipette)
        pipette.triggered.connect(self.color)
        '''

    ##############
    def pen_color(self):
        self.log_action("choose pen color")
        self.canvas.set_color()

    def brush_color(self):
        self.log_action("choose brush color")
        self.canvas.set_bgcolor()

    def rectangle(self):
        self.log_action("Shape mode: rectangle")
        self.canvas.rectangle()

    def ellipse(self):
        self.log_action("Shape Mode: circle")
        self.canvas.ellipse()
        
    def free_drawing(self):
        self.log_action("Shape mode: free drawing")
        self.canvas.drawLasso()

    def move(self):
        self.log_action("Mode: move")
        self.canvas.move()

    def draw(self):
        self.log_action("Mode: draw")
        self.canvas.draw()
        
    def select(self):
        self.log_action("Mode: select")
        self.canvas.select()

    def log_action(self, str):
        content = self.textEdit.toPlainText()
        self.textEdit.setPlainText( content + "\n" + str)
        
    def open(self):
        print("Open...")
        openDialog = QFileDialog.getOpenFileName(self, "Open file", "", "*")
        try:
            fileName = openDialog[0].rsplit('/', 1)[-1]
            file = open(fileName, "r+")
            text = file.read()
            self.textEdit.setPlainText(text)
            openDialog.show()
            
        except:
            pass

    ###############
    def save(self):
        print("Save")
        saveDialog = QFileDialog.getSaveFileName(self, "Save file", "", "*")
        file = open(saveDialog[0],'w')
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()  
        saveDialog.show()
        
    def quit(self):
        print("Quit")
        self.close()
        
    def closeEvent(self, event):
        quitDialog = QMessageBox.question(self, 'Continue?',
                                          'Are you sure ?', QMessageBox.Yes, QMessageBox.No)
        if quitDialog == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def statusBar(self):
        self.statusBar = QStatusBar()
   
    def copy(self):
        print("copy")
        cb = QApplication.clipboard()
        cb.setText(self.textEdit.toPlainText())

    def cut(self):
        print("cut")
        cb = QApplication.clipboard()
        cb.setText(self.textEdit.toPlainText())
        self.textEdit.setPlainText("")

    def paste(self):
        print("paste")
        cb = QApplication.clipboard()
        self.textEdit.setPlainText(cb.text())

def main(args):
    app = QApplication(sys.argv)
    ui = MainWindow(args)
    ui.show()
    sys.exit(app.exec_()) # question 1
	

if __name__ == "__main__":
	main(sys.argv) 
