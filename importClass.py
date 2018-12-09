import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


DATABASE_URL = "postgres://stzunhlprsilqe:a3f1f9f217e9749383753f55b9a408c6582364ab75f2c36c5781537ee68aa577@ec2-50-17-203-51.compute-1.amazonaws.com:5432/demfabv2th1r11"
# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))


class importData:
    def __init__(self, file, table, no_columns, db_url = "postgres://stzunhlprsilqe:a3f1f9f217e9749383753f55b9a408c6582364ab75f2c36c5781537ee68aa577@ec2-50-17-203-51.compute-1.amazonaws.com:5432/demfabv2th1r11"
):
        self.db_url = db_url
        engine = create_engine(DATABASE_URL)
        db = scoped_session(sessionmaker(bind=engine))

        self.file = file
        self.table = table
        self.columns = []
        for i in range(no_columns):
            self.columns.append(str(input("Enter column name")))

    def printPretty(self):
        print("file:", self.file, "table:", self.table, "columns:", self.columns)




if __name__ == "__main__":
    book = importData("book.csv", "book", 4)
    book.printPretty()

