# Домашнее задание по теме "Логирование"
# Цель: получить опыт использования простейшего логирования совместно с тестами.

import logging
import unittest
from unittest import TestCase


class Runner:
    def __init__(self, name, speed=5):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError(f'Имя может быть только строкой, передано {type(name).__name__}')
        self.distance = 0
        if speed > 0:
            self.speed = speed
        else:
            raise ValueError(f'Скорость не может быть отрицательной, сейчас {speed}')

    def run(self):
        self.distance += self.speed * 2

    def walk(self):
        self.distance += self.speed

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        elif isinstance(other, Runner):
            return self.name == other.name


class Tournament:
    def __init__(self, distance, *participants):
        self.full_distance = distance
        self.participants = list(participants)

    def start(self):
        finishers = {}
        place = 1
        while self.participants:
            for participant in self.participants:
                participant.run()
                if participant.distance >= self.full_distance:
                    finishers[place] = participant
                    place += 1
                    self.participants.remove(participant)

        return finishers


class RunnerTest(TestCase):
    is_frozen = False

    @unittest.skipIf(is_frozen, "")  # Так как is_frozen = False то тесты будут выполнены
    def test_walk(self):
        try:
            #run_cls1 = Runner('Вася', 5)
            run_cls1 = Runner('Вася', speed=-5)  # Передаем отрицательную скорость
            for _ in range(10):
                run_cls1.walk()
            self.assertEqual(run_cls1.distance, 50)
            logging.info('"test_walk" выполнен успешно')
        except ValueError as exc:
            #logging.warning('Неверная скорость для Runner')
            logging.exception('Неверная скорость для Runner')
            raise  # выбрасываем исключение после логирования

    @unittest.skipIf(is_frozen, "")
    def test_run(self):
        try:
            #run_cls2 = Runner('Илья', 5)
            run_cls2 = Runner(467)  # Передаем нестроковый тип для name
            for _ in range(10):
                run_cls2.run()
            self.assertEqual(run_cls2.distance, 100)
            logging.info('"test_run" выполнен успешно')
        except TypeError as exc:
            #logging.warning("Неверный тип данных для объекта Runner")
            logging.exception("Неверный тип данных для объекта Runner")
            raise  # выбрасываем исключение после логирования

    @unittest.skipIf(is_frozen, "")
    def test_challenge(self):
        run_cls_r = Runner('test')
        run_cls_w = Runner('test')
        for _ in range(10):
            run_cls_r.run()
            run_cls_w.walk()
        self.assertNotEqual(run_cls_r.distance, run_cls_w.distance)


logging.basicConfig(level=logging.INFO, filemode='w', filename='runner_tests.log', encoding='utf-8',
                    format="%(asctime)s | %(levelname)s : %(message)s")



# first = Runner('Вася', 10)
# second = Runner('Илья', 5)
# # third = Runner('Арсен', 10)
#
# t = Tournament(101, first, second)
# print(t.start())
