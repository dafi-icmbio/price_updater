from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd
import numpy as np

from src.client.client_factory import ClientFactory

class Park(ABC):

    def __init__(self, 
                 base_date: str, 
                 base_entry_price: float,
                 update_frequency: int,
                 price_index: str,
                 base_service_price: Optional[float] = None
                 ):
        
        self.base_date = base_date
        self.base_entry_price = base_entry_price
        self.update_frequency = update_frequency
        self.price_index = price_index
        self.base_service_price = base_service_price

        self.index_table = self._update_index_table()

    @abstractmethod
    def _update_index_table(self):
        ...

    @abstractmethod
    def get_actual_entry_prices(self):
        ...
    
    @abstractmethod
    def get_base_index(self):
        ...

    @abstractmethod
    def get_last_index(self):
        ...

    @abstractmethod
    def get_info_table(self) -> dict:
        ...

class ChapadaDosVeadeiros(Park):

    def _update_index_table(self) -> pd.DataFrame:

        client = ClientFactory.create_ipea_client(index=self.price_index)

        return client.get_table()
    
    def get_base_index(self) -> np.float64:

        date = pd.Timestamp(self.base_date)

        base_index = self.index_table.query("VALDATA == @date").VALVALOR.iloc[0]

        return base_index
    
    def get_last_index(self):

        month = pd.Timestamp(self.base_date).month

        last_index = self.index_table.query("VALDATA.dt.month == @month").VALVALOR.iloc[-1]

        return last_index

    def get_actual_entry_prices(self):

        actual_entry_price = self.base_entry_price * (self.get_last_index()/self.get_base_index())

        return round(float(actual_entry_price), 0)

    def get_actual_service_prices(self):  

        actual_service_price = self.base_service_price * (self.get_last_index()/self.get_base_index())

        return round(float(actual_service_price), 0)
    
    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        camping_price = self.get_actual_service_prices()

        return {
            "Entrada": entry_price,
            "Meia Entrada": entry_price/2,
            "Entorno": round(entry_price*0.1, 0),
            "Acampamento": camping_price

        }
    
class ParkFactory:

    @staticmethod
    def create_park(park: str) -> Park:

        if park == "Chapada dos Veadeiros":
            return ChapadaDosVeadeiros(
                base_date = '2021-09-01',
                base_entry_price = 40.0,
                update_frequency = 12,
                price_index="IPCA",
                base_service_price= 22.0
            )
        



