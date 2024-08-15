import pandas as pd
from urls import IGPM_URL, IGPDI_URL
from tenacity import retry, wait_fixed, stop_after_attempt


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def fetch_igpm_fgv() -> pd.DataFrame:
    """
    Fetch and process IGP-M (FGV) data.

    Returns:
        pd.DataFrame: Processed IGP-M data with 'data' and 'IGPM_FGV' columns.
    """
    try:
        tables = pd.read_html(IGPM_URL)
        df = tables[0]

        # Filter for the current year
        df = df[df["Ano/Mês"] == 2024]

        df = df.drop(columns=["Ano/Mês"])
        df = df.melt(var_name="Month", value_name="IGPM_FGV")

        df["data"] = df["Month"] + "/2024"

        df = df.drop(columns=["Month"])

        # Reordena as colunas para 'Date' e 'Value'
        df = df[["data", "IGPM_FGV"]]

        # Month name to number mapping
        meses = {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12",
        }

        # Convert date format
        def converter_data(data):
            mes, ano = data.split("/")
            mes = meses[mes.lower()]
            return f"{ano}-{mes}-01"

        df["data"] = df["data"].apply(converter_data)

        # Clean IGPM_FGV values
        df["IGPM_FGV"] = (
            df["IGPM_FGV"]
            .astype(str)
            .str.replace(r"[()]", "", regex=True)
            .str.replace(r"%", "", regex=True)
            .str.replace(r"^\s*-\s*", "-", regex=True)
            .str.replace(",", ".")
        )

        # Convert to numeric and percentage
        # df['IGPM_FGV'] = pd.to_numeric(df['IGPM_FGV'], errors='coerce') / 100

        # Sort, set index, and return last 12 months
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")
        return df.tail(12)

    except Exception as e:
        print(f"Error fetching data for IGP-M (FGV): {e}")
        return pd.DataFrame()


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def fetch_igpdi_fgv() -> pd.DataFrame:
    """
    Fetch and process IGP-DI (FGV) data.

    Returns:
        pd.DataFrame: Processed IGP-DI data with 'data' and 'IGPDI_FGV' columns.
    """
    try:
        tables = pd.read_html(IGPDI_URL)
        df = tables[0]

        # Get the current year
        current_year = pd.Timestamp.now().year

        # Filter for the current year
        df = df[df["Ano/Mês"] == current_year]

        # Melt the dataframe to long format
        df = df.melt(id_vars=["Ano/Mês"], var_name="Month", value_name="IGPDI_FGV")

        # Create the 'data' column
        df["data"] = df["Month"] + "/" + df["Ano/Mês"].astype(str)

        # Drop unnecessary columns and reorder
        df = df[["data", "IGPDI_FGV"]]

        # Month name to number mapping
        meses = {
            "janeiro": "01",
            "fevereiro": "02",
            "março": "03",
            "abril": "04",
            "maio": "05",
            "junho": "06",
            "julho": "07",
            "agosto": "08",
            "setembro": "09",
            "outubro": "10",
            "novembro": "11",
            "dezembro": "12",
        }

        # Convert date format
        def converter_data(data):
            mes, ano = data.split("/")
            mes = meses[mes.lower()]
            return f"{ano}-{mes}-01"

        df["data"] = df["data"].apply(converter_data)

        # Clean IGPM_FGV values
        df["IGPDI_FGV"] = (
            df["IGPDI_FGV"]
            .astype(str)
            .str.replace(r"[()]", "", regex=True)
            .str.replace(r"%", "", regex=True)
            .str.replace(r"^\s*-\s*", "-", regex=True)
            .str.replace(",", ".")
        )

        # Convert to numeric and percentage
        # df['IGPDI_FGV'] = pd.to_numeric(df['IGPDI_FGV'], errors='coerce') / 100

        # Sort, set index, and return last 12 months
        df["data"] = pd.to_datetime(df["data"])
        df = df.sort_values("data")
        return df.tail(12)

    except Exception as e:
        print(f"Error fetching data for IGP-DI (FGV): {e}")
        return pd.DataFrame()
