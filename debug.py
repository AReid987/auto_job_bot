import csv
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from pprint import pprint
import ipdb
from csv_formatter import *
from pandas import DataFrame as pd

if __name__ == "__main__":
  with open('qa_pairs.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
      ipdb.set_trace()