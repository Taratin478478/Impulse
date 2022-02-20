from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QInputDialog, QListWidgetItem
from PyQt5.QtCore import QTimer, QUrl, Qt, QDateTime, QDate, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import uic
import sqlite3
import sys
from pprint import pprint


# name - название устройства
# lambda_base - базовое значение интенсивности отказов (доля от общего количества в год)
# time_base - базовое значение срока службы (лет)
# temperature - температура (°C)
# electrical_load - электрическая нагрузка (доля от макс)
# nominal_resistance - номинальное сопротивление (Ом)
# voltage_load - нагрузка по напряжению (Вольт)
# nominal_capacity - номинальная ёмкость (пикоФарад)

# Какие факторы описаны у устройств:
# Resistor (Резистор): temperature, electrical_load, nominal_resistance
# Transistor (Транзистор): temperature, electrical_load, voltage_load
# Capacitor (Конденсатор): temperature, electrical_load, nominal_capacity

# intensity - интенсивность отказов (доля от общего количества в год)
# time - Срок службы (лет)

class mech_test(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mсht2.ui", self)
        self.test_object.currentTextChanged.connect(self.change_names)
        self.show_graph.clicked.connect(self.former)
        self.mslv = {'Температура': 'temperature',
                     'Электрическая нагрузка': 'electrical_load',
                     'Нагрузка по напряжению': 'voltage_load',
                     'Номинальная ёмкость': 'nominal_capacity',
                     'Номинальное сопротивление': 'nominal_resistance',
                     'Резистор': 'resistor',
                     'Транзистор': 'transistor',
                     'Конденсатор': 'capacitor',
                     'Срок службы': 'time',
                     'Интенсивность отказов': 'intensity',
                     }
        self.plot([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [30, 32, 34, 32, 33, 31, 29, 32, 35, 45])
        self.con = sqlite3.connect('values.db')  # Подключение к БД
        self.db = self.con.cursor()

    def plot(self, hour, temperature):
        self.graphWidget.plot(hour, temperature)

    def change_names(self):
        self.object_params.clear()
        self.object_params.addItem('Температура')
        self.object_params.addItem('Электрическая нагрузка')
        if self.test_object.currentText() == 'Транзистор':
            self.object_params.addItem('Нагрузка по напряжению')
        elif self.test_object.currentText() == 'Конденсатор':
            self.object_params.addItem('Номинальная ёмкость')
        else:
            self.object_params.addItem('Номинальное сопротивление')

    def former(self):
        name = self.mslv[self.test_object.currentText()]
        factor = self.mslv[self.object_params.currentText()]
        mode = self.mslv[self.test_reasons.currentText()]
        pprint(self.create_data(name, factor, mode))

    def create_data(self, name, factor, mode):  # Получаем данные из БД
        base = 0
        try:
            if mode == "intensity":
                base = float(
                    self.db.execute("SELECT lambda_base FROM main WHERE name = '{}'".format(name)).fetchall()[0][0])
            elif mode == "time":
                base = float(
                    self.db.execute("SELECT time_base FROM main WHERE name = '{}'".format(name)).fetchall()[0][0])
            # Базовое значение интенсивности отказов или срока службы
            raw = self.db.execute("SELECT {} FROM main WHERE name = '{}'".format(factor, name)).fetchall()[0][0].split()
            # print(raw)
            # Данные по фактору
        except Exception as ex:  # Если произошла ошибка, например был неправильный запрос или несуществующий параметр
            print(ex)
            return 0
        data = [[], []]
        for r in raw:
            d = r.rstrip(",").split(":")
            if mode == "intensity":
                data[0].append(float(d[0]))
                data[1].append(float(d[1]) * base)
            elif mode == "time":
                data[0].append(float(d[0]))
                data[1].append(1 / float(d[1]) * base)
        return data


# print(create_data("capacitor", "nominal_capacity", "intensity"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mech_test()
    ex.show()
    sys.exit(app.exec())
