import os
import shutil
import fileinput
import sys
import csv
import random
import PySimpleGUI as sg
import cProfile
import pstats

profile = cProfile.Profile()

def create_new_list_file(num_in_list, market_segment, side, cust_dest):
    """uses template to create new xml file with name relating to number of items in list + the market segment"""
    src_dir = os.getcwd()
    if cust_dest == '':
        if which_env == 'QA':
            dest_dir = src_dir + f"\\lists\\QA"
        elif which_env == 'STG':
            dest_dir = src_dir + f"\\lists\\STG"
        elif which_env == 'LT':
            dest_dir = src_dir + f"\\lists\\LT"
    else:
        dest_dir = cust_dest

    src_file = os.path.join(src_dir, 'templates\\template.xml')
    shutil.copy(src_file, dest_dir)

    dest_file = os.path.join(dest_dir, 'template.xml')
    new_dest_file_name = os.path.join(dest_dir, f'NewOrderList{num_in_list}Items_{market_segment}_{side}.xml')

    # os.rename(dest_file, new_dest_file_name)
    # Checks if name already exists, if it does name increments + 1 until available
    while True:
        if os.path.exists(new_dest_file_name) == False:
            os.rename(dest_file, new_dest_file_name)
            break
        else:
            for i in range(2, 1000):
                new_dest_file_name = os.path.join(dest_dir, f'NewOrderList{num_in_list}Items_{market_segment}_{side}_v{i}.xml')
                if os.path.exists(new_dest_file_name) == False:
                    break


    return new_dest_file_name

##### Set up on GUI for user to select parameters ######

sg.theme('DarkBlue3')

layout = [  [sg.Text('Create a new suffix list template. Enter a value into each field below.', size=(80,1), text_color='white', font='Arial')],
            [sg.Text('Choose the environment', font='Arial'), sg.Combo(['QA', 'LT', 'STG'],default_value='QA',key='-ENV-', font='Arial')],
            [sg.Text('How many items in the list?', font='Arial'), sg.InputText('10', key='-NUMBER-', font='Arial')],
            [sg.Text('Choose the market segment', font='Arial'), sg.Combo(['HG', 'HY', 'EM', 'AG'],default_value='HG', key='-MS-', font='Arial')],
            [sg.Text('Choose the side of the list', font='Arial'), sg.Combo(['Buy', 'Sell', 'Both'],default_value='Buy', key='-SIDE-', font='Arial')],
            [sg.Text("Choose an output folder: ", font='Arial'), sg.Input(key="-IN2-"), sg.FolderBrowse(key="-DEST-", font='Arial')],
            [sg.Text(size=(60), key='-OUTPUT-')],
            [sg.Button('Create', font='Arial'), sg.Button('Exit', font='Arial')]
            ]

