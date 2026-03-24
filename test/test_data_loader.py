import pytest
import pandas as pd
from pathlib import Path

from src.data_loader import load_csv
from config.settings import CEPAIM_CSV

def test_load_csv_con_ruta_valida_devuelve_dataframe():
    """
    Cuando el archivo CSV existe y es valido. load_csv 
    debe devolver un objeto pandas DataFrame
    """
    #ACT: Llamar a la funcuin con la rura del CSV
    resultado = load_csv(CEPAIM_CSV)
    #El assert: verifica que el resulrtado es un DataFrame
    assert isinstance(resultado, pd.DataFrame)
