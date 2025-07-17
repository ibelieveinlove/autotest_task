import os,json
from pydantic import BaseModel, HttpUrl, ValidationError
class URLModel(BaseModel):
    url: HttpUrl

def url_checker(url: str):
    try:
        URLModel(url=url)
        return True
    except ValidationError:
        return False

class file_worker: #Модуль работы с файлами (чтение/запись)
    def __init__(self, filehost):
        self.file = filehost
        self.hosts = []

    def file_reader(self):
        try:
            with open(str(self.file), 'r') as file:
                for i in file:
                    self.hosts.append(i.strip())
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.file} не найден!")
        except IOError:
            raise IOError(f"Ошибка при открытии файла {self.file}!")
        for i in self.hosts:
            if not url_checker(i):
                raise ValueError(f"Формат ссылки {i} не верный!")
        return self.hosts

    def file_writer(self, host, result, timing, flag):
        if not flag:
            return 0
        else:
            new_record = {
                "Хост": host,
                "Успешные": result["Success"],
                "Ошибки": result["Failed"],
                "Сбои": result["Error"],
                "Прочие": result["Other"],
                "Время (макс)": round(timing["Max"], 7),
                "Время (мин)": round(timing["Min"], 7),
                "Время (среднее)": round(timing["Avg"], 7)
            }

            if os.path.exists(self.file) and os.path.getsize(self.file) > 0:
                try:
                    with open(self.file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                except (json.JSONDecodeError, FileNotFoundError):
                    data = []
            else:
                data = []

            data.append(new_record)

            with open(self.file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
