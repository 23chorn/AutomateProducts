import os

file_names = os.listdir('C:\\Users\\chorn\\Desktop\\SufFIXApplication\\SufFIX3.0.0\\suffixData\\templates\\FIX.4.4\\Script Generated Lists')

prefix = 'FIXListCreator='
new_faves = ""

for file in file_names:
    new_faves += f'{prefix}{file}=FIX.4.4/Script Generated Lists/{file}\n'


append_favourites = open('C:\\Users\\chorn\\Desktop\\SufFIXApplication\\SufFIX3.0.0\\suffixData\\favorites.cfg', 'a+')
append_favourites.write(new_faves)
append_favourites.close()