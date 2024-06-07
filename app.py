import sys
import json
import webbrowser
from PyQt6.QtCore import QDateTime, Qt
from PyQt6.QtWidgets import (QApplication, QDialog, QGroupBox, QHBoxLayout,
                             QLineEdit, QVBoxLayout, QPushButton, QRadioButton, QComboBox, QDateTimeEdit,
                             QTableWidget, QTabWidget, QTextEdit, QSizePolicy, QTableWidgetItem, QWidget, QStyleFactory)
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import weatherComponents
from openAIComponents import tripProposition

# Parametry aplikacji
version = 0.6  # App version
app_name = 'AI Trekking Advisor'  # App name
app_width = 1100  # App window width
app_height = 600  # App window height


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super(WidgetGallery, self).__init__(parent)
        self.trip_props_dict = {}  # Dictionary with trip propositions

        self.originalPalette = QApplication.palette()
        self.setMinimumHeight(app_height)
        self.setMaximumWidth(app_width)
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createbottomTabWidget()

        topLayout = QHBoxLayout()
        topLayout.heightForWidth(1)
        bottomLayout = QHBoxLayout()

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(topLayout, 1)
        topLayout.addWidget(self.topLeftGroupBox, 1)
        topLayout.addWidget(self.topRightGroupBox, 1)

        mainLayout.addLayout(bottomLayout, 1)
        bottomLayout.addWidget(self.bottomTabWidget, 0)
        self.setLayout(mainLayout)

        self.setWindowTitle(f"{app_name} v. {str(version)}")
        self.changeStyle('Fusion')
        self.location_from = None
        self.location_to = None

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
        dateTimeEdit.setObjectName("timeObject")

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

    def openWebsite(self):
        if self.location_from and self.location_to:
            webbrowser.open(f'www.google.pl/maps/dir/{self.location_from}/{self.location_to}')
        else:
            webbrowser.open('http://www.google.pl')

    def createbottomTabWidget(self):
        self.bottomTabWidget = QTabWidget()
        self.bottomTabWidget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Ignored)
        self.bottomTabWidget.setMinimumWidth(app_width - 500)

        # Tab 1 - Table with places
        tab1 = QWidget()
        tableWidget = QTableWidget(3, 3)
        tableWidget.setHorizontalHeaderLabels(["Miejsce", "Odległość w km", "Poziom trudności"])
        tableWidget.itemClicked.connect(self.tableItemClicked)
        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5, 5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        # Tab 2 - Description of the trip
        tab2 = QWidget()
        Tab2textEdit = QTextEdit()
        Tab2textEdit.setPlainText(
            "Propozycja trekkingu, wspinaczki lub innej aktywności w zależności od warunków atmosferycznych i lokalizacji.")
        Tab2textEdit.setReadOnly(True)
        Tab2textEdit.setObjectName("Tab2textEdit")
        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(Tab2textEdit)
        tab2.setLayout(tab2hbox)

        # Tab 3 - Recommended equipment
        tab3 = QWidget()
        Tab3textEdit = QTextEdit()
        Tab3textEdit.setPlainText("Lista zalecanego sprzętu w zależności od aktywności i warunków atmosferycznych.")
        Tab3textEdit.setReadOnly(True)
        Tab3textEdit.setObjectName("Tab3textEdit")
        tab3hbox = QHBoxLayout()
        tab3hbox.setContentsMargins(5, 5, 5, 5)
        tab3hbox.addWidget(Tab3textEdit)
        tab3.setLayout(tab3hbox)

        # Tab 4 - Weather forecast
        tab4 = QWidget()
        Tab4textEdit = QTextEdit()
        Tab4textEdit.setPlainText("Pogoda.")
        Tab4textEdit.setReadOnly(True)
        Tab4textEdit.setObjectName("Tab4textEdit")
        self.weatherCanvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.openWebsiteButton = QPushButton('Localization', self)
        self.openWebsiteButton.clicked.connect(self.openWebsite)
        tab4hbox = QHBoxLayout()
        tab4hbox.setContentsMargins(5, 5, 5, 5)
        tab4hbox.addWidget(Tab4textEdit)
        tab4hbox.addWidget(self.weatherCanvas)
        tab4hbox.addWidget(self.openWebsiteButton)
        tab4.setLayout(tab4hbox)


        self.bottomTabWidget.addTab(tab1, "Lista miejsc")
        self.bottomTabWidget.addTab(tab2, "Opis propozycji wyjazdu")
        self.bottomTabWidget.addTab(tab3, "Lista zalecanego sprzętu")
        self.bottomTabWidget.addTab(tab4, "Prognoza pogody")

    def draw_plot(self, weather_data):

        hourly_temperatures = [hour['Temperature']['Value'] for hour in weather_data]
        hours_list = [hour['DateTime'] for hour in weather_data]
        hours_object = [datetime.fromisoformat(hour) for hour in hours_list]
        hours = [hour.strftime("%H:%M") for hour in hours_object]
        # draw plot
        self.weatherCanvas.axes.clear()
        self.weatherCanvas.axes.plot(hours, hourly_temperatures, marker='o', linestyle='-')
        self.weatherCanvas.axes.set_xlabel('Time (Hour)')
        self.weatherCanvas.axes.set_ylabel('Temperature (°C)')
        self.weatherCanvas.axes.set_title('Hourly Temperature Forecast')
        self.weatherCanvas.axes.tick_params(axis='x', rotation=45)
        self.weatherCanvas.axes.grid(True)
        self.weatherCanvas.figure.tight_layout()
        self.weatherCanvas.axes.set_title('Hourly Temperature Forecast')
        self.weatherCanvas.draw()

    def tableItemClicked(self, item):
        place = self.bottomTabWidget.findChild(QTextEdit, "Tab2textEdit")
        equipment = self.bottomTabWidget.findChild(QTextEdit, "Tab3textEdit")
        placefromdict = self.trip_props_dict['trip_propositions'][item.row()]['proposition_details']
        equipmentfromdoct = self.trip_props_dict['trip_propositions'][item.row()]['equipment']
        latitude = self.trip_props_dict['trip_propositions'][item.row()]['coordinates']['latitude']
        longitude = self.trip_props_dict['trip_propositions'][item.row()]['coordinates']['longitude']
        weather_data = weatherComponents.get_hourly_weather(latitude,longitude)
        self.location_to = self.trip_props_dict['trip_propositions'][item.row()]['place']

        place.setPlainText(placefromdict)
        equipment.setPlainText(equipmentfromdoct)
        self.draw_plot(weather_data)


    def findLocation(self):
        lineEdit = self.topRightGroupBox.findChild(QLineEdit)
        place = lineEdit.text()
        locationsWithId = weatherComponents.weatherLocations(place)  # Get locationID from Accuweather API

        locations = []
        for i in range(len(locationsWithId)):
            locations.append(locationsWithId[i][1])

        # Populate combobox
        styleComboBox = self.topRightGroupBox.findChild(QComboBox)
        styleComboBox.clear()  # Clear combobox
        styleComboBox.addItems(locations)

    def fillTableWidget(self, trip_proposition: dict):
        tableWidget = self.bottomTabWidget.findChild(QTableWidget)

        # get json attributes and set tableWidget items
        for prop in trip_proposition['trip_propositions']:
            tableWidget.setItem(prop['number'] - 1, 0, QTableWidgetItem(prop['place']))
            tableWidget.item(prop['number'] - 1, 0).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tableWidget.setItem(prop['number'] - 1, 1, QTableWidgetItem(str(prop['distance'])))
            tableWidget.item(prop['number'] - 1, 1).setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            tableWidget.setItem(prop['number'] - 1, 2, QTableWidgetItem(str(prop['hardenes_level'])))
            tableWidget.item(prop['number'] - 1, 2).setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        tableWidget.resizeColumnsToContents()

    def proposeTrip(self):
        # get activity from radio button
        if self.topLeftGroupBox.findChild(QRadioButton).isChecked():
            activity = 'Trekking'
        else:
            activity = 'Wspinaczka'

        # get location from combobox
        place = self.topRightGroupBox.findChild(QComboBox).currentText()
        self.location_from = place
        # time = self.topRightGroupBox.findChild(QDateTimeEdit, "timeObject")
        # self.time = time.dateTime()


        trip_proposition = tripProposition(place, activity)
        trip_proposition_dict = json.loads(trip_proposition)
        self.trip_props_dict = trip_proposition_dict
        self.fillTableWidget(trip_proposition_dict)


# Run app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec())
