import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QGraphicsScene, QGraphicsView, 
    QGraphicsPixmapItem, QGraphicsEllipseItem, QPushButton, QVBoxLayout, QHBoxLayout, 
    QWidget, QInputDialog)
from PyQt5.QtGui import QPixmap, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPointF

class Access_Point(QGraphicsEllipseItem):
    """Custom QGraphicsEllipseItem to represent an access point"""

    def __init__(self, x, y, radius=8, color=Qt.red):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.black, 1))
        self.setZValue(1)

class SignalHeatZone(QGraphicsEllipseItem):
    """Custom QGraphicsEllipseItem to represent a signal heat zone"""

    def __init__(self, x, y, radius=400, signal_strength=-70):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2)
        self.setBrush(QBrush(self.get_color(signal_strength, 100)))  # 100 is alpha transparency
        self.setPen(QPen(Qt.black, 1, Qt.DotLine))
        self.setZValue(0)

    def get_color(self, signal_strength, alpha):
        """Determine color based on signal strength."""
        if signal_strength < -70:
            return QColor(255, 0, 0, alpha)  # Red (Weak Signal)
        elif -69 <= signal_strength <= -50:
            return QColor(255, 255, 0, alpha)  # Yellow (Moderate Signal)
        else:
            return QColor(0, 255, 0, alpha)  # Green (Strong Signal)

class SimulatorApp(QMainWindow):
    """GUI for the access point simulation app"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Access Point Simulator & Analysis")
        self.setGeometry(100, 100, 1000, 700)

        self.blueprint = None  # Store the blueprint pixmap
        self.adding_heat_zone = False  # Flag for adding signal heat zones
        self.adding_access_point = False #Flag for adding access points

        self.setupUI()
    
    def setupUI(self):
        """Setup UI components"""
        main_Widget = QWidget()
        layout = QVBoxLayout(main_Widget)
         
        sub_widget = QWidget()
        sub_layout = QHBoxLayout(sub_widget)

        #Button to add access point
        self.addAccessPointBtn = QPushButton("Add Access Point")
        self.addAccessPointBtn.clicked.connect(self.toggleAccessPoint)
        sub_layout.addWidget(self.addAccessPointBtn)

        # Button to add signal heat zones
        self.addSignalHeatZoneBtn = QPushButton("Add Signal Heat Zone")
        self.addSignalHeatZoneBtn.clicked.connect(self.toggleSignalHeatZone)
        sub_layout.addWidget(self.addSignalHeatZoneBtn)

        layout.addWidget(sub_widget)

        # QGraphics scene and view
        self.scene = QGraphicsScene()
        self.view = QGraphicsView()
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)  # Enable panning
        
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

            self.view.setScene(self.scene)
            self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

            self.access_points = []
            self.signal_zones = []
    
    def toggleAccessPoint(self):
        """Enable or disable adding access points."""
        self.adding_access_point = not self.adding_access_point
        if self.adding_access_point:
            if self.adding_heat_zone:
                self.adding_heat_zone = not self.adding_heat_zone
            self.addAccessPointBtn.setText("Click on Blueprint to Add AP")
        else:
            self.addAccessPointBtn.setText("Add Access Point")

    
    def toggleSignalHeatZone(self):
        """Enable or disable adding signal heat zones."""
        self.adding_heat_zone = not self.adding_heat_zone
        if self.adding_heat_zone:
            if self.adding_access_point:
                self.adding_access_point = not self.adding_access_point
            self.addSignalHeatZoneBtn.setText("Click on Blueprint to Add Heat Zone")
        else:
            self.addSignalHeatZoneBtn.setText("Add Signal Heat Zone")

    def mousePressEvent(self, event):
        """Handle mouse clicks to add signal heat zones and access points accurately, considering zoom."""

        # Convert global position to scene coordinates to fix offset
        scenePos = self.view.mapToScene(self.view.mapFromGlobal(event.globalPos()))

        if self.adding_heat_zone and self.blueprint:
            # Ensure click is within blueprint boundaries
            if not self.scene.itemsBoundingRect().contains(scenePos):
                print("Click was outside the blueprint, no heat zone added.")
                return

            # Prompt user for signal strength
            signal_strength, ok = QInputDialog.getInt(self, "Signal Strength", "Enter signal strength (dBm):", -60, -100, 0)
            if not ok:
                return

            # Add signal heat zone
            heat_zone = SignalHeatZone(scenePos.x(), scenePos.y(), 50, signal_strength)
            self.scene.addItem(heat_zone)
            self.signal_zones.append(heat_zone)
            print(f"Signal Heat Zone Added at: {scenePos.x()}, {scenePos.y()} with {signal_strength} dBm")

        
        elif self.adding_access_point and self.blueprint:
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
    viewer = SimulatorApp()
    viewer.show()
    sys.exit(app.exec_())