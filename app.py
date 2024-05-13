# Aplikacja wspomagająca planowanie trekkingu lub wspinaczki górskiej
# Autorzy: Rafał Gruszka, Dawid Furs
import json

# Importowanie bibliotek PyQt6
from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
                             QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
                             QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
                             QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
                             QVBoxLayout, QWidget, QTableWidgetItem)
import weatherComponents
from openAIComponents import tripProposition

# Parametry aplikacji
version = 0.6                       # App version
app_name = 'AI Trekking Advisor'    # App name
app_width = 1100                    # App window width
app_height = 600                    # App window height


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)

        trip_props_dict = {}  # Dictionary with trip propositions

        self.originalPalette = QApplication.palette()
        self.setMinimumHeight(app_height)
        self.setMaximumWidth(app_width)
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createbottomTabWidget()

        topLayout = QHBoxLayout()
        topLayout.heightForWidth(1)
        #topLayout.addStretch(1)

        bottomLayout = QHBoxLayout()
        #bottomLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout, 1)
        topLayout.addWidget(self.topLeftGroupBox, 1)
        topLayout.addWidget(self.topRightGroupBox, 1)

        mainLayout.addLayout(bottomLayout, 1)
        bottomLayout.addWidget(self.bottomTabWidget, 0)
        #mainLayout.setRowStretch(1, 1)
        #mainLayout.setRowStretch(2, 1)
        #mainLayout.setColumnStretch(0, 1)
        #mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle(f"{app_name} v. {str(version)}")
        self.changeStyle('Fusion')

    def changeStyle(self, styleName):
        QApplication.setStyle(QStyleFactory.create(styleName))
        QApplication.setPalette(QApplication.style().standardPalette())



    def createTopLeftGroupBox(self):
        self.topLeftGroupBox = QGroupBox("Aktywność")
        self.topLeftGroupBox.setFixedWidth(120)
        self.topLeftGroupBox.setMaximumHeight(200)
        radioButton1 = QRadioButton("Trekking")
        radioButton2 = QRadioButton("Wspinaczka")
        radioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("Podaj lokalizację i datę wyjazdu")
        self.topRightGroupBox.setMaximumHeight(200)
        lineEdit = QLineEdit('')
        lineEdit.setPlaceholderText('Lokalizacja')

        dateTimeEdit = QDateTimeEdit(self.topRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        findLocPushButton = QPushButton("Wyszukaj lokalizację")
        findLocPushButton.setDefault(True)
        findLocPushButton.clicked.connect(self.findLocation)

        proposeTripPushButton = QPushButton("Proponuj aktywność")
        proposeTripPushButton.setDisabled(False)
        proposeTripPushButton.clicked.connect(self.proposeTrip)
        styleComboBox = QComboBox()

        layout = QVBoxLayout()
        layout.addWidget(lineEdit, 0)
        layout.addWidget(dateTimeEdit, 2)
        layout.addWidget(findLocPushButton)
        layout.addWidget(proposeTripPushButton)
        layout.addWidget(styleComboBox)
        self.topRightGroupBox.setLayout(layout)


    def createbottomTabWidget(self):
        self.bottomTabWidget = QTabWidget()
        self.bottomTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred,
                QSizePolicy.Policy.Ignored)
        self.bottomTabWidget.setMinimumWidth(app_width-500)
        tab1 = QTabWidget()
        tableWidget = QTableWidget(3, 3)
        tableWidget.setHorizontalHeaderLabels(["Miejsce", "Odległość w km", "Poziom trudności"])
        tableWidget.itemClicked.connect(self.tableItemClicked)


        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QTabWidget() # Opis propozycji wyjazdu
        Tab2textEdit = QTextEdit()

        Tab2textEdit.setPlainText("Propozycja trekkingu, wspinaczki lub innej aktywności w zależności od warunków atmosferycznych i lokalizacji.")
        Tab2textEdit.setReadOnly(True)
        Tab2textEdit.setObjectName("Tab2textEdit")


        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(Tab2textEdit)
        tab2.setLayout(tab2hbox)

        tab3 = QTabWidget()
        Tab3textEdit = QTextEdit()

        Tab3textEdit.setPlainText("Lista zalecanego sprzętu w zależności od aktywności i warunków atmosferycznych.")
        Tab3textEdit.setReadOnly(True)
        Tab3textEdit.setObjectName("Tab3textEdit")

        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(Tab3textEdit)
        tab3.setLayout(tab3hbox)

        tab4 = QWidget()

        self.bottomTabWidget.addTab(tab1, "Lista &miejsc")
        self.bottomTabWidget.addTab(tab2, "&Opis propozycji wyjazdu")
        self.bottomTabWidget.addTab(tab3, "Lista zalecanego &sprzętu")
        self.bottomTabWidget.addTab(tab4, "Prognoza &pogody")

    def tableItemClicked(self, item):

        place = self.bottomTabWidget.findChild(QTextEdit, "Tab2textEdit")
        equipment = self.bottomTabWidget.findChild(QTextEdit, "Tab3textEdit")
        placefromdict = self.trip_props_dict['trip_propositions'][item.row()]['proposition_details']
        equipmentfromdoct = self.trip_props_dict['trip_propositions'][item.row()]['equipment']
        place.setPlainText(placefromdict)
        equipment.setPlainText(equipmentfromdoct)


    def findLocation(self):
        lineEdit = self.topRightGroupBox.findChild(QLineEdit)
        place = lineEdit.text()
        locationsWithId = weatherComponents.weatherLocations(place) # Get locationID from Accuweather API

        locations = []
        for i in range(len(locationsWithId)):
            locations.append(locationsWithId[i][1])

        # Populate combobox
        styleComboBox = self.topRightGroupBox.findChild(QComboBox)
        styleComboBox.clear()  # Clear combobox
        styleComboBox.addItems(locations)


    def fillTableWidget(self, trip_proposition:dict):
        tableWidget = self.bottomTabWidget.findChild(QTableWidget)

        # get json attributes and set tableWidget items
        for prop in trip_proposition['trip_propositions']:
            # print(prop)
            tableWidget.setItem(prop['number'] - 1, 0, QTableWidgetItem(prop['place']))
            tableWidget.item(prop['number'] - 1, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            tableWidget.setItem(prop['number'] - 1, 1, QTableWidgetItem(str(prop['distance'])))
            tableWidget.item(prop['number'] - 1, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            tableWidget.setItem(prop['number'] - 1, 2, QTableWidgetItem(str(prop['hardenes_level'])))
            tableWidget.item(prop['number'] - 1, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            #print(str(prop['coordinates']['latitude']))
            #print(str(prop['coordinates']['longitude']))

        tableWidget.resizeColumnsToContents()
        #tableWidget.resizeRowsToContents()

    def proposeTrip(self):

        # get activity from radio button
        if self.topLeftGroupBox.findChild(QRadioButton).isChecked():
            activity = 'Trekking'
        else:
            activity = 'Wspinaczka'

        # get location from lineEdit
        place = self.topRightGroupBox.findChild(QComboBox).currentText()

        trip_proposition = tripProposition(place, activity)
        trip_proposition_dict = json.loads(trip_proposition)
        self.trip_props_dict = trip_proposition_dict
        self.fillTableWidget(trip_proposition_dict)


# Run app
if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())