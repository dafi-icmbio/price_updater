from src.client.client_factory import ClientFactory
import pandas as pd

def test_ipca_client():

    ipca_client = ClientFactory.create_ipea_client(index="IPCA")

    data = ipca_client.get_table()

    if isinstance(data, pd.DataFrame):
        assert True

def test_igpm_client():

    igpm_client = ClientFactory.create_ipea_client(index="IGP-M")

    data = igpm_client.get_table()

    if isinstance(data, pd.DataFrame):
        assert True