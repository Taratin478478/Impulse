from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sqlite3
import sys
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
        self.mslv = {'Температура (°C)': 'temperature',
                     'Электрическая нагрузка (%)': 'electrical_load',
                     'Нагрузка по напряжению (Ом)': 'voltage_load',
                     'Номинальная ёмкость (пФ)': 'nominal_capacity',
                     'Номинальное сопротивление (Ом)': 'nominal_resistance',
                     'Резистор': 'resistor',
                     'Транзистор': 'transistor',
                     'Конденсатор': 'capacitor',
                     'Срок службы (лет)': 'time',
                     'Интенсивность отказов (%)': 'intensity',
                     }
        self.con = sqlite3.connect('values.db')  # Подключение к БД
        self.db = self.con.cursor()

    def plot(self, x, y):
        self.graphWidget.clear()
        self.graphWidget.plot(x, y)

    def change_names(self):
        self.object_params.clear()
        self.object_params.addItem('Температура (°C)')
        self.object_params.addItem('Электрическая нагрузка (%)')
        if self.test_object.currentText() == 'Транзистор':
            self.object_params.addItem('Нагрузка по напряжению (Ом)')
        elif self.test_object.currentText() == 'Конденсатор':
            self.object_params.addItem('Номинальная ёмкость (пФ)')
        else:
            self.object_params.addItem('Номинальное сопротивление (Ом)')

    def former(self):
        name = self.mslv[self.test_object.currentText()]
        factor = self.mslv[self.object_params.currentText()]
        mode = self.mslv[self.test_reasons.currentText()]
        self.plot(self.create_data(name, factor, mode)[0], self.create_data(name, factor, mode)[1])

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mech_test()
    ex.show()
    sys.exit(app.exec())
