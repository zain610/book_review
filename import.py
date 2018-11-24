import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgres://stzunhlprsilqe:a3f1f9f217e9749383753f55b9a408c6582364ab75f2c36c5781537ee68aa577@ec2-50-17-203-51.compute-1.amazonaws.com:5432/demfabv2th1r11"
# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def extractData(file):
    '''
    This function is for taking in a file and inserting data into db.
    Reads data from csv file and creates insert statements to be enterred into db.
    Provide
    :param file: CSV(excel) files
    :return:
    '''

    f = open(file)
    reader = list(csv.reader(f))
    print(type(reader))
    for isbn, title, author, pubYear in reader[1::]:

        # print("isbn:", isbn, "\ttitle:", title, "\tauthor:", author, "\tyear:", year)
        db.execute("INSERT into book (isbn, title, author, year_publication) values (:isbn, :title, :author, :pubYear)", {"isbn": isbn, "title": title, "author": author, "pubYear": pubYear})
        db.commit()








if __name__ == "__main__":
    extractData("books.csv")
