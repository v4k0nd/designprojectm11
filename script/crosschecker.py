import pandas as pd

'''
param:
    csv1 - path to first csv file
    csv2 - path to second csv file
    join_on - common column between the two files that will be used for the join
output:
    a csv file that is the result of the merge between csv1 and csv2 based on the specified join column
'''
def merge(csv1, csv2, join_on):
    table1 = pd.read_csv(csv1)
    table2 = pd.read_csv(csv2)

    if len(table1.index) < len(table2.index):
        join = "left"
    else:
        join = "right"

    merge_result = pd.merge(table1, table2, how=join, on=join_on)
    merge_result.to_csv("merge_result.csv")
