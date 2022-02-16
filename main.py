all_values = {  # Все значения коэффициентов
    "resistor": {
        "lambda_base": 0.00046428,  # Интенсивность отказов, 1/год
        "temperature": {25: 1, 30: 1.05, 35: 1.09, 40: 1.15, 45: 1.21, 50: 1.28, 55: 1.36, 60: 1.46,
                        65: 1.57, 70: 1.71, 75: 1.87, 80: 2.06, 85: 2.31, 90: 2.60, 95: 2.98, 100: 3.45,
                        105: 4.06, 110: 4.86},  # Начиная с 25 градусов, шаг 5 градусов, до 110 градусов
        "electrical_load": {0.1: 0.35, 0.2: 0.40, 0.3: 0.45, 0.4: 0.51, 0.5: 0.58, 0.6: 0.65, 0.7: 0.72, 0.8: 0.81,
                            0.9: 0.9, 1: 1},  # Доля от максимальной нагрузки, от 0.1 до 1, шаг 0.1
        "nominal_resistance": {500: 1, 5000: 0.7, 50000: 0.7, 500000: 2, 5000000: 0.6},  # сопротивление в Омах

    }
}


class Criteria:  # Критерий зависимости срока службы от какого-либо фактора
    def __init__(self, name=None, values=None):
        self.name = name
        self.values = values  # Значения коэффициента при разных значениях критерия


class Component:  # Испытываемый компонент
    def __init__(self, name=None, lambda_base=None, criteria=None):
        self.name = name
        self.lambda_base = lambda_base  # Базовое значение интенсивности отказов
        self.criteria = criteria  # Критерии, по которым можно посчитать зависимость срока службы

    def dependence(self, name):
        print(self.lambda_base, self.criteria)
        cr = Criteria()
        for c in self.criteria:
            if c.name == name:
                cr = c
                break
        for i in cr.values.keys():
            cr.values[i] *= self.lambda_base  # Значения интенсивности отказов при различных значениях критерия
        return cr.values


r = all_values["resistor"]
cr1 = Criteria("temperature", r["temperature"])
cr2 = Criteria("electrical_load", r["electrical_load"])
cr3 = Criteria("nominal_resistance", r["nominal_resistance"])
res = Component("resistor", r["lambda_base"], [cr1, cr2, cr3])
print(res.dependence("electrical_load"))
