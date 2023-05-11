import pandas
import os
import numpy
import datetime
from ScheduleClass import Schedule
from UrokClass import Urok




date =  "12.05.2023"
group = "ИСиП 21-11-3"


def parstable(date:str, group:str):
    path = "ExcelAndWord"
    file = pandas.read_excel(os.path.join(path, "2table.xlsx"), sheet_name=None)
    csv = "Sheet"

    lstraspis = []
    
    flagdate = None
    for i in range(len(file[csv].values)):
        if flagdate:
            lstraspis.append(numpy.array(file[csv].values[i])) 
        if type(file[csv].values[i][0]) == str and "День" in file[csv].values[i][0] and flagdate:
            flagdate = None
        if type(file[csv].values[i][0]) == str and date in file[csv].values[i][0] and group in file[csv].values[i+1]:
            flagdate = True
    final = []
    
    indx = numpy.where(lstraspis[0] == group)[0][0]
    for i in lstraspis:
        arr = []
        arr.append(i[0])
        arr.append(i[indx])
        arr.append(i[indx+1])
        final.append(arr)
    return final 

def GetExcelSchedule(lst:list, grp:str):
    arg = {"Группа": grp,"№":[], "Урок":[], "Кабинет": [],"Преподаватель": []}

    arg["Группа"] = grp


    flag = False
    namepara = ""
    prepod = ""
    kab = ""
    for i in lst[2:]:
        if (type(i[0]) == int and flag) or (type(i[0]) == str and type(i[1]) == float and type(i[2]) == float) :
            flag = False
            arg["Урок"].append(namepara)
            arg["Кабинет"].append(kab)
            arg["Преподаватель"].append(prepod)
            namepara = ''
            prepod = ''
            kab = ''

        if type(i[0]) == int and type(i[1]) != float:
            arg["№"].append(i[0])
            namepara += i[1] + ' '
            kab += str(i[2]) + ' '
            flag = True

        if type(i[0]) == float and type(i[1]) == str and type(i[2]) == float :
            prepod += i[1] + ' '

        if type(i[0]) == float and type(i[1]) == str and type(i[2]) == int:
            namepara += i[1] + ' '
            kab += str(i[2]) + ' '


    govnolist = []
    for i in range(len(arg["Урок"])):
        a = Urok(Name = arg["Урок"][i],Kabinet = arg["Кабинет"][i],Number = arg["№"][i],Prepod = arg["Преподаватель"][i])
        govnolist.append(a)
    govno1 = Schedule(datetime.datetime.strptime(date, "%d.%m.%Y").date(), govnolist)
    return govno1


for i in parstable(date, group):
    print(i)

for i in GetExcelSchedule(parstable(date, group), group).Uroki:
    print(i.Number, i.Name, i.Prepod, i.Kabinet)



            



    




