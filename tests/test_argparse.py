import pytest
import argparse
import sys

def build_parser():
    parser = argparse.ArgumentParser(description="Автостестирование сайтов на Python")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-H', '--hosts', help='URL-адреса через запятую')
    group.add_argument('-f', '--file', help='Файл с URL-адресами')
    parser.add_argument('-o', '--output', help='Путь к JSON-файлу')
    parser.add_argument('-C', '--count', type=int, default=1, help='Количество запросов')
    return parser

def test_invalid_count_exit():
    parser = build_parser()
    test_args = ['-H', 'https://ya.ru', '-C', '0']
    args = parser.parse_args(test_args)
    assert args.count == 0

    with pytest.raises(SystemExit) as exc_info:
        if args.count <= 0:
            print("Ошибка: Аргумент --count должен быть положительным числом.")
            sys.exit(1)

    assert exc_info.type == SystemExit
    assert exc_info.value.code == 1