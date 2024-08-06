from urls import IPC_FIPE_URL

import pandas as pd

def fetch_ipc_fipe() -> pd.DataFrame:
    """
    Fetch and process IPC-FIPE data.
    """
    try:
        tables = pd.read_html(IPC_FIPE_URL)
        df = tables[0]
        df = df.iloc[:, :2]  # Select the first two columns
        df.columns = ['data', 'IPC_Fipe']  # Rename columns

        # Create a mapping of Portuguese month names to month numbers
        meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }

        # Function to convert date from 'MMMM/YYYY' to 'YYYY-MM-DD'
        def converter_data(data):
            mes, ano = data.split('/')
            mes = meses[mes.lower()]
            return f"{ano}-{mes}-01"

        # Apply the conversion function
        df['data'] = df['data'].apply(converter_data)
        df['IPC_Fipe'] = pd.to_numeric(df['IPC_Fipe'], errors='coerce') / 100
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values(by='data')
        
        return df
    except Exception as e:
        print(f"Error fetching data for IPC-FIPE: {e}")
        return pd.DataFrame()