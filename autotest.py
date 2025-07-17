import asyncio,time
from aiohttp import ClientSession, ClientError, ClientConnectorError, ClientResponseError, ServerTimeoutError
from statistics import mean
from printresult import print_res

class auto_test: # Главный модуль выполнения http запросов
    def __init__(self, cs, host,fw=None):
        self.count_session = cs
        self.hosts = host
        self.fw = fw
    async def complite_send(self, session, host, result_test, all_times):
        start = time.perf_counter()
        try:
            async with session.get(host) as response:
                response.raise_for_status()
                result_test["Success"] += 1

        except ClientConnectorError:
            result_test["Error"] += 1
            print(f"Ошибка подключения к серверу, host - {host}")

        except ServerTimeoutError:
            result_test["Error"] += 1
            print(f"Таймаут при запросе к серверу, host - {host}")

        except ClientResponseError as e:
            if e.status in (400, 500):
                result_test["Failed"] += 1
            else:
                result_test["Error"] += 1
            print(f"HTTP ошибка со статусом {e.status}, host - {host}")

        except ClientError as e:
            result_test["Error"] += 1
            print(f"Ошибка на стороне клиента при связи с хостом: {e}")

        except Exception as e:
            result_test["Error"] += 1
            print(f"Непредвиденная ошибка при попытке связи с хостом: {e}")

        finally:
            if all(result_test[key] == 0 for key in ("Failed", "Error")):
                print("Лог: Успешный запрос!")
            end = time.perf_counter()
            all_times.append(end - start)

    async def make_send(self): #Клиент
        async with ClientSession() as session:
            for host in self.hosts:
                result_test = {"Success": 0, "Failed": 0, "Error": 0, "Other": 0}
                time_test = {"Max": 0, "Min": 999999, "Avg": 0}
                all_times = []
                tasks = [self.complite_send(session, host, result_test, all_times) for count_start_http in range(self.count_session)]
                await asyncio.gather(*tasks) # оптимизация при помощи ансинхронного выполнения задач

                time_test["Max"], time_test["Min"], time_test["Avg"] = max(all_times), min(all_times), mean(all_times)

                if self.fw != None:
                    self.fw.file_writer(host, result_test, time_test, flag=True)
                    print(f"Файл с результатами тестирования успешно создан/обновлён! ")
                elif self.fw == None:
                    print_res.print_results(h=host, r=result_test, t=time_test)
