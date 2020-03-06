from PyQt5.QtChart import *


class Chart(QChart):

	def __init__(self, parent=None):
		QChart.__init__(self)
		self.view = None
		print("chart")

		set0 = QBarSet("Rectangle")
		set1 = QBarSet("Ellipses")

		set0 << 0 << 0
		set1 << 0 << 0

		series = QBarSeries()
		series.append(set0)
		series.append(set1)

		self.addSeries(series)

		self.createDefaultAxes()
		categories = ["Rectangles", "Ellipses"]
		axis = QBarCategoryAxis()
		axis.append(categories)
		axis.setTitleText("Number of shapes")
		self.setAxisX(axis, series)

		self.setAnimationOptions(QChart.SeriesAnimations)

	def update_chart(self, nb_rectangles, nb_ellipses):
		self.removeAllSeries()
		set0 = QBarSet("Rectangle")
		set1 = QBarSet("Ellipses")
		set0 << nb_rectangles << 0
		set1 << 0 << nb_ellipses
		series = QBarSeries()
		series.append(set0)
		series.append(set1)
		self.addSeries(series)

		self.createDefaultAxes()
		categories = ["Rectangles", "Ellipses"]
		axis = QBarCategoryAxis()
		axis.append(categories)
		axis.setTitleText("Number of shapes")
		self.setAxisX(axis, series)
		self.setAnimationOptions(QChart.SeriesAnimations)
		self.view.repaint()

	def set_view(self, view):
		self.view = view
