import pandas as pd
import os
import src.signals as sigs
from datetime import date


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
