from imports import *
from classes import *
from PIL import *
UrokOne = Urok(1,"Name",212,"Vladislave")
UrokTwo = Urok(2,"DrugoyNameфывфывфыфыввфыфыввфыфывфвывфывыфвфыфвывфыфыввфывфыфывывф",313,"Drugoy Vladislave")
a = Schedule(datetime.datetime.now(),[UrokOne,UrokTwo,UrokOne,UrokTwo,UrokOne,UrokTwo,UrokOne,UrokTwo,UrokOne,UrokTwo])
image = getScheduleAsImg(a)
image.save('schedule.png')
