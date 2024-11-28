from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

import pandas as pd
import numpy as np

from src.client.client_factory import ClientFactory

class Park(ABC):

    def __init__(self,
                 name: str, 
                 base_date: str, 
                 base_entry_price: float,
                 effectiveness: int,
                 price_index: str,
                 base_service_price: Optional[float] = None
                 ):
        
        self.name = name
        self.base_date = base_date
        self.base_entry_price = base_entry_price
        self.effectiveness = effectiveness
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

        price_var_table["VALDATA"] = price_var_table["VALDATA"] + pd.DateOffset(months=self.effectiveness)

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

    def get_base_service_price(self):

        today = datetime.today()

        if today < datetime(2022,12,1):
            return 0
        elif today < datetime(2023,12,1):
            return self.base_entry_price
        elif today < datetime(2024,12,1):
            return 93.17
        elif today < datetime(2025,12,1):
            return 103.52
        elif today < datetime(2026,12,1): 
            return 113.88
        else:
            return 124.23

    def get_actual_entry_prices(self):

        actual_service_price = self.get_base_service_price() * (self.get_last_index()/self.get_base_index())

        return round(float(actual_service_price), 0)


    def get_info_table(self):

        entry_price = self.get_actual_entry_prices()

        return{
            "Entrada": entry_price,
            "Mercosul/Brasil": 0.9*entry_price,
            "Entorno": 0.2*entry_price 
        }
    
class Macuco(Park):

    def get_info_table(self):

        service_price = self.get_actual_entry_prices()

        return {
            "Passeio do Macuco Tradicional": service_price
        }

class ParkFactory:

    @staticmethod
    def create_park(park: str) -> Park:

        if park == "Chapada dos Veadeiros":
            return ChapadaDosVeadeiros(
                name = "da Chapada dos Veadeiros",
                base_date = '2021-09-01',
                base_entry_price = 40.0,
                effectiveness = 2,
                price_index="IPCA",
                base_service_price= 22.0
            )
        
        elif park == "Itatiaia":

            return Itatiaia(
                name = "de Itatiaia",
                base_date = '2022-09-01',
                base_entry_price = 40.0,
                effectiveness= 2,
                price_index = "IPCA"
            )

        elif park == "Tijuca - Trem Corcovado":

            return TijucaTrem(
                name = "da Tijuca - Trem Corcovado",
                base_date = '2021-09-01',
                base_entry_price = 44.0,
                base_service_price = 60.0,
                effectiveness=2,
                price_index="IPCA"
            )
        
        elif park == "Tijuca - Paineiras":

            return TijucaPaineiras(
                name = "da Tijuca - Paineiras",
                base_date = '2021-09-01',
                base_entry_price = 44.0, 
                effectiveness= 2,
                price_index="IPCA"
            )

        elif park == "Fernando de Noronha":

            return FernandoDeNoronha(
                name = "Marinho Fernando de Noronha",
                base_date = '2023-08-01',
                base_entry_price = 358.0,
                effectiveness = 2,
                price_index = "IGP-M"
            )

        elif park == "Aparados da Serra e Serra Geral":

            return AparadosDaSerra(
                name = "de Aparados da Serra e Serra Geral",
                base_date = '2021-07-01',
                base_entry_price = 85.0,
                effectiveness = 2,
                price_index="IPCA"
            )
        
        elif park == "Iguaçu - Cataratas":

            return Iguacu(
                name = "do Iguaçu - Cataratas",
                base_date = '2022-11-01',
                base_entry_price = 82.82,
                effectiveness = 0,
                price_index = "IPCA"
            )
        
        elif park == "Iguaçu - Ilha do Sol":

            return Macuco(
                name = "do Iguaçu - Macuco Safari",
                base_date = '2022-09-01',
                base_entry_price = 0,
                effectiveness = 2,
                price_index = "IGP-M"
            )