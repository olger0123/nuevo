import streamlit as st
import csv
from PIL import Image
import sqlite3
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title='Energias')
def main():
    st.title('Produccion de energias renovables')
    img = Image.open('imagen_ER.jpg')
    st.image(img, use_container_width=True)
    proyecto_final_db = sqlite3.connect('proyecto_final_db.db')
    llenar = proyecto_final_db.cursor()

    llenar.execute(''' CREATE TABLE IF NOT EXISTS energia_renovable_paises(
    Entity TEXT,
    Code TEXT,
    Year INTEGER,
    Electricity_from_wind_TWh ,
    Electricity_from_hydro_TWh REAL,
    Electricity_from_solar_TWh REAL,
    Electricity_from_other_renewables_TWh REAL
    )
    ''')
    with open('modern-renewable-prod.csv', 'r', encoding='utf-8') as archivo :
        lector = csv.reader(archivo, delimiter=';')
        next(lector)
        for fila in lector:
            llenar.execute('''
                            INSERT INTO energia_renovable_paises VALUES (?, ?, ?, ?, ?, ?, ?)
                            ''', fila)

    proyecto_final_db.commit()
    df = pd.read_sql_query('SELECT * FROM energia_renovable_paises', proyecto_final_db)
    st.dataframe(df)
    #categorizar la columnas
    df['Electricity_from_wind_TWh'] = pd.to_numeric(df['Electricity_from_wind_TWh'], errors='coerce')
    df['Electricity_from_hydro_TWh'] = pd.to_numeric(df['Electricity_from_hydro_TWh'], errors='coerce')
    df['Electricity_from_other_renewables_TWh'] = pd.to_numeric(df['Electricity_from_other_renewables_TWh'], errors='coerce')
    df['Year'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    df['Entity'] = df['Entity'].astype("string")
    df['Code'] = df['Code'].astype("string")
    print(df.info())
    

    # Comparacion de los paises que mas producen energia con hidro electricas
    df_comparacion = pd.read_sql_query('select Entity,Year,Electricity_from_hydro_TWh FROM energia_renovable_paises WHERE Entity IN ("United States","China")', proyecto_final_db)
    #grafico de china vs usa
    fig2 = px.line(df_comparacion, x='Year', y='Electricity_from_hydro_TWh',color ='Entity', title='Comparación de Produccion de Energia')
    st.plotly_chart(fig2)

if __name__ == '__main__':
    main()