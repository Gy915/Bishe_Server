import pandas as pd
import numpy as np



def HandleSchLevel(ser):
    data = ser.values
    data = np.array(data, dtype=str)
    for i in range(len(data)):
        if(data[i]== "985"):
          data[i] = 0.8
        elif(data[i] == "211"):
          data[i] = 0.6
        elif(data[i] == "双一流"):
          data[i] = 0.4
        elif(data[i] == "普通"):
          data[i] = 0.2
    data = np.array(data, dtype=float)
    return data
def HandleTeacherNum(ser):
    data = np.array(ser.values, dtype=float)
    #假设最小值为0， 最大值为max + 10
    data_scale = (data - 0)/(np.max(data) + 10 - 0)
    return data_scale
def HandleSubRank(ser):
    data = np.array(ser.values, dtype=str)
    dic = {"A+":9/10, "A":8/10, "A-":7/10, "B+":6/10, "B":5/10, "B-":4/10,
           "C+":3/10, "C":2/10, "C-":1/10,'0':-1}
    data_res = np.ones(len(data))
    for i in range(len(data)):
        val = dic[data[i]]
        data_res[i] = val
    return data_res
def HandleSchRank(ser):
    data = np.array(ser.values, dtype=float)
    data_res = 1 - (data - 1)/(np.max(data) + 10 - 1)
    return data_res
def HandleHighRank(ser):
    data = np.array(ser.values, dtype=float)
    data_res = 1 - (data - 1)/(np.max(data) + 10 - 1)
    return data_res
def HandleSubLevel(ser):
    data = np.array(ser.values, dtype=float)
    data_res = 1 - (data - np.min(data)/2)/(np.max(data)+0.1 - np.min(data)/2)
    return data_res


def HandleStuNum(ser):
    data = np.array(ser.values, dtype=float)
    data_res = (data - 0)/(np.max(data)+20 - 0)
    return data_res


def FillSubRank(df):
    dataOri = np.array(df["SB"].values,dtype=float)
    dataRefer = np.array(df["SuL"].values,dtype=float)
    dataRes = dataOri
    for i in range(len(dataOri)):
        if(dataOri[i]==-1):
            sulV = dataRefer[i]
            delta1 = np.array(abs(dataRefer - sulV))
            spec = np.where(delta1== np.min(delta1))
            for j in spec[0]:
                if(dataOri[j]+1!=-1):
                    dataRes[i] = dataOri[j]

    return dataRes
def CreateExcel(df):
    SchLevel = HandleSchLevel(df["学校层次"])
    print(np.max(SchLevel), np.min(SchLevel))
    TeacherNum = HandleTeacherNum(df["导师人数"])
    print(np.max(TeacherNum), np.min(TeacherNum))
    SubRank = HandleSubRank(df["第四轮学科排名"])
    print(np.max(SubRank), np.min(SubRank))
    SchRank = HandleSchRank(df["软科排名"])
    print(np.max(SchRank), np.min(SchRank))
    HighRank = HandleHighRank(df["高端人才排名"])
    print(np.max(HighRank), np.min(HighRank))
    SubLevel = HandleSubLevel(df["学科层次"])
    print(np.max(SubLevel), np.min(SubLevel))
    StuNum = HandleStuNum(df["招生人数"])
    print(np.max(StuNum), np.min(StuNum))

    df_dic = {"ScL":SchLevel, "SR":SchRank, "HR":HighRank, "TN":TeacherNum,"SB":SubRank,"SuL":SubLevel, "TG":StuNum}
    df_new = pd.DataFrame(df_dic)
    SubRank = FillSubRank(df_new)

    print(SubRank)
    df_new["SB"] = SubRank
    df_new.to_excel("./TrainData.xlsx")
if __name__ == '__main__':
    df = pd.read_excel('./毕设数据.xlsx')
    CreateExcel(df)



