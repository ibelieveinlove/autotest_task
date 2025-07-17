from prettytable import PrettyTable

class print_res:
    def print_results(h, r, t):
        table = PrettyTable()
        table.title = f"Результаты тестирования хоста: {h}"
        print("\n")
        table.field_names = ["Показатель", "Значение"]
        table.add_row(["Успешные запросы", r['Success']])
        table.add_row(["Серверные/клиентские ошибки", r['Failed']])
        table.add_row(["Ошибки соединения и таймауты", r['Error']])
        table.add_row(["Прочие ответы", r['Other']])
        table.add_row(["Максимальное время", f"{t['Max']:.7f}"])
        table.add_row(["Минимальное время", f"{t['Min']:.7f}"])
        table.add_row(["Среднее время", f"{t['Avg']:.7f}"])
        print(table,"\n")