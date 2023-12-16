import unittest
from datetime import datetime, timedelta
from typing import List, Dict
from busy_schedule import find_free_windows, BusySchedule, parse_time


class TestFindFreeWindows(unittest.TestCase):

    def test_find_free_windows(self):
        busy_schedule: BusySchedule = [
            {'start': '10:30', 'stop': '10:50'},
            {'start': '18:40', 'stop': '18:50'},
            {'start': '14:40', 'stop': '15:50'},
            {'start': '16:40', 'stop': '17:20'},
            {'start': '20:05', 'stop': '20:20'}
        ]

        expected_result: List[Dict[str, str]] = [
            {'start': '09:00', 'stop': '09:30'},
            {'start': '09:30', 'stop': '10:00'},
            {'start': '10:00', 'stop': '10:30'},
            {'start': '10:50', 'stop': '11:20'},
            {'start': '11:20', 'stop': '11:50'},
            {'start': '11:50', 'stop': '12:20'},
            {'start': '12:20', 'stop': '12:50'},
            {'start': '12:50', 'stop': '13:20'},
            {'start': '13:20', 'stop': '13:50'},
            {'start': '13:50', 'stop': '14:20'},
            {'start': '15:50', 'stop': '16:20'},
            {'start': '17:20', 'stop': '17:50'},
            {'start': '17:50', 'stop': '18:20'},
            {'start': '18:50', 'stop': '19:20'},
            {'start': '19:20', 'stop': '19:50'},
            {'start': '20:20', 'stop': '20:50'}
        ]

        result = find_free_windows(busy_schedule)
        self.assertEqual(result, expected_result)

    def test_find_free_windows_single_busy_slot(self):
        # Тест с одним занятым интервалом
        busy_schedule: BusySchedule = [{'start': '10:30', 'stop': '11:00'}]

        expected_result: List[Dict[str, str]] = [
            {'start': '09:00', 'stop': '09:30'},
            {'start': '09:30', 'stop': '10:00'},
            {'start': '10:00', 'stop': '10:30'},
            {'start': '11:00', 'stop': '11:30'},
            {'start': '11:30', 'stop': '12:00'},
            {'start': '12:00', 'stop': '12:30'},
            {'start': '12:30', 'stop': '13:00'},
            {'start': '13:00', 'stop': '13:30'},
            {'start': '13:30', 'stop': '14:00'},
            {'start': '14:00', 'stop': '14:30'},
            {'start': '14:30', 'stop': '15:00'},
            {'start': '15:00', 'stop': '15:30'},
            {'start': '15:30', 'stop': '16:00'},
            {'start': '16:00', 'stop': '16:30'},
            {'start': '16:30', 'stop': '17:00'},
            {'start': '17:00', 'stop': '17:30'},
            {'start': '17:30', 'stop': '18:00'},
            {'start': '18:00', 'stop': '18:30'},
            {'start': '18:30', 'stop': '19:00'},
            {'start': '19:00', 'stop': '19:30'},
            {'start': '19:30', 'stop': '20:00'},
            {'start': '20:00', 'stop': '20:30'},
            {'start': '20:30', 'stop': '21:00'}
        ]

        result = find_free_windows(busy_schedule)
        self.assertEqual(result, expected_result)

    def test_find_free_windows_multiple_busy_slots(self):
        '''Тест с несколькими занятыми интервалами'''
        busy_schedule: BusySchedule = [
            {'start': '10:30', 'stop': '11:00'},
            {'start': '14:00', 'stop': '15:00'},
            {'start': '16:00', 'stop': '17:00'}
        ]

        expected_result: List[Dict[str, str]] = [
            {'start': '09:00', 'stop': '09:30'},
            {'start': '09:30', 'stop': '10:00'},
            {'start': '10:00', 'stop': '10:30'},
            {'start': '11:00', 'stop': '11:30'},
            {'start': '11:30', 'stop': '12:00'},
            {'start': '12:00', 'stop': '12:30'},
            {'start': '12:30', 'stop': '13:00'},
            {'start': '13:00', 'stop': '13:30'},
            {'start': '13:30', 'stop': '14:00'},
            {'start': '15:00', 'stop': '15:30'},
            {'start': '15:30', 'stop': '16:00'},
            {'start': '17:00', 'stop': '17:30'},
            {'start': '17:30', 'stop': '18:00'},
            {'start': '18:00', 'stop': '18:30'},
            {'start': '18:30', 'stop': '19:00'},
            {'start': '19:00', 'stop': '19:30'},
            {'start': '19:30', 'stop': '20:00'},
            {'start': '20:00', 'stop': '20:30'},
            {'start': '20:30', 'stop': '21:00'}
        ]

        # Получение свободных окон
        result = find_free_windows(busy_schedule)

        # Проверка соответствия ожидаемому результату
        self.assertEqual(result, expected_result)

    def test_find_free_windows_no_busy_slots(self):
        # Тест без занятых интервалов
        busy_schedule: BusySchedule = []

        start_time: datetime = parse_time('09:00')
        end_time: datetime = parse_time('21:00')
        current_time: datetime = start_time
        expected_result: List[Dict[str, str]] = []

        while current_time < end_time:
            next_time: datetime = current_time + timedelta(minutes=30)
            expected_result.append({'start': current_time.strftime('%H:%M'), 'stop': next_time.strftime('%H:%M')})
            current_time = next_time

        # Получение свободных окон
        result = find_free_windows(busy_schedule)

        # Проверка соответствия ожидаемому результату
        self.assertEqual(result, expected_result)

    def test_find_free_windows_full_busy_day(self):
        # Тест на полный занятый день
        busy_schedule: BusySchedule = [
            {'start': '09:00', 'stop': '21:00'}
        ]

        # Получение свободных окон
        result = find_free_windows(busy_schedule)

        # Проверка отсутствия свободных окон
        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
