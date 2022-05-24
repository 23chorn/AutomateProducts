from audioop import add
import os
import shutil
import fileinput
import sys
import csv
import random
from turtle import right
import PySimpleGUI as sg


def create_new_list_file(num_in_list, market_segment, side, with_limits, cust_dest):
    """uses template to create new xml file with name relating to number of items in list + the market segment"""
    src_dir = os.getcwd()
    if cust_dest == '':
        if which_env == 'QA':
            dest_dir = src_dir + f"\\lists\\QA"
        elif which_env == 'STG':
            dest_dir = src_dir + f"\\lists\\STG"
    else:
        dest_dir = cust_dest
    
    if with_limits == 'Yes':
        with_limits = '_Limits'
    else:
        with_limits = ''

    src_file = os.path.join(src_dir, 'templates\\template.xml')
    shutil.copy(src_file, dest_dir)

    dest_file = os.path.join(dest_dir, 'template.xml')
    new_dest_file_name = os.path.join(dest_dir, f'NewOrderList{num_in_list}Items_{market_segment}_{side}{with_limits}.xml')

    # os.rename(dest_file, new_dest_file_name)
    # Checks if name already exists, if it does name increments + 1 until available
    while True:
        if os.path.exists(new_dest_file_name) == False:
            os.rename(dest_file, new_dest_file_name)
            break
        else:
            for i in range(2, 1000):
                new_dest_file_name = os.path.join(dest_dir, f'NewOrderList{num_in_list}Items_{market_segment}_{side}{with_limits}_v{i}.xml')
                if os.path.exists(new_dest_file_name) == False:
                    break


    return new_dest_file_name

##### Set up on GUI for user to select parameters ######

sg.theme('DarkBlue3')

layout = [  [sg.Text('Create a new suffix list template. Enter a value into each field below.', size=(80,1), text_color='white', font='Arial')],
            [sg.Text('Choose the environment', font='Arial'), sg.Combo(['QA', 'STG'],default_value='QA',key='-ENV-', font='Arial')],
            [sg.Text('How many items in the list?', font='Arial'), sg.InputText('10', key='-NUMBER-', font='Arial')],
            [sg.Text('Choose the market segment', font='Arial'), sg.Combo(['HG', 'HY', 'EM', 'AG', 'USPortfolio', 'EUPortfolio', 'LoanPortfolio', 'EUPrice', 'EUGov', 'EUHY', 'JPY', 'EUNonCore', 'EMLocal', 'EMLocalAsia', 'CNY'],default_value='HG', key='-MS-', font='Arial')],
            [sg.Text('Choose the side of the list', font='Arial'), sg.Combo(['Buy', 'Sell', 'Both'],default_value='Buy', key='-SIDE-', font='Arial')],
            [sg.Text('Add random limits for orders?', font='Arial'), sg.Combo(['Yes', 'No'],default_value='No', key='-LIMIT-', font='Arial')],
            [sg.Text("Choose an output folder: ", font='Arial'), sg.Input(key="-IN2-"), sg.FolderBrowse(key="-DEST-", font='Arial')],
            [sg.Text(size=(60), key='-OUTPUT-')],
            [sg.Button('Create', font='Arial'), sg.Button('Exit', font='Arial')],
            [sg.Push(), sg.Text("v1.0", font='Arial, 8')]
            ]

