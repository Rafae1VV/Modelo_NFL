import streamlit as st
import pandas as pd
from joblib import load
import time
 
# Función para cargar el modelo KNN
def cargar_modelo_knn(ruta_modelo='modelo_nfl.joblib'):
    modelo = load(ruta_modelo)
    return modelo
 
# Inicia la construcción de la interfaz de usuario en Streamlit
st.title('Predicciones de Campo: Local o Visitante en la NFL')
 
# Widget para cargar archivos
st.header('Lugar para carga de archivo')
archivo_cargado = st.file_uploader("Carga tu archivo CSV", type=["csv"])
 
# Verificar si se cargó un archivo y procesarlo
if archivo_cargado is not None:
    # Leer el archivo CSV
    datos = pd.read_csv(archivo_cargado)
    datos_para_prediccion = datos.iloc[:,:8]
    # Cargar el modelo KNN
    modelo_knn = cargar_modelo_knn()
    # Realizar la predicción (asegúrate de ajustar esto a cómo tu modelo procesa los datos)
    prediccion = modelo_knn.predict(datos_para_prediccion)
    # Convertir la predicción en un DataFrame para una mejor visualización
    df_prediccion = pd.DataFrame(prediccion, columns=['Prediccion'])
    df_concatenado = pd.concat([datos.iloc[:, :2], datos.iloc[:, -2:], df_prediccion], axis=1)
    for index, row in df_concatenado.iterrows():
        if row["Prediccion"] == 1:
            df_concatenado.at[index,"Prediccion"] = row["home"]
        else:
            df_concatenado.at[index,"Prediccion"] = row["away"]
    # Mostrar el head de los primeros 5 resultados de la predicción
    st.header('Head de los primeros 5 resultados de la predicción')
    st.dataframe(df_concatenado.head(5))
 
    csv = df_concatenado.to_csv(index=False)
    st.download_button(
        label="Descargar predicciones como CSV",
        data=csv,
        file_name='predicciones.csv',
        mime='text/csv',
    )
# Espacio para mostrar un gif o cualquier otro contenido
#st.header('Aquí va un gif')
# Suponiendo que tienes un gif para mostrar, descomenta la línea siguiente y reemplaza la ruta
    
    # Lista de rutas de tus GIFs
lista_de_gifs = [
    '200.gif',
    'Nfl2.gif',
    'nfl3.gif',
    'nfl4.gif',
    'nfl5.gif',
]
# Marcador de posición para el GIF
col1, col2, col3 = st.columns([1,2,1])  # La relación aquí puede ser ajustada según necesites
with col2:
    espacio_gif = st.empty()
 
# Bucle para mostrar cada GIF
for gif in lista_de_gifs:
    espacio_gif.image(gif)
    # Pausa por 2 segundos antes de mostrar el siguiente GIF
    time.sleep(5)
 
# No olvides el resto de tu código Streamlit aquí
#col1, col2, col3 = st.columns([1,2,1])  # La relación aquí puede ser ajustada según necesites
#with col2:  # Usamos la columna del medio para el contenido que queremos centrar
    # Suponiendo que tienes un gif para mostrar, descomenta la línea siguiente y reemplaza la ruta
#    st.image('200.gif')

 
# Ejecutar con: streamlit run app.py
