import xlrd

dt = "05.05.2023"
FIO = "Полищук"

def parsteacher(date:str, FIO:str):

    file = xlrd.open_workbook("ExcelAndWord/prepod.xls")
    # Получаем список листов в файле
    sheet_names = file.sheet_names()
    # Выбираем первый лист (можете выбрать нужный вам)
    sheet = file.sheet_by_name(sheet_names[0])
    
    #Нахождение индекса Даты.
    date = sheet.row_values(1)
    indxdate = None
    for i in range(len(date)):
        if dt in date[i]:
            indxdate = i
    
    #Нахождение индекса ФИО.
    fio = sheet.col_values(0)
    indxfio = None
    for i in range(len(fio)):
        if FIO in fio[i]:
            indxfio = i
    
    arr = sheet.row_values(indxfio, indxdate, indxdate + 13)
    
    test = {'Номер':[1,2,3,4,5,6,7,8,9,10,11,12,13], 'Предмет':[], 'Группа':[], 'Кабинет':[],}
    
    for i in arr:
        if len(i) > 1:
            s = i.split("\n")[:4]
            test["Предмет"].append(s[0])
            if FIO in s[1]:
                grp = s[1].split("(")
                test['Группа'].append(grp[1])
            else:
                test["Группа"].append('Вся группа')
            kab = s[3].split(".")
            test["Кабинет"].append(kab[1])
        else:
            test["Предмет"].append('ничего')
            test["Группа"].append('ничего')
            test["Кабинет"].append('ничего')
    
    return test

print(parsteacher(dt, FIO))