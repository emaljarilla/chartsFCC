import pandas as pd
from pathlib import Path

#cargamos el CSV
csv_path = Path("data/cepaim.csv")
df=pd.read_csv(csv_path)

#Mostrar info básica
print("*** COLUMNAS DEL CSV ***")
print(df.columns.tolist())

print("*** DIMENSIONES ***")
print(f"Filas: {len(df)}")
print(f"Columnas: {len(df.columns)}")

print("*** TIPOS DE DATOS ***")
print(df.dtypes)

print("*** PRIMERAS 5 FILAS ***")
print(df.head())

print("*** VALORES UNICOS EN COLUMNAS CLAVE ***")
columnas_a_revisar=['sexo', 'nacionalidad','vulnerable','comunidad']
for col in columnas_a_revisar:
    if col in df.columns:
        print(f"\n{col}: {df[col].nunique()} valores unicos")
        print(df[col].value_counts().head())
    else:
        print(f"\n{col}: Columna NO ENCONTRADA")