from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget):

    def __init__(self, parent = None):
        QWidget.__init__(self)
        self.setMinimumSize(200, 200)
        self.begin = QPoint()
        self.end = QPoint()
        self.components = []
        self.current_component = None
        self.shape = ""
        self.drawShape = False
        self.drawMode = True
        self.moveMode = False
        self.lassoMode = False
        self.selectMode = False
        self.selection = None
        self.selectionLasso = [] # list of components selected
        self.current_selection = None # QPolygon
        self.beginLasso = QPoint()
        self.endLasso = QPoint()
        
        self.shapeColor = None
        self.shapeBgColor = None
        
        self.translateBegin = QPoint()
        self.translateEnd = QPoint()
        self.translatePoint = QPoint()
  
        
    def paintEvent(self, event): # c fait que pour afficher
        qp = QPainter(self)
        qp.translate(self.translatePoint)
        
        #affichage des éléments dessinés
        for i in range(len(self.components)):
            #par défaut
            pen = QPen(Qt.black)
            qp.setPen(pen)
            pen.setWidth(5)
            
            #changement de couleur du contour
            if self.components[i][2] != None:
                pen = QPen(self.components[i][2])
                qp.setPen(pen)
                
            #changement de couleur du fond
            if self.components[i][3] != None:
                br = QBrush(self.components[i][3])  
                qp.setBrush(br) 
                
            #affichage de la sélection
            if self.selectMode and i == self.selection:
                pen = QPen(Qt.red)
                pen.setWidth(5)
                qp.setPen(pen)
                
            if self.components[i][1] == "rectangle":
                qp.drawRect(self.components[i][0])
            elif self.components[i][1] == "ellipse":
                qp.drawEllipse(self.components[i][0])
                
        
                
        if self.drawMode:
            
            #affichage de l'élément en cours de construction
            if self.current_component != None:
                if self.shapeColor != None:
                    pen = QPen(self.shapeColor)
                    qp.setPen(pen)
                
                #changement de couleur du fond
                if self.shapeBgColor != None:
                    br = QBrush(self.shapeBgColor)  
                    qp.setBrush(br) 
                
                #forme
                if self.shape == "rectangle":
                    qp.drawRect(self.current_component)
                elif self.shape == "ellipse":
                    qp.drawEllipse(self.current_component)
                    
            if self.current_selection != None:
                qp.drawConvexPolygon(self.current_selection)

        
    def mousePressEvent(self, event):
        if self.drawMode:
            self.current_component = QRect(self.begin, self.end)
            self.begin = event.pos()-self.translatePoint
            self.end = event.pos()-self.translatePoint
            
        if self.moveMode:
            self.translateBegin = event.pos()
            
        if self.selectMode:
            select = event.pos()-self.translatePoint
            for i in range(len(self.components)):
                if self.components[i][0].contains(select):
                   self.selection = i
                   break
               
        if self.selectionLasso:
            select = event.pos()-self.translatePoint
            for i in range(len(self.components)):
                if self.components[i][0].contains(select):
                   self.selectionLasso.append(i)
                   
        if self.lassoMode:
            self.beginLasso = event.pos()-self.translatePoint
            self.endLasso = event.pos()-self.translatePoint
            self.current_selection = QPolygon(QRect(self.beginLasso,self.endLasso))
        
        self.update()
        
    def mouseMoveEvent(self, event):
        if self.drawMode:
            self.end = event.pos()-self.translatePoint
            self.current_component = QRect(self.begin, self.end)
            
        if self.moveMode: #à tester
            self.translateEnd = event.pos()
            self.translatePoint = self.translatePoint + (self.translateEnd - self.translateBegin)
            self.translateBegin = event.pos()
                   
        if self.lassoMode:
            self.endLasso = event.pos()-self.translatePoint
            self.current_selection = QRect(self.beginLasso, self.endLasso)

        self.update()
            
    def mouseReleaseEvent(self, event):
        if self.drawMode:
            self.current_component = QRect(self.begin, self.end)
            self.components.append([self.current_component, self.shape, self.shapeColor, self.shapeBgColor])
            
        if self.moveMode: 
            self.translateEnd = event.pos()
            self.translatePoint = self.translatePoint + (self.translateEnd - self.translateBegin)
            
        self.update()

    def rectangle(self):
        self.moveMode = False
        
        if self.selection:
            self.drawShape = False
            self.drawMode = False
            self.components[self.selection][1] = "rectangle"
        else:
            self.drawMode = True
            self.drawShape = True
            self.shape = "rectangle"
        
    def ellipse(self):
        self.moveMode = False
        
        if self.selection:
            self.drawShape = False
            self.drawMode = False
            self.components[self.selection][1] = "ellipse"
        else:
            self.drawMode = True
            self.drawShape = True
            self.shape = "ellipse"

    #pen
    def set_color(self):
        self.drawShape = False
        color = QColorDialog.getColor()
        if self.selection:
            self.components[self.selection][2] = color
        elif self.selectionLasso:
            for i in range(len(self.selectionLasso)):
                self.components[i][2] = color
        else:
            self.shapeColor = color
    
    #brush    
    def set_bgcolor(self):
        self.drawShape = False
        color = QColorDialog.getColor()
        if self.selection:
            self.components[self.selection][3] = color
        elif self.selectionLasso:
            for i in range(len(self.selectionLasso)):
                self.components[i][3] = color
        else:
            self.shapeBgColor = color
    
    def draw(self):
        print("draw")
        self.moveMode = False
        self.selectMode = False
        self.drawMode = True
        
    def move(self):
        print("move")
        self.drawShape = False
        self.drawMode = False
        self.selectMode = False
        self.moveMode = True
        
    def select(self):
        self.moveMode = False
        self.drawMode = False
        self.selectMode = True
        
    def lasso(self):
        print("lasso")
        self.moveMode = False
        self.drawMode = False
        self.lassoMode = True