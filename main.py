import asyncio,argparse,sys
from autotest import auto_test
from fileworker import file_worker, url_checker

async def main():
    #argparser_group(оформление флагов)____________________________________________________________________________________
    agobject = argparse.ArgumentParser(description="Автостестирование сайтов на Python")
    source_group = agobject.add_mutually_exclusive_group(required=True)
    source_group.add_argument('-H', '--hosts', help='URL-адреса через запятую (например, https://ya.ru,https://google.com)')
    source_group.add_argument('-f', '--file', help='Файл с URL-адресами (по одному на строку)')
    agobject.add_argument('-o', '--output', help='Путь к JSON-файлу для сохранения результатов/Имя нового JSON файла')
    agobject.add_argument('-C', '--count', type=int, default=1,help='Количество запросов к каждому сайту (по умолчанию: 1)')
    args = agobject.parse_args()
    # argparser_group(оформление флагов)____________________________________________________________________________________

    try:
        if args.count <= 0: #Проверка верного значения для количества запросов
            raise ValueError("Аргумент --count должен быть положительным числом.")
    except ValueError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

    if args.hosts: #Проверка источника данных
        urls = [url.strip() for url in args.hosts.split(',') if url.strip()]
        if not urls:
            print("Ошибка: список URL пуст.")
            sys.exit(1)
        for i in urls:
            if not url_checker(i):
                print(f"Формат ссылки {i} не верный!")
                sys.exit(1)
    elif args.file:
        try:
            fw = file_worker(args.file)
            urls = fw.file_reader()
        except ValueError as e:
            print(e)
            sys.exit(1)

    if args.output: #Проверка способа экспорта
        try:
            fw = file_worker(args.output)
        except Exception as e:
            print(f"Ошибка при создании файла: {e}")
            sys.exit(1)
    else:
        fw = None
    at = auto_test(cs=args.count, host=urls, fw=fw)

    try:
        await at.make_send() #Выполнение запросов
    except Exception as e:
        print(f"Ошибка во время тестирования: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("\n")
    asyncio.run(main())
    print("\n")
