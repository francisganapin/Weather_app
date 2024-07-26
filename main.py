import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QApplication,QLineEdit
from PyQt6.QtCore import QTimer
from datetime import datetime

from PyQt6 import QtCore, QtWidgets
import requests

#######idea at NeuralNine





class MyApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        try:
            # Load the UI file
            uic.loadUi('main.ui', self)

            # Set fixed size based on loaded UI
            self.setFixedSize(self.size())


            # Initialize the emergency label
            self.emergency_label_text = "Ganapin || Emergency Calls  "
            self.emergency_label = QLabel(self.emergency_label_text, self)
            self.emergency_label.setGeometry(QtCore.QRect(10, 10, 91, 16))
            
            #if you want target the lael name it setobject then put stylesheet

            self.emergency_label.setObjectName("emergencyLabel")
            # Create a timer to update the text
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_text)
            self.timer.start(200)  # Update every 200 milliseconds
            ##date today and time

            # Get current date and time
            # Initialize the date label
            self.date_label = QLabel(self)
            self.date_label.setGeometry(QtCore.QRect(120, 10, 150, 16))  # Adjusted width for longer text
            self.date_label.setObjectName('dateLabel')

        # Set up the timer to update the time every second
            self.timer = QtCore.QTimer(self)
            self.timer.timeout.connect(self.update_time)
            self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

        # Initialize the time display
            self.update_time()

            # Apply stylesheet
            self.setStyleSheet("""
                #emergencyLabel {
                    color: black;
                }
                #dateLabel {
                    color: black;
                }
            """)
            self.search_bt.clicked.connect(self.get_city)
            self.input_city.setPlaceholderText("Enter Your City Name")
            self.input_api.setPlaceholderText("Enter Your Api Key")
            self.input_api.setEchoMode(QLineEdit.EchoMode.Password)

        except FileNotFoundError:
            print("UI file 'main2.ui' not found.")




    def update_text(self):
        # Shift the text
        self.emergency_label_text = self.emergency_label_text[1:] + self.emergency_label_text[0]
        self.emergency_label.setText(self.emergency_label_text)


    def update_time(self):
        # Get current date and time
        now = datetime.now()
        # Format the date and time as "day | month | day_number | year hour:minute am/pm"
        dt_string = now.strftime("%A | %B | %d | %y %I:%M %p")
        # Update the label text
        self.date_label.setText(dt_string)

    def get_weather_data(self):
        try:
            self.response = requests.get(self.url).json()
            if self.response.get('cod') != 200:
                self.Indvalid_label.setText(f"Error: {self.response.get('message', 'Failed to retrieve data')}")
                QTimer.singleShot(3000, lambda: self.Indvalid_label.setText(""))
                return

            self.temp_kelvin = self.response['main']['temp']
            self.temp_celsius, self.temp_fahrenheit = self.kelvin_to_celsius_fahrenheit(self.temp_kelvin)
            self.feels_like_kelvin = self.response['main']['feels_like']
            self.feels_like_celsius, self.feels_like_fahrenheit = self.kelvin_to_celsius_fahrenheit(self.feels_like_kelvin)
            self.humidity = self.response['main']['humidity']
            self.wind_speed = self.response['wind']['speed']
            self.description = self.response['weather'][0]['description']


            self.label_1_a.setText(f"{self.CITY}: {self.temp_celsius:.2f}°C / {self.temp_fahrenheit:.2f}°F")
            self.label_2_a.setText(f"Feels like: {self.feels_like_celsius:.2f}°C / {self.feels_like_fahrenheit:.2f}°F")
            self.label_3_a.setText(f"Humidity: {self.humidity}%")
            self.label_4_a.setText(f"Wind speed: {self.wind_speed} m/s")
            self.label_5_a.setText(f"Weather: {self.description}")
       

        except requests.RequestException as e:
            self.Indvalid_label.setText(f"Error retrieving weather data: {e}")
            QTimer.singleShot(3000, lambda: self.Indvalid_label.setText(""))

    def kelvin_to_celsius_fahrenheit(self, kelvin):
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9/5 + 32
        return celsius, fahrenheit
        
    def get_city(self):
        self.city = self.input_city.text()
        self.your_api_key = self.input_api.text()
        if self.city:
            self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
            self.API_KEY =  self.your_api_key
            self.CITY = self.city
            self.url = self.BASE_URL + 'appid=' + self.API_KEY + '&q=' + self.CITY

            self.get_weather_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MyApp()
    main_app.show()
    sys.exit(app.exec())