window = sg.Window('FIX List Creator', layout)

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
        add_limits = values['-LIMIT-']
        user_dest = values['-DEST-']

        #creates new file with number of items and market segment for list

        file_name = create_new_list_file(num_in_list, list_market_segment, buy_or_sell, add_limits, user_dest) 

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
        if add_limits == 'No':
            read_group_template = open('templates\\group_template.txt', 'r')
        else:
            read_group_template = open('templates\\groupwithlimit_template.txt', 'r')

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

        ################# Trying to put action in a function for reuse -- NOT FINISHED        
        # def write_to_template(name_of_file, line_to_replace):
        #     sequence_iter = 1
        #     while sequence_iter < int(num_in_list):
        #         for line in fileinput.input(name_of_file, inplace=1):
        #             if line_to_replace in line:
        #                 for char in line_to_replace:
        #                     if char == '0':
        #                         char = char.replace('0', str(sequence_iter))
        #                 sequence_iter += 1
        #         else:
        #             pass

        #         sys.stdout.write(line)

        # listseqno_line1 = '<field name="ListSeqNo" id="67">0</field>'
        # write_to_template(file_name, listseqno_line1)
        
        seq_iter = 1
        while seq_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="ListSeqNo" id="67">0</field>' in line:
                    line = line.replace('<field name="ListSeqNo" id="67">0</field>', f'<field name="ListSeqNo" id="67">{seq_iter}</field>')
                    seq_iter += 1
                else:
                    pass

                sys.stdout.write(line)

        ##### This section chooses which instrument file to look at based on environment/mktsegment selected by user and uses it as the source for filling each insrument
        # group with a random CUSIP #####
        
        def instrument_src(environment, mktseg):
            instruments = open(f'instruments\\{environment}\\{mktseg}.csv', 'r')
            return instruments

        user_mktseg = instrument_src(which_env, list_market_segment)
        csv_reader = csv.reader(user_mktseg)

        # adds all cusips from instruments csv into a list
        lists_from_csv = list(csv_reader)

        #Generate random set of unique indexes to pick unique instruments from csv
        rand_indexes = []
        while len(rand_indexes) < (int(num_in_list) + 1):
            rand_index = random.randint(0, len(lists_from_csv))
            if rand_index not in rand_indexes:
                rand_indexes.append(rand_index)
            else:
                pass

        #Create list of random cusips from csv file
        cusips = [lists_from_csv[i].pop() for i in rand_indexes]

        #Replaces dummy instrument with random cusips from list of 300
        instrument_iter = 1
        while instrument_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="SecurityID" id="48">dummy_instrument</field>' in line:
                    line = line.replace('<field name="SecurityID" id="48">dummy_instrument</field>', f'<field name="SecurityID" id="48">{cusips[instrument_iter]}</field>')
                    instrument_iter += 1
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

        side_iter = 0
        while side_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="Side" id="54">0</field>' in line:
                    line = line.replace('<field name="Side" id="54">0</field>', f'<field name="Side" id="54">{side[side_iter]}</field>')
                    side_iter += 1
                else:
                    pass

                sys.stdout.write(line)


        ##### attempt to allow user to specify how many orders have limits -- NOT FINISHED
        # if add_limits != 'No':
        #     if add_limits == '100%':
        #         list_lim = int(num_in_list)
        #     elif add_limits == '75%':
        #         list_lim = 0.75 * int(num_in_list)
        #     elif add_limits == '50%':
        #         list_lim = 0.5 * int(num_in_list)
        #     elif add_limits == '25%':
        #         list_lim = 0.25 * int(num_in_list)
            
        #     whole_list_lim = int(list_lim)

        #     rand_limits = []
        #     while len(rand_limits) < whole_list_lim:
        #         rand_limit = round(random.uniform(0, 200), 3)
        #         rand_limits.append(rand_limit)
            
        #     print(rand_limits)

        #     limit_iter = 0
        #     while limit_iter < len(rand_limits)-1:
        #         for line in fileinput.input(file_name, inplace=1):
        #             if '<field name="Price" id="44">0</field>' in line:
        #                 line = line.replace('<field name="Price" id="44">0</field>', f'<field name="Price" id="44">{rand_limits[limit_iter]}</field>')
        #                 limit_iter += 1
        #             else:
        #                 pass

        #             sys.stdout.write(line)
        # else:
        #     pass

        ##### This section adds random limits between 0-200 with decimal places for order

        if add_limits == 'Yes':
            rand_limits = []
            while len(rand_limits) < int(num_in_list):
                rand_limit = round(random.uniform(0, 100), 3)
                rand_limits.append(rand_limit)

            limit_iter = 1
            while limit_iter < int(num_in_list) :
                for line in fileinput.input(file_name, inplace=1):
                    if '<field name="Price" id="44">0</field>' in line:
                        line = line.replace('<field name="Price" id="44">0</field>', f'<field name="Price" id="44">{rand_limits[limit_iter]}</field>')
                        limit_iter += 1
                    else:
                        pass

                    sys.stdout.write(line)
        else:
            pass

window.close()