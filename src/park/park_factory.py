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

    def _update_index_table(self) -> pd.DataFrame:

        client = ClientFactory.create_ipea_client(index=self.price_index)

        return client.get_table()

    def get_actual_entry_prices(self):

        actual_entry_price = self.base_entry_price * (self.get_last_index()/self.get_base_index())

        return round(float(actual_entry_price), 0)
    
    def get_base_index(self) -> np.float64:

        date = pd.Timestamp(self.base_date)

        base_index = self.index_table.query("VALDATA == @date").VALVALOR.iloc[0]

        return base_index

    def get_last_index(self):

        month = pd.Timestamp(self.base_date).month

        last_index = self.index_table.query("VALDATA.dt.month == @month").VALVALOR.iloc[-1]

        return last_index
    
    def get_price_var_table(self):

        date = pd.Timestamp(self.base_date)

        month = pd.Timestamp(self.base_date).month

        month_indexes = self.index_table.query("VALDATA.dt.month == @month and VALDATA >= @date")

        price_var_table = month_indexes.loc[:,["VALDATA", "VALVALOR"]]

        price_var_table["VALVAR"] = price_var_table["VALVALOR"]/price_var_table["VALVALOR"].shift(1)

        price_var_table["VALVAR"] = price_var_table["VALVAR"].fillna(1)

        price_var_table["VALPRECO"] = self.base_entry_price * price_var_table["VALVAR"].cumprod()

        price_var_table["VALDATA"] = price_var_table["VALDATA"] + pd.DateOffset(months=2)

        return price_var_table

    def get_actual_service_prices(self):

        actual_service_price = self.base_service_price * (self.get_last_index()/self.get_base_index())

        return round(float(actual_service_price), 0)

    @abstractmethod
    def get_info_table(self) -> dict:
        ...

class ChapadaDosVeadeiros(Park):
        
    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        camping_price = self.get_actual_service_prices()

        return {
            "Entrada": entry_price,
            "Meia Entrada": entry_price/2,
            "Entorno": round(entry_price*0.1, 0),
            "Acampamento": camping_price
        }
    
class Itatiaia(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return {
            "Entrada": entry_price,
            "Meia Entrada": entry_price/2,
            "Entorno": round(entry_price*0.1, 1)
        }

class TijucaTrem(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        train_price = self.get_actual_service_prices()

        return {
            "Entrada (Alta Temporada)": entry_price,
            "Entrada (Baixa Temporada)": entry_price/2,
            "Passagem": train_price,
        }

    def get_actual_service_prices(self):

        actual_service_price = self.base_service_price * (self.get_last_index()/self.get_base_index())

        return round(float(actual_service_price), 0)
            
class TijucaPaineiras(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return {
            "Entrada (Alta Temporada)": entry_price,
            "Entrada (Baixa Temporada)": entry_price/2,
        }
    
class FernandoDeNoronha(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return {
             "Entrada": entry_price,
             "Meia Entrada": entry_price/2
        }
    
class AparadosDaSerra(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return {
            "Entrada": entry_price
        }
    
class Iguacu(Park):

    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return{
            "Entrada": entry_price
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
        
        elif park == "Itatiaia":

            return Itatiaia(
                base_date = '2022-09-01',
                base_entry_price = 40.0,
                update_frequency= 12,
                price_index = "IPCA"
            )

        elif park == "Tijuca - Trem Corcovado":

            return TijucaTrem(
                base_date = '2021-09-01',
                base_entry_price = 44.0,
                base_service_price = 60.0,
                update_frequency=12,
                price_index="IPCA"
            )
        
        elif park == "Tijuca - Paineiras":

            return TijucaPaineiras(
                base_date = '2021-09-01',
                base_entry_price = 0, 
                update_frequency= 12,
                price_index="IGP-M"
            )

        elif park == "Fernando de Noronha":

            return FernandoDeNoronha(
                base_date = '2023-08-01',
                base_entry_price = 358.0,
                update_frequency = 12,
                price_index = "IGP-M"
            )

        elif park == "Aparados da Serra e Serra Geral":

            return AparadosDaSerra(
                base_date = '2021-07-01',
                base_entry_price = 85.0,
                update_frequency = 12,
                price_index="IPCA"
            )
        
        elif park == "Iguaçu":

            return Iguacu(
                base_date = '2022-03-01',
                base_entry_price = 100.0,
                update_frequency = 12,
                price_index = "IPCA"
            )