import requests
import pandas as pd
from abc import ABC


class IpeaDataClient(ABC):

    ipea_root = "http://www.ipeadata.gov.br/api/odata4/Metadados"

    def __init__(self):
        self.sercodigo = None

    def get_table(self) -> pd.DataFrame:
        headers = {
            'Accept': 'application/json'
        }

        response = requests.get(
            url = self.ipea_root + f"('{self.sercodigo}')/Valores",
            headers=headers
        )

        if response.status_code == 200:
            try:
                data = response.json()
            except ValueError:
                print("Error: Could not retrieve data from IPEA.")

        df = pd.DataFrame(
            data=data.get("value")
        )

        df["VALDATA"] = pd.to_datetime(df["VALDATA"], utc=True).dt.floor("D").dt.tz_localize(None)

        return df

class IpcaClient(IpeaDataClient):

    def __init__(self):        
       self.sercodigo = "PRECOS12_IPCA12"

        
class IgpmClient(IpeaDataClient):

    def __init__(self):
        self.sercodigo = "IGP12_IGPM12"

class SelicClient(IpeaDataClient):

    def __init__(self):
        self.sercodigo = "GM366_TJOVER366"

class ClientFactory:

    @staticmethod
    def create_ipea_client(index: str) -> IpeaDataClient:
        if index == "IPCA":
            return IpcaClient()
        elif index == "IGP-M":
            return IgpmClient()
        elif index == "SELIC":
            return SelicClient()
        else:
            return ValueError(f"Unknown client type: {index}")