window = sg.Window('Create list templates', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Create': # If user clicks Create button the 5 variables below are populated and used in rest of code
        window['-OUTPUT-'].update('You have created a ' + values['-NUMBER-'] + ' item ' + values['-MS-'] + ' ' + values['-SIDE-'] + ' list, for ' + values['-ENV-'] + '.', text_color='white')
        which_env = values['-ENV-']
        num_in_list = values['-NUMBER-']
        list_market_segment = values['-MS-']
        buy_or_sell = values['-SIDE-']
        user_dest = values['-DEST-']

        #creates new file with number of items and market segment for list

        file_name = create_new_list_file(num_in_list, list_market_segment, buy_or_sell, user_dest) 

        ##### This section replaces the overall list count value with user input of number of list items in the template #####

        #Begins replacement of id 73 with correct number
        read_template = open(f'{file_name}', 'r')

        new_list_count = "" #string which contains basic template with id 73 replaced with number of orders in list
        for line in read_template:
            new_line = line.replace('<groups name="NoOrders" id="73" count="1">', f'<groups name="NoOrders" id="73" count="{num_in_list}">')
            new_list_count += new_line

        read_template.close() #Closes initial version of template

        #Writes new version of file with id 73 filled correctly
        write_template = open(f"{file_name}", 'w')
        write_template.write(new_list_count)
        write_template.close()

        #Second stage - replaces id 68 with number of orders in list
        read_template1 = open(f'{file_name}', 'r')

        new_list_count1 = "" #string which contains basic template with id 68 replaced with number of orders in list
        for line in read_template1:
            new_line1 = line.replace('<field name="TotNoOrders" id="68">1</field>', f'<field name="TotNoOrders" id="68">{num_in_list}</field>')
            new_list_count1 += new_line1

        read_template1.close() #Closes second version of template

        #Writes new version of file with id 68 and id 73 filled correctly with no. orders in list
        write_template1 = open(f"{file_name}", 'w')
        write_template1.write(new_list_count1)
        write_template1.close()

        ##### This section creates an instrument group for each instrument in the list #####

        #Opens the instrument group template as the base
        read_group_template = open('templates\\group_template.txt', 'r')

        group = "" # contents of template stored in this string
        for line in read_group_template:
            group += line

        group_newline = f'{group}\n' # adds a new line to separate each instrument group correctly
        multiple_groups = group_newline*(int(num_in_list)-1) # Create correct number of instrument groups based on no. orders in list
        read_group_template.close()

        append_groups_file = open(f'{file_name}', 'a+')
        append_groups_file.write(multiple_groups) # add N instrument group sections to the template with id 68 and id 73 filled
        append_groups_file.close()

        ##### This section appends tail of file to new list xml #####

        read_end_template = open('templates\\end_template.txt', 'r')
        append_end_file = open(f'{file_name}', 'a+')

        append_end_file.write(read_end_template.read())

        read_end_template.close()
        append_end_file.close()

        ##### This section replaces the list seq no. to increment for each order in list #####

        # Increments each subsequent id 67 with number up to total size of list to comply with correct numbering of items in list
        for i in range(1, int(num_in_list)):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="ListSeqNo" id="67">0</field>' in line:
                    line = line.replace('<field name="ListSeqNo" id="67">0</field>', f'<field name="ListSeqNo" id="67">{i}</field>')
                    i += 1
                else:
                    pass

                sys.stdout.write(line)

        ### Testing putting retrieving instruments in function - NOT FINISHED
        # def instrument_src(mktseg):
        #     if mktseg == 'HG':
        #         instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
        #     elif mktseg == 'HY':
        #         instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
        #     elif mktseg == 'EM':
        #         instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
        #     elif mktseg == 'AG':
        #         instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
        #     return instruments
            
        # instruments = ""

        # This section replaces instruments with n number
        # if which_env == 'QA':
        #     instrument_src(list_market_segment)
        # elif which_env == 'STG':
        #     instrument_src(list_market_segment)
        # elif which_env == 'LT':
        #     instrument_src(list_market_segment)
        
        ##### This section chooses which instrument file to look at based on environment selected by user and uses it as the source for filling each insrument
        # group with a random CUSIP #####

        if which_env == 'QA':
            if list_market_segment == 'HG' :
                instruments = open(f'instruments\\QA\\ALLHG.csv', 'r')
            elif list_market_segment == 'HY':
                instruments = open(f'instruments\\QA\\ALLHY.csv', 'r')
            elif list_market_segment == 'EM':
                instruments = open(f'instruments\\QA\\ALLEM.csv', 'r')
            elif list_market_segment == 'AG':
                instruments = open(f'instruments\\QA\\ALLAG.csv', 'r')
        elif which_env == 'STG':
            if list_market_segment == 'HG' :
                instruments = open(f'instruments\\QA\\ALLHG.csv', 'r')
            elif list_market_segment == 'HY':
                instruments = open(f'instruments\\QA\\ALLHY.csv', 'r')
            elif list_market_segment == 'EM':
                instruments = open(f'instruments\\QA\\ALLEM.csv', 'r')
            elif list_market_segment == 'AG':
                instruments = open(f'instruments\\QA\\ALLAG.csv', 'r')
        elif which_env == 'LT':
            if list_market_segment == 'HG' :
                instruments = open(f'instruments\\QA\\ALLHG.csv', 'r')
            elif list_market_segment == 'HY':
                instruments = open(f'instruments\\QA\\ALLHY.csv', 'r')
            elif list_market_segment == 'EM':
                instruments = open(f'instruments\\QA\\ALLEM.csv', 'r')
            elif list_market_segment == 'AG':
                instruments = open(f'instruments\\QA\\ALLAG.csv', 'r')

        csv_reader = csv.reader(instruments)

        lists_from_csv = []
        for row in csv_reader:
            lists_from_csv.append(row)

        #Generate random set of unique indexes to pick unique instruments from csv
        rand_indexes = []
        while len(rand_indexes) < (int(num_in_list) + 1):
            rand_index = random.randint(0, len(lists_from_csv))
            if rand_index not in rand_indexes:
                rand_indexes.append(rand_index)
            else:
                pass

        #Create list of random cusips from csv file
        cusips = []
        for i in rand_indexes:
            cusips.append(lists_from_csv[i].pop())
            i += 1

        #Replaces dummy instrument with random cusips from list of 300
        for i in range(1, int(num_in_list)):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="SecurityID" id="48">dummy_instrument</field>' in line:
                    line = line.replace('<field name="SecurityID" id="48">dummy_instrument</field>', f'<field name="SecurityID" id="48">{cusips[i]}</field>')
                    i += 1
                else:
                    pass

                sys.stdout.write(line)

        #Creates list of buy/sell or both sides
        side = []

        if buy_or_sell == 'Buy' :
            buy = 1
            side.append(buy)
            side *= int(num_in_list)
        elif buy_or_sell == 'Sell':
            sell = 2
            side.append(sell)
            side *= int(num_in_list)
        elif buy_or_sell == 'Both':
            for i in range(1, int(num_in_list)+1):
                n = random.randint(1, 2)
                side.append(n)
                i +=1


        for i in range(0, int(num_in_list)):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="Side" id="54">0</field>' in line:
                    line = line.replace('<field name="Side" id="54">0</field>', f'<field name="Side" id="54">{side[i]}</field>')
                    i += 1
                else:
                    pass

                sys.stdout.write(line)


window.close()