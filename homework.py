class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f"Тип тренировки: {self.training_type}; "
                   f"Длительность: {self.duration:.3f} ч.; "
                   f"Дистанция: {self.distance:.3f} км; "
                   f"Ср. скорость: {self.speed:.3f} км/ч; "
                   f"Потрачено ккал: {self.calories:.3f}.")

class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    LEN_STEP = 0.65 # один шаг в метрах
    M_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        return self.action * Training.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration, self.get_distance(), self.get_mean_speed(), self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self, action, duration, weight):
        Training.__init__(self, action, duration, weight) # вызов родительского конструктора

    def get_spent_calories(self):
        return (Running.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed() + Running.CALORIES_MEAN_SPEED_SHIFT) * self.weight / Training.M_IN_KM * (self.duration * 60)

class SportsWalking(Training):

    CALORIES_WEIGHT_MLP_1 = 0.035
    CALORIES_WEIGHT_MLP_2 = 0.029
    MS_IN_KMH = 0.278 # константа для перевода значений из км/ч в м/с
    CM_IN_M = 100

    def __init__(self, action, duration, weight, height):
        Training.__init__(self, action, duration, weight) # вызов родительского конструктора
        self.height = height # новый параметр - рост

    def get_spent_calories(self):
        # нужны скорость в м/с и время в минутах
        mins = self.duration * Training.M_IN_H
        return ((SportsWalking.CALORIES_WEIGHT_MLP_1 * self.weight + (((self.get_mean_speed() * SportsWalking.MS_IN_KMH) ** 2) / (self.height / SportsWalking.CM_IN_M)) * SportsWalking.CALORIES_WEIGHT_MLP_2 * self.weight) * mins)

class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # один гребок в метрах
    CALORIES_MEAN_SPEED_ADD = 1.1
    CALORIES_COEFF = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        Training.__init__(self, action, duration, weight) # вызов родительского конструктора
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self) -> float:
        return self.action * Swimming.LEN_STEP / Training.M_IN_KM

    def get_mean_speed(self) -> float:
        return self.length_pool * self.count_pool / Training.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return (self.get_mean_speed() + Swimming.CALORIES_MEAN_SPEED_ADD) * Swimming.CALORIES_COEFF * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    # словарь с кодами для типов занятий
    codes = {'SWM' : Swimming,
             'WLK' : SportsWalking,
             'RUN' : Running}
    return codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info() # информационное сообщение
    print(info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
