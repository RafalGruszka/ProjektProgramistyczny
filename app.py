# Aplikacja wspomagająca planowanie trekkingu lub wspinaczki górskiej

import weatherComponents
# Importowanie bibliotek PyQt6
from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

# Parametry aplikacji
version = 0.4                       # Wersja aplikacji
app_name = 'AI Trekking Advisor'    # Nazwa aplikacji
app_width = 600                     # Szerokość okna aplikacji
app_height = 400                    # Wysokość okna aplikacji


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        self.originalPalette = QApplication.palette()
        self.setFixedWidth(app_width)
        self.setFixedHeight(app_height)
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()

        topLayout = QHBoxLayout()
        topLayout.addStretch(1)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle(f"{app_name} v. {str(version)}")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        QApplication.setPalette(QApplication.style().standardPalette())



    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Aktywność:")
        self.topLeftGroupBox.setFixedWidth(120)
        radioButton1 = QRadioButton("Trekking")
        radioButton2 = QRadioButton("Wspinaczka")
        radioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Podaj lokalizację i datę wyjazdu:")

        lineEdit = QLineEdit('')
        lineEdit.setPlaceholderText('Lokalizacja')

        dateTimeEdit = QDateTimeEdit(self.topRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        findLocPushButton = QPushButton("Wyszukaj lokalizację")
        findLocPushButton.setDefault(True)
        findLocPushButton.clicked.connect(self.findLocation)

        proposeTripPushButton = QPushButton("Proponuj aktywność")
        proposeTripPushButton.setDisabled(True)
        proposeTripPushButton.clicked.connect(self.proposeTrip)

        styleComboBox = QComboBox()

        layout = QVBoxLayout()
        layout.addWidget(lineEdit, 0)
        layout.addWidget(dateTimeEdit, 2)
        layout.addWidget(findLocPushButton)
        layout.addWidget(proposeTripPushButton)
        layout.addStretch(1)
        layout.addWidget(styleComboBox)
        self.topRightGroupBox.setLayout(layout)


    def createBottomLeftTabWidget(self):
        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Ignored)
        self.bottomLeftTabWidget.setFixedWidth(app_width-300)
        tab1 = QWidget()
        tableWidget = QTableWidget(10, 1)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                              "How I wonder what you are.\n" 
                              "Up above the world so high,\n"
                              "Like a diamond in the sky.\n"
                              "Twinkle, twinkle, little star,\n" 
                              "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, "&Table")
        self.bottomLeftTabWidget.addTab(tab2, "Text &Edit")

    def findLocation(self):
        lineEdit = self.topRightGroupBox.findChild(QLineEdit)
        place = lineEdit.text()
        locationsWithId = weatherComponents.weatherLocations(place) # Pobranie lokalizacji z API Accuweather

        #pobierz drugi element z listy
        locations = []
        for i in range(len(locationsWithId)):
            locations.append(locationsWithId[i][1])

        # Dodanie wyników lokalizacji do comboboxa
        styleComboBox = self.topRightGroupBox.findChild(QComboBox)
        styleComboBox.clear()  # Czyszczenie comboboxa
        styleComboBox.addItems(locations)

    def proposeTrip(self):
        trip = ''


# Uruchomienie aplikacji
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())