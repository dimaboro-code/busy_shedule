from datetime import datetime, timedelta
from typing import List, Dict


# Определение типа для расписания занятости
BusySchedule = List[Dict[str, str]]


def parse_time(time_str: str) -> datetime:
    """Преобразует строку времени в объект datetime."""
    return datetime.strptime(time_str, '%H:%M')


def find_free_windows(busy: BusySchedule) -> List[Dict[str, str]]:
    """
    Находит свободные окна по 30 минут в расписании.
    При условии, что перерыв будет не меньше 10 минут! При дальнейшем увеличении уровня точности
     возрастает нагрузка на систему.

    Args:
    - busy (BusySchedule): Расписание занятости.

    Returns:
    - List[Dict[str, str]]: Список свободных окон по 30 минут в формате {'start': 'HH:MM', 'stop': 'HH:MM'}.
    """
    start_time: datetime = parse_time('09:00')
    end_time: datetime = parse_time('21:00')
    free_windows: List[Dict[str, str]] = []
    current_time: datetime = start_time

    while current_time < end_time:
        busy_flag: bool = False
        for event in busy:
            event_start: datetime = parse_time(event['start'])
            event_stop: datetime = parse_time(event['stop'])
            if event_start <= current_time < event_stop:
                current_time = event_stop
                busy_flag = True
                break

            if event_start <= current_time + timedelta(minutes=10) <= event_stop:
                current_time = event_stop
                busy_flag = True
                break

            if event_start <= current_time + timedelta(minutes=20) <= event_stop:
                current_time = event_stop
                busy_flag = True
                break

            if event_start < current_time + timedelta(minutes=30) <= event_stop:
                current_time = event_stop
                busy_flag = True
                break

            if end_time < current_time + timedelta(minutes=30):
                busy_flag = True
                current_time = current_time + timedelta(minutes=30)

                break

        if not busy_flag:
            next_time: datetime = current_time + timedelta(minutes=30)
            free_windows.append({'start': current_time.strftime('%H:%M'), 'stop': next_time.strftime('%H:%M')})
            current_time = next_time

    return free_windows


# Использование функции для поиска свободных окон
busy_schedule: BusySchedule = [
    {'start': '10:30', 'stop': '10:50'},
    {'start': '18:40', 'stop': '18:50'},
    {'start': '14:40', 'stop': '15:50'},
    {'start': '16:40', 'stop': '17:20'},
    {'start': '20:05', 'stop': '20:20'}
]

free_windows = find_free_windows(busy_schedule)

print("Свободные окна по 30 минут:")
for window in free_windows:
    print(f"{window['start']} - {window['stop']}")
