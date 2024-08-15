import pandas as pd
from tenacity import retry, wait_fixed, stop_after_attempt


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def process_tr_data(url, year="2024"):
    """
    Processa os dados da TR obtidos de uma URL e formata os valores e datas.

    Args:
    - url (str): URL da qual os dados da TR são lidos.
    - year (str): Ano a ser adicionado às datas. Padrão é '2024'.

    Returns:
    - pd.DataFrame: DataFrame com as colunas 'data' e 'TR' formatadas.
    """
    try:
        # Ler a tabela da URL
        tables = pd.read_html(url)
        df = tables[0]

        # Selecionar as duas primeiras colunas
        df = df.iloc[:, :2]
        df.columns = ["data", "TR"]

        # Criar uma coluna de data no formato YYYY-MM-DD
        df["data"] = df["data"] + "/" + year

        # Dicionário para conversão de meses
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

        def converter_data(data):
            """
            Converte a data do formato 'MMMM/YYYY' para 'YYYY-MM-DD'.

            Args:
            - data (str): Data no formato 'MMMM/YYYY'.

            Returns:
            - str: Data no formato 'YYYY-MM-DD'.
            """
            mes, ano = data.split("/")
            mes = meses[mes.lower()]
            return f"{ano}-{mes}-01"

        # Aplicar a função de conversão
        df["data"] = df["data"].apply(converter_data)

        # Remover '%' e substituir vírgula por ponto
        df["TR"] = (
            df["TR"]
            .astype(str)
            .str.replace("%", "", regex=True)
            .str.replace(",", ".")
            .astype(float)
        )

        return df
    except Exception as e:
        print(f"Error fetching data for TR: {e}")
        return pd.DataFrame()

@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def process_poupanca_data(url, year="2024"):
    """
    Processa os dados da TR obtidos de uma URL e formata os valores e datas.

    Args:
    - url (str): URL da qual os dados da TR são lidos.
    - year (str): Ano a ser adicionado às datas. Padrão é '2024'.

    Returns:
    - pd.DataFrame: DataFrame com as colunas 'data' e 'TR' formatadas.
    """
    try:
        # Ler a tabela da URL
        tables = pd.read_html(url)
        df = tables[0]

        # Selecionar as duas primeiras colunas
        df = df.iloc[:, :2]
        df.columns = ["data", "Poupanca"]

        # Criar uma coluna de data no formato YYYY-MM-DD
        df["data"] = df["data"] + "/" + year

        # Dicionário para conversão de meses
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

        def converter_data(data):
            """
            Converte a data do formato 'MMMM/YYYY' para 'YYYY-MM-DD'.

            Args:
            - data (str): Data no formato 'MMMM/YYYY'.

            Returns:
            - str: Data no formato 'YYYY-MM-DD'.
            """
            mes, ano = data.split("/")
            mes = meses[mes.lower()]
            return f"{ano}-{mes}-01"

        # Aplicar a função de conversão
        df["data"] = df["data"].apply(converter_data)

        # Remover '%' e substituir vírgula por ponto
        df["Poupanca"] = (
            df["Poupanca"]
            .astype(str)
            .str.replace("%", "", regex=True)
            .str.replace(",", ".")
            .astype(float)
        )

        return df

    except Exception as e:
        print(f"Error fetching data for TR: {e}")
        return pd.DataFrame()
