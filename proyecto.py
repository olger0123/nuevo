import streamlit as st
import csv
from PIL import Image
import sqlite3
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(page_title='Energias')
def main():
    st.title('Produccion de Energias Renovables')
    img = Image.open('imagen_ER.jpg')
    st.image(img, use_container_width=True)

    st.subheader("Introducción") 
    st.write(""" La energía es el motor que impulsa el desarrollo económico y social de las naciones. Comprender las tendencias y patrones en la producción de energía nos permite identificar oportunidades para mejorar la eficiencia y sostenibilidad del uso energético. En particular, la producción de energías renovables ha cobrado una relevancia significativa en la lucha contra el cambio climático. La transición hacia fuentes de energía limpia, como la hidroeléctrica, eólica, solar y otras renovables, es crucial para reducir las emisiones de gases de efecto invernadero y mitigar el impacto ambiental.""")

    st.write(""" Dentro de este contexto, la región de Suramérica juega un papel fundamental. Países como Brasil, Colombia, Paraguay y Venezuela están liderando la producción de energía hidroeléctrica, aprovechando sus vastos recursos hídricos. En nuestras gráficas, se destaca la posición de Colombia en la producción de energía hidroeléctrica en comparación con otros países de la región. """)

    # Descripción con enlace a Colab
    st.markdown("""
    
    Puedes acceder al notebook en Google Colab haciendo clic en el siguiente enlace:
    [Abrir en Google Colab](https://github.com/olger0123/nuevo/blob/28262ceaef5bead2bebf434c127a2e78000fc827/Energias_renovables_GRUPO13.ipynb<TU_ID_DEL_NOTEBOOK>)
    """,
    unsafe_allow_html=True
     )
             
    # Lista de opciones disponibles
    opciones = ["SQL", "Plotly", "Pandas", "matplotlib","streamlit"]

    # Opciones fijas
    opciones_fijas = ["SQL", "Plotly", "Pandas", "matplotlib","streamlit"]



    # Multiselect con opciones predeterminadas
    seleccionadas = st.multiselect(
        "Herramientas y librerias utilizadas en este proyecto:",
        opciones,
        default=opciones_fijas)

    

     


    st.info(
    """
    **¿Qué es un TWh?**
    
    TWh significa **Teravatio-hora**. Es una unidad de medida de energía que representa la cantidad de electricidad consumida o generada en una hora.  
    - **1 TWh** equivale a **1 billón de vatios-hora (10¹² Wh)**.  
    - Se usa comúnmente para medir el consumo energético de países, industrias o grandes sistemas.
    """
    )
    
    


    st.subheader('Dataframe de Produccion de enegia')
    #dataframe
    df = pd.read_csv('modern-renewable-prod.csv', delimiter=';')
    st.dataframe(df)

    # Descripción para el gráfico
    st.markdown("""
     ### Producion de Energia Hidroelectrica de 1965 hasta 2021
     Este gráfico interactivo muestra la evolución de la producción de
     electricidad a partir de fuentes hidroeléctricas (en TWh) a lo largo de los años, desglosado por país. La visualización utiliza un mapa choroplético, donde cada país está coloreado según su nivel de producción eléctrica de origen hidroeléctrico en un año específico.
    
    """)
    #grafica de produccion de ene
    fig = px.choropleth(df.sort_values('Year'),
                        color='Electricity_from_hydro_TWh',
                        locations='Code',
                        locationmode='ISO-3',
                        color_continuous_scale='Plasma',
                        animation_frame='Year')
    st.plotly_chart(fig)
        
    # barras
    df_hydro = df.groupby('Entity', as_index=False)['Electricity_from_hydro_TWh'].sum()
    df_hydro.rename(columns={'Electricity_from_hydro_TWh': 'TOTAL'}, inplace=True) # Ordenar por 'TOTAL' en orden descendente y seleccionar las 10 primeras filas 
    df_hydro = df_hydro.sort_values(by='TOTAL', ascending=False).head(10)
    #grafico de barras

    fig1 = px.bar(df_hydro, x ='Entity',y = 'TOTAL', title='TOP 10 DE LOS PAISES QUE MAS PRODUCEN ENERGIA CON HIDROELECTRICA')
    xlabel = 'PAISES'
    ylabel = 'TOTAL en TWh'
    fig1.update_layout(xaxis_title=xlabel, yaxis_title=ylabel)
    st.plotly_chart(fig1)
    #df_comparacion
    df_comparacion = df[ df['Entity'].isin(['United States', 'China'])]
    #grafico de china vs usa
    
    custom_colors = {
    'China': 'red',               # Color personalizado para China
    'United States': 'blue'       # Color personalizado para EE. UU.
    }
    fig2 = px.line(df_comparacion,
     x='Year', y='Electricity_from_hydro_TWh',color ='Entity', title='Producion de Energia Hidroelectrica (China Vs United States)',color_discrete_map=custom_colors) 
    st.plotly_chart(fig2)

    #barras agrupadas
    df_agrupado = df[ df['Entity'].isin(['United States', 'China'])].groupby('Entity').agg({
         'Electricity_from_wind_TWh': 'sum',
         'Electricity_from_hydro_TWh': 'sum',
         'Electricity_from_solar_TWh': 'sum',
         'Electricity_from_other_renewables_TWh': 'sum' }).reset_index()
    df_agrupado.columns = ['Entity', 'Total_Wind', 'Total_Hydro', 'Total_Solar', 'Total_Other']

    df_long = df_agrupado.melt( id_vars="Entity", var_name="Fuente", value_name="Electricidad (TWh)" )

    #gráfico de barras agrupadas
    barra_aagrupas = px.bar(df_long,
                x='Entity',
                y='Electricidad (TWh)',
                color='Fuente',
                barmode='group',
                title='(Energias Renovables) China vs Usa')
    st.plotly_chart(barra_aagrupas)
    

    #grafico de pie
    df_pie = df[[ 'Electricity_from_wind_TWh', 'Electricity_from_hydro_TWh', 'Electricity_from_solar_TWh', 'Electricity_from_other_renewables_TWh' ]]
    df_pie = df_pie.apply(pd.to_numeric, errors='coerce') 
    nuevo_df = df_pie.sum().reset_index()
    nuevo_df.columns = ['Columna', 'Total']

    # grafico
    fig_pie = px.pie(nuevo_df, values='Total', names='Columna', title='Distribución de la Energía Renovable en el MUNDO')
    st.plotly_chart(fig_pie)

    #sur America 
    #grafico de barras nivel latino america
    img1 = Image.open('grafica_barras_suramerica.png')
    st.image(img1, use_container_width=True)

    df_comparacion2 = df[ df['Entity'].isin(['Brazil', 'Colombia', 'Paraguay', 'Venezuela']) ][['Entity', 'Year', 'Electricity_from_hydro_TWh']]

    #grafico comparativo sur america
    fig_comp = px.line(df_comparacion2, x='Year', y='Electricity_from_hydro_TWh',color ='Entity', title='Producion de Energia Hidroelectrica en SUR AMERICA')
    st.plotly_chart(fig_comp)

    #grafico de barras sur america
    df_agrupado2 = df[ df['Entity'].isin(['Brazil', 'Colombia', 'Paraguay', 'Venezuela']) ].groupby('Entity').agg({ 
        'Electricity_from_wind_TWh': 'sum',
        'Electricity_from_hydro_TWh': 'sum',
        'Electricity_from_solar_TWh': 'sum',
        'Electricity_from_other_renewables_TWh': 'sum' }).reset_index()
    
    df_agrupado2.columns = ['Entity', 'Total_Wind', 'Total_Hydro', 'Total_Solar', 'Total_Other']

    df_long2 = df_agrupado2.melt( id_vars="Entity", var_name="Fuente", value_name="Electricidad (TWh)" )

    #gráfico de barras agrupadas
    fig_barras_sur = px.bar(df_long2,
                 x='Entity',
                 y='Electricidad (TWh)',
                 color='Fuente',
                 barmode='group',
                 title='Energias Renovables a Nivel SUR AMERICA')
    st.plotly_chart(fig_barras_sur)
if __name__ == '__main__':
    main()