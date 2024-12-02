from itertools import chain


def merge_intervals(intervals):
    """Функция для объединения пересекающихся интервалов."""
    if not intervals:
        return []

    # Сортировка интервалов по началу
    intervals.sort()
    merged = [intervals[0]]

    for current in intervals[1:]:
        previous = merged[-1]
        if current[0] <= previous[1]:
            # Объединение пересекающихся интервалов
            merged[-1] = (previous[0], max(previous[1], current[1]))
        else:
            # Добавление нового интервала в результат
            merged.append(current)

    return merged


def get_intersection(intervals1, intervals2):
    """Функция для нахождения пересечения двух списков интервалов."""
    intersections = []
    i, j = 0, 0
    while i < len(intervals1) and j < len(intervals2):
        start1, end1 = intervals1[i]
        start2, end2 = intervals2[j]

        # Поиск пересечений
        intersection_start = max(start1, start2)
        intersection_end = min(end1, end2)
        if intersection_start < intersection_end:
            intersections.append((intersection_start, intersection_end))

        # Передвигаемся к следующему интервалу
        if end1 < end2:
            i += 1
        else:
            j += 1

    return intersections


def get_total_time(intervals):
    """Функция возврата общего времени из интервалов."""
    return sum(end - start for start, end in intervals)


def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']

    # Формирование интервалов ученика и учителя
    pupil_intervals = list(zip(intervals['pupil'][::2], intervals['pupil'][1::2]))
    tutor_intervals = list(zip(intervals['tutor'][::2], intervals['tutor'][1::2]))

    # Ограничение интервалов учеников и преподавателей интервалом урока
    lesson_start, lesson_end = lesson
    lesson_interval = (lesson_start, lesson_end)

    def clamp(intervals, bounds):
        bound_start, bound_end = bounds
        return [(max(start, bound_start), min(end, bound_end)) for start, end in intervals if
                start < bound_end and end > bound_start]

    pupil_intervals = clamp(pupil_intervals, lesson_interval)
    tutor_intervals = clamp(tutor_intervals, lesson_interval)

    # Находим и объединяем пересечения между учеником и учителем
    intersection_intervals = get_intersection(pupil_intervals, tutor_intervals)
    merged_intersections = merge_intervals(intersection_intervals)

    # Возвращаем общее время пересечений
    return get_total_time(merged_intersections)


# Тестирование функции
tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'