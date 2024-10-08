from fetch.fetch_bcb import fetch_bcb_data
from fetch.fetch_bi import process_poupanca_data, process_tr_data
from fetch.fetch_fgv import fetch_igpdi_fgv, fetch_igpm_fgv
from fetch.fetch_fipe import fetch_ipc_fipe
from png_utils import save_all_indicators_as_png
from save import save_indicator_data
from urls import POUPANCA_URL, TR_URL


def fetch_all_indicators():
    return {
        "IPCA": fetch_bcb_data("IPCA"),
        "INPC": fetch_bcb_data("INPC"),
        "TR": process_tr_data(TR_URL),
        "Poupanca": process_poupanca_data(POUPANCA_URL),
        "IGP_DI": fetch_igpdi_fgv(),
        "IGP_M": fetch_igpm_fgv(),
        "IPC_FIPE": fetch_ipc_fipe(),
    }


def main():
    try:
        data_dict = fetch_all_indicators()
        save_indicator_data(data_dict)
        print("All indicator data fetched and saved successfully.")

        save_all_indicators_as_png(data_dict)
        print("All indicator tables saved as PNG files.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
