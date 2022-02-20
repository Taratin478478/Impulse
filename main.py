from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QMessageBox, QInputDialog, QListWidgetItem
from PyQt5.QtCore import QTimer, QUrl, Qt, QDateTime, QDate, QSize
from PyQt5.QtGui import QIcon, QPixmap
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



def create_data(name, factor, mode):  # Получаем данные из БД
    con = sqlite3.connect('values.db')  # Подключение к БД
    db = con.cursor()
    base = None
    try:
        if mode == "intensity":
            base = float(db.execute("SELECT lambda_base FROM main WHERE name = '{}'".format(name)).fetchall()[0][0])
        elif mode == "time":
            base = float(db.execute("SELECT time_base FROM main WHERE name = '{}'".format(name)).fetchall()[0][0])
        # Базовое значение интенсивности отказов или срока службы
        raw = db.execute("SELECT {} FROM main WHERE name = '{}'".format(factor, name)).fetchall()[0][0].split()
        # Данные по фактору
    except Exception:  # Если произошла ошибка, например был неправильный запрос или несуществующий параметр
        return 0
    finally:  # Всегда отключаемся от БД
        con.close()
    data = dict()
    for r in raw:
        d = r.rstrip(",").split(":")
        if mode == "intensity":
            data[float(d[0])] = float(d[1]) * base
        elif mode == "time":
            data[float(d[0])] = 1 / float(d[1]) * base
    return data


print(create_data("capacitor", "nominal_capacity", "intensity"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = mech_test()
    ex.show()
    sys.exit(app.exec())
