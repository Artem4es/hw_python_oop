from typing import List, Tuple


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type: str = training_type
        self.duration: float = duration
        self.distance: float = distance
        self.speed: float = speed
        self.calories: float = calories

    def get_message(self) -> str:
        """Вернуть описание тренировки в виде строки данных"""
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {"%.3f" % self.duration} ч.;'
                f' Дистанция: {"%.3f" % self.distance} км;'
                f' Ср. скорость: {"%.3f" % self.speed} км/ч;'
                f' Потрачено ккал: {"%.3f" % self.calories}.')


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000       # конст для перевода зн из километров в метры
    LEN_STEP: float = 0.65    # длина шага в метрах

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM  # пр.дист

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        # ниже создание экземпляров класса InfoMessage
        return InfoMessage(self.__class__.__name__,   # назв. клас. чер. мет
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # coeff_calorie_1 = 18
        # coeff_calorie_2 = 20
        # часы в минуты = 60
        return ((18 * self.get_mean_speed() - 20) * self.weight / self.M_IN_KM
                * (self.duration * 60))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: int = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        # coeff_calorie_1 = 0.035
        # coeff_calorie_2 = 0.029
        # часы в минуты = 60
        return ((0.035 * self.weight + (self.get_mean_speed()**2
                // self.height) * 0.029 * self.weight) * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38   # длина гребка

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int):  # число проплытых бассейнов
        super().__init__(action, duration, weight)
        self.length_pool: int = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.get_mean_speed() + 1.1) * 2 * self.weight


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
        return Swimming(*data)  # созд. и возвр. объект класса Swimming
    if workout_type == 'RUN':
        return Running(*data)
    if workout_type == 'WLK':
        return SportsWalking(*data)
    return Training   # чтобы flake8 не ругался:)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()   # экз. кл. InfoMessage
    print(InfoMessage.get_message(info))


if __name__ == '__main__':
    packages: List[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
