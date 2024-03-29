import streamlit as st
import pandas as pd
from joblib import load
 
# Función para cargar el modelo KNN
def cargar_modelo_knn(ruta_modelo='modelo_nfl.joblib'):
    modelo = load(ruta_modelo)
    return modelo
 
# construcción de la interfaz de usuario en Streamlit
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
    # Realizar la predicción
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

col1, col2, col3 = st.columns([1,2,1])  # La relación aquí puede ser ajustada según necesites
with col2:
        st.image('200.gif')

# Ejecutar con: streamlit run app.py
