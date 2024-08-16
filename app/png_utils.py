import os
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def format_percentage(value) -> str:
    if pd.isna(value):
        return "-"
    if isinstance(value, (int, float)):
        return f"{value:.2f}%"
    return str(value)


def save_table_png(data: pd.DataFrame, filename="table.png"):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.axis("off")

    data["data"] = pd.to_datetime(data["data"]).dt.strftime("%Y-%m-%d")

    formatted_data = data.applymap(format_percentage)

    table = ax.table(
        cellText=formatted_data.values,
        colLabels=formatted_data.columns,
        cellLoc="center",
        loc="center",
    )

    table.scale(1, 2)
    table.scale(1, 2)
    row_colors = ["#FFFFFF", "#F0F0F0"]
    for i in range(len(data)):
        color = row_colors[i % len(row_colors)]
        table._cells[(i + 1, 0)].set_facecolor(color)
        table._cells[(i + 1, 1)].set_facecolor(color)

    for j in range(len(data.columns)):
        table._cells[(0, j)].set_facecolor("#CCCCCC")

    plt.savefig(filename, bbox_inches="tight", dpi=300)
    plt.close(fig)


def save_all_indicators_as_png(data_dict: Dict[str, pd.DataFrame]):
    png_dir = "tables"
    os.makedirs(png_dir, exist_ok=True)

    for indicator, data in data_dict.items():
        filename = os.path.join(png_dir, f"{indicator}.png")
        save_table_png(data, filename)
        print(f"{indicator} table saved as PNG.")