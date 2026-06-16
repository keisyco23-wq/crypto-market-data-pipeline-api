import requests
import pandas as pd
from datetime import datetime

def extract_crypto_data():
    print("Iniciando la extracción de datos desde la API...")
    
    # URL pública de la API de CoinGecko para obtener precios en tiempo real
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'ids': 'bitcoin,ethereum,solana,cardano',
        'order': 'market_cap_desc'
    }
    
    try:
        # 1. Petición programática a la API
        response = requests.get(url, params=params)
        response.raise_for_status() # Lanza un error si la respuesta falla
        data = response.json()
        
        # 2. Transformación de JSON estructurado a un DataFrame de Pandas
        df = pd.DataFrame(data)
        
        # Seleccionamos las columnas clave para el negocio financiero
        columns_to_keep = ['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'last_updated']
        df_cleaned = df[columns_to_keep]
        
        # Agregar estampa de tiempo de la ejecución
        df_cleaned['extracted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print("✅ Extracción y limpieza completadas con éxito.")
        print(df_cleaned.head())
        
        # 3. Exportación del set de datos limpio para analistas de BI
        df_cleaned.to_csv("crypto_market_data.csv", index=False)
        print("📁 Archivo 'crypto_market_data.csv' generado listo para ingesta.")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error en la conexión o límite de la API alcanzado: {e}")

if __name__ == "__main__":
    extract_crypto_data()
