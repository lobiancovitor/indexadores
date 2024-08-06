import requests
import pandas as pd
from urls import IPCA_URL, INPC_URL


def fetch_bcb_data(indicator: str) -> pd.DataFrame:
    """
    Fetch economic indicator data from the Brazilian Central Bank API and return as a pandas DataFrame.

    Args:
    indicator (str): The indicator to fetch. Must be either 'IPCA' or 'INPC'.

    Returns:
    pd.DataFrame: A DataFrame containing the last 12 months of data.

    Raises:
    ValueError: If an invalid indicator is provided.
    requests.RequestException: If there's an error with the API request.
    """
    if indicator.upper() == "IPCA":
        url = IPCA_URL
    elif indicator.upper() == "INPC":
        url = INPC_URL
    else:
        raise ValueError("Invalid indicator. Must be either 'IPCA' or 'INPC'.")

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()[-12:]
        df = pd.DataFrame(data)
        df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")
        df["valor"] = df["valor"].astype(float)
        df = df.sort_values("data")
        df = df.rename(columns={'valor': indicator})
        
        return df
    except requests.RequestException as e:
        print(f"Error accessing the API: {e}")
        return pd.DataFrame()
