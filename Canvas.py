from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Canvas(QWidget):

    def __init__(self, chart):
        QWidget.__init__(self)
        self.chart = chart
        self.setMinimumSize(500, 500)
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
        self.listLasso = []
        self.lasso = None

        self.shapeColor = None
        self.shapeBgColor = None

        #pour le moveMode
        self.translateBegin = QPoint()
        self.translateEnd = QPoint()
        self.translatePoint = QPoint()

        self.skriboli = []  # tableau de QLineF indiquant la direction (après intersection exclue)
        #self.listLineLasso = []  # tableau de QlineF
        self.skriboliMode = False  # devient True si intersection détectée
        self.skriboliDirection = 'N' #nord/sud/est/ouest
        self.skriboliX = 0
        self.skriboliY = 0

        # self.focusC = None

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.translate(self.translatePoint)

        # affichage des éléments dessinés
        for i in range(len(self.components)):
            # par défaut
            pen = QPen(Qt.black)
            qp.setPen(pen)
            pen.setWidth(5)

            # changement de couleur du contour
            if self.components[i][2] != None:
                pen = QPen(self.components[i][2])
                qp.setPen(pen)

            # changement de couleur du fond
            if self.components[i][3] != None:
                br = QBrush(self.components[i][3])
                qp.setBrush(br)

            # affichage de la sélection
            if self.selectMode and i == self.selection:
                pen = QPen(Qt.red)
                pen.setWidth(5)
                qp.setPen(pen)

            # affichage de la sélection lasso
            if self.lassoMode and self.selectionLasso:
                for j in self.selectionLasso:
                    if i == j:
                        pen = QPen(Qt.red)
                        pen.setWidth(5)
                        qp.setPen(pen)

            if self.components[i][1] == "rectangle":
                qp.drawRect(self.components[i][0])
            elif self.components[i][1] == "ellipse":
                qp.drawEllipse(self.components[i][0])

        # lasso en cours
        if self.listLasso != [] and self.lasso == None:
            pen = QPen(Qt.red)
            pen.setWidth(5)
            qp.setPen(pen)
            for point in self.listLasso:
                qp.drawPoint(point)
                # skriboli menu
                if self.skriboliMode:
                    qp.setOpacity(1) if self.skriboliDirection == 'N' else qp.setOpacity(0.3)
                    qp.drawRect(self.skriboliX, self.skriboliY - 30, 3, 30)
                    qp.drawText(self.skriboliX - 16, self.skriboliY - 36, 'Clear')

                    qp.setOpacity(1) if self.skriboliDirection == 'S' else qp.setOpacity(0.3)
                    qp.drawRect(self.skriboliX, self.skriboliY, 3, 30)
                    qp.drawText(self.skriboliX - 20, self.skriboliY + 50, 'Color')

                    qp.setOpacity(1)
        '''
        #lasso fini
        if self.lasso != None:
            pen = QPen(Qt.red)
            pen.setWidth(5)
            #pen.setStyle(Qt.DashDotLine)
            qp.setPen(pen)
            qp.setBrush(QColor(0,0,0,0))
            qp.drawPolygon(self.lasso)
        '''

        if self.drawMode:

            # affichage de l'élément en cours de construction
            if self.current_component != None:
                if self.shapeColor != None:
                    pen = QPen(self.shapeColor)
                    qp.setPen(pen)

                # changement de couleur du fond
                if self.shapeBgColor != None:
                    br = QBrush(self.shapeBgColor)
                    qp.setBrush(br)

                # forme
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

        if self.lassoMode:
            #reset lasso
            self.lasso = None
            self.listLasso = []
            self.selectionLasso = []

            pt = event.pos()-self.translatePoint
            self.listLasso.append(pt)

            if self.skriboli:
                self.skriboliActions()
                self.skriboli = False

        if self.selectMode:
            # reset selection
            self.selection = None
            select = event.pos()-self.translatePoint
            for i in range(len(self.components)):
                if self.components[i][0].contains(select):
                    self.selection = i
                    break
        self.update()

    def mouseMoveEvent(self, event):
        if self.drawMode:
            self.end = event.pos()-self.translatePoint
            self.current_component = QRect(self.begin, self.end)

        if self.moveMode:
            self.translateEnd = event.pos()
            self.translatePoint = self.translatePoint + (self.translateEnd - self.translateBegin)
            self.translateBegin = event.pos()

        if self.lassoMode:
            pt = event.pos()-self.translatePoint

            #skriboli
            if not self.skriboli:
                for i in range(0, len(self.listLasso[:-3])-1, 2):
                    line = QLineF(self.listLasso[i], self.listLasso[i + 1])
                    res = QLineF(self.listLasso[-1], event.pos()).intersects(line)
                    # check if intersection
                    if res[0] == 1:
                        self.skriboliX = res[1].x()
                        self.skriboliY = res[1].y()
                        self.skriboliMode = True
            else:

                if QRegion(QRect(self.skriboliX - 30, self.skriboliY - 200, 60, 200), QRegion.Ellipse).contains(
                        QPoint(self.pEndX, self.pEndY)):
                    self.skriboliDirection = 'N'

                elif QRegion(QRect(self.skriboliX - 30, self.skriboliY, 60, 200), QRegion.Ellipse).contains(
                        QPoint(self.pEndX, self.pEndY)):
                    self.skriboliDirection = 'S'

            self.listLasso.append(pt)

        self.update()

    def mouseReleaseEvent(self, event):
        if self.drawMode:
            self.current_component = QRect(self.begin, self.end)
            self.components.append([self.current_component, self.shape, self.shapeColor, self.shapeBgColor])
            self.update_charts()

        if self.moveMode:
            self.translateEnd = event.pos()
            self.translatePoint = self.translatePoint + (self.translateEnd - self.translateBegin)

        if self.lassoMode:
            self.lasso = QPolygon(self.listLasso)
            for i in range(len(self.components)):
                pt = self.components[i][0].center()
                if self.lasso.containsPoint(pt, 1):
                    self.selectionLasso.append(i)
            if self.skriboli:
                self.skriboliActions()
                self.skriboli = False

        self.update()

    def rectangle(self):
        self.moveMode = False

        if self.selection:
            self.drawShape = False
            self.drawMode = False
            self.components[self.selection][1] = "rectangle"

        elif self.selectionLasso != []:
            for c in self.selectionLasso:
                self.components[c][1] = "rectangle"
        else:
            self.drawMode = True
            self.drawShape = True
            self.shape = "rectangle"
        self.update_charts()
        self.update()

    def ellipse(self):
        self.moveMode = False

        if self.selection:
            self.drawShape = False
            self.drawMode = False
            self.components[self.selection][1] = "ellipse"
        elif self.selectionLasso != []:
            for c in self.selectionLasso:
                self.components[c][1] = "ellipse"
        else:
            self.drawMode = True
            self.drawShape = True
            self.shape = "ellipse"
        self.update_charts()
        self.update()

    #pen
    def set_color(self):
        self.drawShape = False
        color = QColorDialog.getColor()
        if self.selection:
            self.components[self.selection][2] = color
        elif self.selectionLasso != []:
            for i in range(len(self.selectionLasso)):
                self.components[i][2] = color
        else:
            self.shapeColor = color

        self.update()

    #brush
    def set_bgcolor(self):
        self.drawShape = False
        color = QColorDialog.getColor()
        if self.selection:
            self.components[self.selection][3] = color
        elif self.selectionLasso != []:
            for i in range(len(self.selectionLasso)):
                self.components[i][3] = color
        else:
            self.shapeBgColor = color
        self.update()

    def draw(self):
        self.moveMode = False
        self.selectMode = False
        self.lassoMode = False
        self.drawMode = True

    def move(self):
        self.drawShape = False
        self.drawMode = False
        self.selectMode = False
        self.lassoMode = False
        self.moveMode = True

    def select(self):
        self.moveMode = False
        self.drawMode = False
        self.drawShape = False
        self.selectMode = True

    def drawLasso(self):
        self.moveMode = False
        self.drawMode = False
        self.selectMode = True
        self.lassoMode = True

    def update_charts(self):
        rectangles = 0
        ellipses = 0
        for c in self.components:
            if c[1] == "rectangle":
                rectangles += 1
            elif c[1] == "ellipse":
                ellipses += 1
        self.chart.update_chart(rectangles, ellipses)
        self.chart.update()

    def skriboliActions(self):
        if self.skriboliDirection == 'N':
            print("N")
            self.components = []
        elif self.skriboliDirection == 'S':
            print("s")
