import pandas as pd
import os
import src.signals as sigs
from datetime import date
import numpy as np
import matplotlib.pyplot as plt


class Journal:
    def __init__(self):
        self.journal_path = "journal/journal.csv"

        if not os.path.exists(self.journal_path):
            df_vacio = pd.DataFrame(
                columns=["Fecha", "Aprobados", "Desaprobados"])
            df_vacio.to_csv(self.journal_path, index=False)

        self.journal = pd.read_csv(self.journal_path, parse_dates=["Fecha"])
        self.journal.set_index("Fecha", inplace=True)

        if pd.Timestamp(date.today()) not in self.journal.index:
            self.insertRow()

    def addByCategory(self, category):
        today = pd.Timestamp(date.today())
        if category == sigs.TX_APPROVED:
            self.journal.loc[today, "Aprobados"] += 1
        elif category == sigs.TX_REJECT:
            self.journal.loc[today, "Desaprobados"] += 1
        self.journal.to_csv(self.journal_path)

    def insertRow(self):
        today = pd.Timestamp(date.today())
        self.journal.loc[today] = [0, 0]

    def getGraphic(self):
        df = pd.read_csv("journal/journal.csv")
        x = np.arange(len(df["Fecha"]))
        ancho = 0.35  # Ancho de las barras

        plt.figure(figsize=(8, 5))
        plt.bar(x - ancho/2, df["Aprobados"],
                width=ancho, label='Aprobados', color='red')
        plt.bar(x + ancho/2, df["Desaprobados"],
                width=ancho, label='Reprobados', color='green')

        plt.xlabel('Fecha')
        plt.ylabel('Cantidad')
        plt.title('Comparación de Cantidad por Fecha')
        plt.xticks(x, df["Fecha"])
        plt.legend()
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        plt.tight_layout()
        plt.savefig('comparacion_ventas.png', dpi=300)

        plt.show()
