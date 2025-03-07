import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QGraphicsScene, QGraphicsView, 
    QGraphicsPixmapItem, QGraphicsEllipseItem, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtGui import QPixmap, QBrush, QPen
from PyQt5.QtCore import Qt, QPointF

class Access_Point(QGraphicsEllipseItem):
    """Custom QGraphicsEllipseItem to represent an access point"""

    def __init__(self, x, y, radius=8, color=Qt.red):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.black, 1))

class Simulator_App(QMainWindow):
    """This will be the gui for the access point simulation app"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access Point Simulator & Analysis")
        self.setGeometry(100, 100, 1000, 700)

        self.blueprint = None  # Store the blueprint pixmap
        self.adding_access_point = False  # Flag for adding mode
        self.access_points = []  # Store access points

        self.setupUI()
    
    def setupUI(self):
        """Setup UI components"""
        main_Widget = QWidget()
        layout = QVBoxLayout(main_Widget)
         
        #Button to add access points 
        self.addAccessPointBtn = QPushButton("Add Access Point")
        self.addAccessPointBtn.clicked.connect(self.toggleAccessPoint)
        layout.addWidget(self.addAccessPointBtn)

        #QGraphics scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        #self.view.setRenderingHints(Qt.antialiasing) Only at the paint()

        #Enable zooming and panning
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        
        layout.addWidget(self.view)
        self.setCentralWidget(main_Widget)

         # Create menu actions
        self.createActions()
        self.createMenus()

    def createActions(self):
         """Create menu actions."""
         self.openAct = QAction("&Load Blueprint...", self, shortcut="Ctrl+O", triggered=self.loadBlueprint)
         self.exitAct = QAction("&Exit", self, shortcut="Ctrl+Q", triggered=self.close)

    def createMenus(self):
        """Create menu bar."""
        fileMenu = self.menuBar().addMenu("&File")
        fileMenu.addAction(self.openAct)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

    def loadBlueprint(self):
        """Load a building blueprint (image)."""
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Blueprint", "",
                            "Images (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            if pixmap.isNull():
                print("Failed to load blueprint!")
                return
            
            self.scene.clear()
            self.blueprint = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.blueprint)
            self.scene.setSceneRect(self.blueprint.boundingRect())  # Fit scene to image

            # Reset zoom and panning
            self.view.setScene(self.scene)
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

            self.access_points = []  # Reset access points
    
    def toggleAccessPoint(self):
        """Enable or disable adding access points."""
        self.adding_access_point = not self.adding_access_point
        if self.adding_access_point:
            self.addAccessPointBtn.setText("Click on Blueprint to Add AP")
        else:
            self.addAccessPointBtn.setText("Add Access Point")

    def mousePressEvent(self, event):
        """Handle mouse clicks to add access points accurately, considering zoom."""
        if self.adding_access_point and self.blueprint:
            # Convert global position to scene coordinates to fix offset
            scenePos = self.view.mapToScene(self.view.mapFromGlobal(event.globalPos()))

            # Ensure click is within blueprint boundaries
            if not self.scene.itemsBoundingRect().contains(scenePos):
                print("Click was outside the blueprint, no access point added.")
                return

            # Add access point at the correct location
            ap = Access_Point(scenePos.x(), scenePos.y())
            self.scene.addItem(ap)  
            self.access_points.append(ap)

            print(f"Access Point Added at: {scenePos.x()}, {scenePos.y()}")

    def wheelEvent(self, event):
        """Handle zooming with the mouse wheel."""
        factor = 1.2 if event.angleDelta().y() > 0 else 0.8
        self.view.scale(factor, factor)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = Simulator_App()
    viewer.show()
    sys.exit(app.exec_())
        
    

        