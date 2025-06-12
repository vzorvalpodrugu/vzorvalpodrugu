from abc import ABC, abstractmethod

# class TechAnalysContext:
#     def __init__(self, strategy: "AbstractStrategy") -> None:
#         self.strategy = strategy
#
#     def set_strategy(self, strategy: "AbstractStrategy") -> None:
#         self.strategy = strategy
#
#     def execute_strategy(self, message: str):
#         return self.strategy.execute(message)
#
# class AbstractStrategy(ABC):
#     @abstractmethod
#     def execute(self, message: str) -> str:
#         pass
#
# class StrategyAnalysOne(AbstractStrategy):
#     def execute(self, message: str) -> str:
#         return f"Анализ 1: {message}"
#
# class StrategyAnalysTwo(AbstractStrategy):
#     def execute(self, message: str):
#         return f"Анализ 2: {message}"
#
# user_choise = input('Введите стратегию анализа 1 или 2: ')
#
# try:
#     int_choise = int(user_choise)
#
# except ValueError:
#     print('Вы ввели не число')
#     exit(1)
#
# if int_choise == 1:
#         strategy = StrategyAnalysOne()
# elif int_choise == 2:
#         strategy = StrategyAnalysTwo()
#
# context = TechAnalysContext(strategy)
# message = input('Введите сообщение для анализа: ')
# result = context.execute_strategy(message)
# print(result)

# -----------------------------------------------------------------------------------------------------------------------

class AbstractMarketObserver(ABC):
    @abstractmethod
    def update(self, data: dict) -> None:
        pass

class NotifyMarkerObserver(AbstractMarketObserver):
    def update(self, data: dict) -> None:
        BTC = data.get("BTC")
        ETH = data.get("ETH")

        if BTC >100000:
            print(f"BTC подорожал более, чем на 100000. Текущая цена: {BTC}")

        if ETH >100000:
            print(f"ETH подорожал более, чем на 100000. Текущая цена: {ETH}")

class TradeMarketObserver(AbstractMarketObserver):
    def update(self, data: dict) -> None:
        TON = data.get("TON", 0)
        LTC = data.get("LTC", 0)

        if TON > 5:
            print("ПРОДАЕМ ТОН МУЖИКИ")

        if LTC > 100:
                print("ПРОДАЕМ ЛИТКОИНЫ")

class Market:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.observers = []
        self.data = {}

    def add_observer(self, observer: AbstractMarketObserver) -> None:
        self.observers.append(observer)

    def remove_observer(self, observer: AbstractMarketObserver) -> None:
        self.observers.remove(observer)

    def _notify_observers(self, new_data: dict) -> None:
        for observer in self.observers:
            observer.update(self.data)

    def set_data(self, new_data: dict) -> None:
        self.data.update(new_data)
        self._notify_observers(new_data)

if __name__ == "__main__":
    market = Market("api_key")

    notify_observer = NotifyMarkerObserver()
    trade_observer = TradeMarketObserver()

    market.add_observer(notify_observer)
    market.add_observer(trade_observer)

    market.set_data({"BTC": 100000, "ETH": 100000, "TON": 10, "LTC": 100})
    market.set_data({"BTC": 120000, "ETH": 110000, "TON": 10, "LTC": 100})
    market.set_data({"BTC": 100000, "ETH": 100000, "TON": 10, "LTC": 100})
    market.set_data({"BTC": 130000, "ETH": 100000, "TON": 10, "LTC": 100})
    market.set_data({"BTC": 100000, "ETH": 130000})
