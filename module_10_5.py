# Многопроцессное программирование
# Моделирование программы для управления данными о движении товаров на складе
# и эффективной обработки запросов на обновление информации в многопользовательской среде.
# Представим, что у вас есть система управления складом, где каждую минуту поступают запросы
# на обновление информации о поступлении товаров и отгрузке товаров.
# Наша задача заключается в разработке программы, которая будет эффективно обрабатывать
# эти запросы в многопользовательской среде, с использованием механизма мультипроцессорности
# для обеспечения быстрой реакции на поступающие данные.

from multiprocessing import Process, Manager
from colorama import Fore, Style, init

init(autoreset=False)


class WarehouseManager:
    """
    Менеджер склада: data - словарь (ключ - название продукта, значение - его кол-во, (изначально пустой))
    """

    def __init__(self):
        self.data = {}

    def process_request(self, request):
        """
        Реализует запрос (действие с товаром), принимая request - кортеж.
        В случае получения (receipt) данные поступают в data (добавляет пару, если её не было и изменяет значение ключа,
        если позиция уже была в словаре)
        В случае отгрузки (shipment) данные товара уменьшаются (если товар есть в data и если товара больше чем 0).
        """
        (product, action, quantity) = request[0], request[1], request[2]

        if action == 'receipt':
            if product in self.data.keys():
                self.data[product] += quantity
            else:
                self.data[product] = quantity
        elif action == 'shipment':
            if product in self.data.keys():
                if self.data[product] >= quantity:
                    self.data[product] -= quantity
                if self.data[product] < quantity:
                    print(f'{Fore.LIGHTGREEN_EX}{product}{Style.RESET_ALL} '
                          f'в наличии только-{Fore.LIGHTCYAN_EX}{self.data[product]}:\n'
                          f'{Style.RESET_ALL}для отгрузки указано неверное количество-'
                          f'{Fore.LIGHTRED_EX}{quantity}{Style.RESET_ALL}\n')
            else:
                print(f'{Fore.LIGHTGREEN_EX}{product}{Style.RESET_ALL} отсутствует на складе\n')

    def run(self, requests):
        """
        Принимает запросы и создаёт для каждого свой параллельный процесс,
        запускает его(start) и замораживает(join).
        """
        with Manager():
            self.data = Manager().dict()
            actions = []
            for request in requests:
                p = Process(target=self.process_request, args=(request,))
                actions.append(p)
                p.start()
                p.join()
            print(f'{Fore.LIGHTBLUE_EX}Наличие товаров на складе:')


if __name__ == '__main__':
    manager = WarehouseManager()
    requests = [
        ("product-1", "receipt", 100),
        ("product-2", "receipt", 150),
        ("product-1", "shipment", 30),
        ("product-3", "receipt", 200),
        ("product-2", "shipment", 50),
        ("product-4", "receipt", 50),  # для проверки условия - если товара меньше, чем было
        ("product-4", "shipment", 60),
        ("product-5", "shipment", 60)  # для проверки условия - если товара нет в наличии
    ]
    manager.run(requests)
    print(manager.data)
