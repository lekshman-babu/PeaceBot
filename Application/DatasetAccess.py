import pandas as pd
def main():
    fileName1='DataSet1'
    fileName2='DataSet2'
    fileName3='DataSet3'
    dataSetRoot='DataSets/'
    dataSet1=pd.read_csv(dataSetRoot+fileName1)
    # dataSet=dataSet1
    dataSet2=pd.read_csv(dataSetRoot+fileName2)
    # dataSet=dataSet2
    dataSet3=pd.read_csv(dataSetRoot+fileName3)
    # dataSet=dataSet3
    dataSet4=pd.read_csv(dataSetRoot+'DataSet4')
    # dataSet=dataSet4
    dataSet=pd.concat([dataSet2,dataSet3,dataSet4],ignore_index=True)
    return dataSet