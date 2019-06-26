#!/usr/bin/env python3

from csv import reader
from pathlib import Path
import re
from uuid import uuid4

rand_re = re.compile('<<<:RANDOM:>>>')

def gen_rand(known):

    while True:
        r = uuid4().__str__().split('-')[-1]
        if r not in known:
            return r

class Record:
    
    def __init__(self,headers,values):

        if headers.__len__() != values.__len__():

            raise Exception(
                'Headers and Value lengths must match'
            )

        for n in range(0,headers.__len__()):

            self.__setattr__(headers[n],values[n])

    def update_content(self, content, known=None):

        known = known or []

        for k,v in self.__dict__.items():

            # =======================================
            # HANDLE WHEN RANDOM CONTENT IS REQUESTED
            # =======================================

            if re.search(rand_re,content):

                content = re.sub(
                    rand_re,
                    gen_rand(known),
                    content
                )

            content = re.sub(
                re.escape(f'<<<:{k}:>>>'),
                v,content
            )

        return content

class CSV:

    def __init__(self,csv_file):

        if not Path(csv_file).exists():
            raise Exception(
                f'CSV file not found: {csv_file}'
            )

        self.headers = []
        self.raw_records = []
        self.records = []
        
        with open(csv_file, newline='') as infile:

            for row in reader(infile):

                if not self.headers:
                    self.headers = row
                    
                else:
                    self.raw_records.append(row)
                    self.records.append(Record(self.headers,row))
