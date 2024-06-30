import encodings
import os
import pandas as pa
from userfunctions import Extract_Patterns
p2='C:/Users/vgunaganti/PycharmProjects/match/Jobs/p0_job_dnf1.txt'
#dnf gets new feature master in nex
def dnf_to_excel(p2):

        with open(p2, 'r') as f:
            data = f.read()
        data=data.split('\n')
        i=0
        keywords = ["Observation=", "ID=", "DDNAME=", "DSLIST="]
        for line in data:
          for keyword in keywords:
            if f"{keyword}" in line:
                parts = line.split()

                keyword_index = parts.index(f"{keyword}=") + 1
                value = parts[keyword_index]

                print(f"{keyword}: {value}")
            else:
                print(f"{keyword} not found.")


dnf_to_excel(p2)
