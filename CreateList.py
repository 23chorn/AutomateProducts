from audioop import add
import os
import shutil
import fileinput
import sys
import csv
import random
from turtle import right
import PySimpleGUI as sg


def create_new_list_file(num_in_list, market_segment, side, file_size, with_limits, cust_dest):
    """uses template to create new xml file with name relating to number of items in list + the market segment"""
    src_dir = os.getcwd()
    if cust_dest == "":
        if layout == "Custom":
            dest_dir = src_dir + f"\\lists\\Custom"
        elif which_env == "QA":
            dest_dir = src_dir + f"\\lists\\QA"
        elif which_env == "STG":
            dest_dir = src_dir + f"\\lists\\STG"
    else:
        dest_dir = cust_dest

    if with_limits == "Yes":
        with_limits = "_Limits"
    else:
        with_limits = ""


    src_file = os.path.join(src_dir, "templates\\template.xml")
    shutil.copy(src_file, dest_dir)

    dest_file = os.path.join(dest_dir, "template.xml")
    new_dest_file_name = os.path.join(
        dest_dir,
        f"List_Orders{num_in_list}_Size{file_size}_{market_segment}_{side}{with_limits}.xml",
    )

    # os.rename(dest_file, new_dest_file_name)
    # Checks if name already exists, if it does name increments + 1 until available
    while True:
        if os.path.exists(new_dest_file_name) == False:
            os.rename(dest_file, new_dest_file_name)
            break
        else:
            for i in range(2, 1000):
                new_dest_file_name = os.path.join(
                    dest_dir,
                    f"List_Orders{num_in_list}_Size{file_size}_{market_segment}_{side}{with_limits}_v{i}.xml",
                )
                if os.path.exists(new_dest_file_name) == False:
                    break

    return new_dest_file_name


##### Set up on GUI for user to select parameters ######

# sg.theme("DarkTeal12")
sg.ChangeLookAndFeel('BlueMono')
font = ('Roboto, 12')

layout1 = [
    [
        sg.Text("Choose the environment:", font=font),
        sg.Combo(["QA", "STG"], default_value="QA", key="-ENV-", font=font),
    ],
    [
        sg.Text("Choose the market segment:", font=font),
        sg.Combo(
            [
                "HG",
                "HY",
                "EM",
                "AG",
                "USPortfolio",
                "EUPortfolio",
                "LoanPortfolio",
                "EUPrice",
                "EUGov",
                "EUHY",
                "JPY",
                "EUNonCore",
                "EMLocal",
                "EMLocalAsia",
                "CNY",
            ],
            default_value="HG",
            key="-MS-",
            size=(12),
            font=font,
        ),
    ],
    [
        sg.Text("How many items in the list?", font=font),
        sg.InputText("10", key="-NUMBER-", size=(6), font=font),
    ],
    [
        sg.Text("Choose the side of the list:", font=font),
        sg.Combo(
            ["Buy", "Sell", "Both"], default_value="Buy", key="-SIDE-", font=font
        ),
    ],
    [
        sg.Text("Size of the orders? (000s)", font=font),
        sg.Combo(
            ["1", "100", "1000", "5000", "10000", "Random"], default_value="1000", key="-SIZE-", font=font
        )
    ],
    [
        sg.Text("Add random limits for orders?", font=font),
        sg.Combo(["Yes", "No"], default_value="No", key="-LIMIT-", font=font),
    ],
    [
        sg.Text(
            "Choose an output folder (Default = FIXListCreator/lists):", font=font
        )
    ],
    [sg.Input(key="-IN2-"), sg.FolderBrowse(key="-DEST-", font=font)],
    [sg.Text(size=(80), key="-OUTPUT-")],
]

layout2 = [
    [sg.Text("Custom Instrument Source (.csv):", font=font)],
    [sg.InputText(), sg.FileBrowse(key="-SOURCECUST-", font=font)],
    [
        sg.Text("How many items in the list?", font=font),
        sg.InputText("10", key="-NUMBERCUST-", size=(6), font=font),
    ],
    [
        sg.Text("Choose the side of the list", font=font),
        sg.Combo(
            ["Buy", "Sell", "Both"], default_value="Buy", key="-SIDECUST-", font=font
        ),
    ],
    [
        sg.Text("Size of the orders? (000s)", font=font),
        sg.Combo(
            ["1", "100", "1000", "5000", "10000", "Random"], default_value="1000", key="-SIZECUST-", font=font
        )
    ],
    [
        sg.Text("Add random limits for orders?", font=font),
        sg.Combo(["Yes", "No"], default_value="No", key="-LIMITCUST-", font=font),
    ],
    [
        sg.Text(
            "Choose an output folder (Default = FIXListCreator/lists):", font=font
        )
    ],
    [sg.Input(key="-IN2-"), sg.FolderBrowse(key="-DESTCUST-", font=font)],
    [sg.Text(size=(80), key="-OUTPUTCUST-")],
]

layout = [
    [
        sg.Text(
            "Create a FIX List Template",
            size=(40, 1),
            font="Roboto, 20",
            justification="center",
        ),
        sg.Push(),
        sg.Button("Help", font=font),
    ],
    [
        sg.Text(
            "First, choose the source of instruments:",
            font=font,
        )
    ],
    [sg.Button("Default", font="Arial"), sg.Button("Custom", font=font)],
    [
        sg.Column(layout1, key="-COLDefault-"),
        sg.Column(layout2, visible=False, key="-COLCustom-"),
    ],
    [
        sg.Button("Create", font=font),
        sg.Button("Exit", font=font),
        sg.Push(),
        sg.Text("v1.1", font='Roboto, 8'),
    ],
]

window = sg.Window("FIX List Creator", layout)
layout = "Default"

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    elif event in "DefaultCustom":
        window[f"-COL{layout}-"].update(visible=False)
        layout = event
        window[f"-COL{layout}-"].update(visible=True)
    elif event == "Help":
        sg.popup(
            "Default Instrument Source = Use list of all available CUSIPS from BL Database and picks a random selection on N based on user input\n\n\
Custom Instrument Source = User can supply their own list of instruments as the source for the template. It must be a .csv file containing a single column with a header \
followed by a list of CUSIPS. You cannot select number of items as greater than number of CUSIPS in the .csv"
        )
    elif (
        event == "Create"
    ):  # If user clicks Create button the 5 variables below are populated and used in rest of code
        if layout == "Default":
            window["-OUTPUT-"].update(
                "You have created: Orders = "
                + values["-NUMBER-"]
                + ", Mkt Sgmt = "
                + values["-MS-"]
                + ", Size = "
                + values["-SIZE-"]
                + ", Limits = "
                + values["-LIMIT-"]
                + ", "
                + values["-SIDE-"]
                + " list, for "
                + values["-ENV-"]
                + ".",
            )
            which_env = values["-ENV-"]
            num_in_list = values["-NUMBER-"]
            list_market_segment = values["-MS-"]
            buy_or_sell = values["-SIDE-"]
            size = values["-SIZE-"]
            add_limits = values["-LIMIT-"]
            user_dest = values["-DEST-"]
            user_source = values["-SOURCECUST-"]
            file_name = create_new_list_file(
                num_in_list, list_market_segment, buy_or_sell, size, add_limits, user_dest
            )
        elif layout == "Custom":
            window["-OUTPUTCUST-"].update(
                "You have created: Orders = "
                + values["-NUMBERCUST-"]
                + ", Size = "
                + values["-SIZECUST-"]
                + ", Limits = "
                + values["-LIMITCUST-"]
                + ", "
                + values["-SIDECUST-"]
                + " list, with Custom Instruments",
            )
            num_in_list = values["-NUMBERCUST-"]
            buy_or_sell = values["-SIDECUST-"]
            size = values["-SIZECUST-"]
            add_limits = values["-LIMITCUST-"]
            user_dest = values["-DESTCUST-"]
            user_source = values["-SOURCECUST-"]

            file_name = create_new_list_file(
                num_in_list, layout, buy_or_sell, size, add_limits, user_dest
            )

        ##### This section replaces the overall list count value with user input of number of list items in the template #####

        # Begins replacement of id 73 with correct number
        read_template = open(f"{file_name}", "r")

        new_list_count = ""  # string which contains basic template with id 73 replaced with number of orders in list
        for line in read_template:
            new_line = line.replace(
                '<groups name="NoOrders" id="73" count="1">',
                f'<groups name="NoOrders" id="73" count="{num_in_list}">',
            )
            new_list_count += new_line

        read_template.close()  # Closes initial version of template

        # Writes new version of file with id 73 filled correctly
        write_template = open(f"{file_name}", "w")
        write_template.write(new_list_count)
        write_template.close()

        # Second stage - replaces id 68 with number of orders in list
        read_template1 = open(f"{file_name}", "r")

        new_list_count1 = ""  # string which contains basic template with id 68 replaced with number of orders in list
        for line in read_template1:
            new_line1 = line.replace(
                '<field name="TotNoOrders" id="68">1</field>',
                f'<field name="TotNoOrders" id="68">{num_in_list}</field>',
            )
            new_list_count1 += new_line1

        read_template1.close()  # Closes second version of template

        # Writes new version of file with id 68 and id 73 filled correctly with no. orders in list
        write_template1 = open(f"{file_name}", "w")
        write_template1.write(new_list_count1)
        write_template1.close()

        ##### This section creates an instrument group for each instrument in the list #####

        # Opens the instrument group template as the base
        if add_limits == "No":
            read_group_template = open("templates\\group_template.txt", "r")
        else:
            read_group_template = open("templates\\groupwithlimit_template.txt", "r")

        group = ""  # contents of template stored in this string
        for line in read_group_template:
            group += line

        group_newline = (
            f"{group}\n"  # adds a new line to separate each instrument group correctly
        )
        multiple_groups = group_newline * (
            int(num_in_list) - 1
        )  # Create correct number of instrument groups based on no. orders in list
        read_group_template.close()

        append_groups_file = open(f"{file_name}", "a+")
        append_groups_file.write(
            multiple_groups
        )  # add N instrument group sections to the template with id 68 and id 73 filled
        append_groups_file.close()

        ##### This section appends tail of file to new list xml #####

        read_end_template = open("templates\\end_template.txt", "r")
        append_end_file = open(f"{file_name}", "a+")

        append_end_file.write(read_end_template.read())

        read_end_template.close()
        append_end_file.close()

        ##### This section replaces the list seq no. to increment for each order in list #####

        # Increments each subsequent id 67 with number up to total size of list to comply with correct numbering of items in list

        seq_iter = 1
        while seq_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="ListSeqNo" id="67">0</field>' in line:
                    line = line.replace(
                        '<field name="ListSeqNo" id="67">0</field>',
                        f'<field name="ListSeqNo" id="67">{seq_iter}</field>',
                    )
                    seq_iter += 1
                else:
                    pass

                sys.stdout.write(line)

        ##### This section chooses which instrument file to look at based on environment/mktsegment selected by user and uses it as the source for filling each insrument
        # group with a random CUSIP #####

        def instrument_src(environment, mktseg):
            instruments = open(f"instruments\\{environment}\\{mktseg}.csv", "r")
            return instruments

        if user_source == "":
            user_mktseg = instrument_src(which_env, list_market_segment)
            csv_reader = csv.reader(user_mktseg)
        else:
            user_instruments = open(user_source, "r")
            csv_reader = csv.reader(user_instruments)

        # adds all cusips from instruments csv into a list
        lists_from_csv = list(csv_reader)

        # Generate random set of unique indexes to pick unique instruments from csv
        rand_indexes = []
        while len(rand_indexes) < (int(num_in_list) + 1):
            rand_index = random.randint(0, len(lists_from_csv) - 1)
            if rand_index not in rand_indexes:
                rand_indexes.append(rand_index)
            else:
                pass

        # Create list of random cusips from csv file
        cusips = [lists_from_csv[i].pop() for i in rand_indexes]

        instrument_iter = 1
        while instrument_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="SecurityID" id="48">dummy_instrument</field>' in line:
                    line = line.replace(
                        '<field name="SecurityID" id="48">dummy_instrument</field>',
                        f'<field name="SecurityID" id="48">{cusips[instrument_iter]}</field>',
                    )
                    instrument_iter += 1
                else:
                    pass

                sys.stdout.write(line)

        ##### This section creates a list of buy/sell or a random mix of both sides and populates field with id=54 appropriately
        side = []

        if buy_or_sell == "Buy":
            buy = 1
            side.append(buy)
            side *= int(num_in_list)
        elif buy_or_sell == "Sell":
            sell = 2
            side.append(sell)
            side *= int(num_in_list)
        elif buy_or_sell == "Both":
            for i in range(1, int(num_in_list) + 1):
                n = random.randint(1, 2)
                side.append(n)
                i += 1

        side_iter = 0
        while side_iter < int(num_in_list):
            for line in fileinput.input(file_name, inplace=1):
                if '<field name="Side" id="54">0</field>' in line:
                    line = line.replace(
                        '<field name="Side" id="54">0</field>',
                        f'<field name="Side" id="54">{side[side_iter]}</field>',
                    )
                    side_iter += 1
                else:
                    pass

                sys.stdout.write(line)

        ##### This section creates a list of sizes based on the user selection (specified or random) and populates field with id=38 appropriately
        def fill_sizes(list_size):
            size_iter = 0
            while size_iter < int(num_in_list):
                for line in fileinput.input(file_name, inplace=1):
                    if '<field name="OrderQty" id="38">1000000</field>' in line:
                        line = line.replace(
                            '<field name="OrderQty" id="38">1000000</field>',
                            f'<field name="OrderQty" id="38">{list_size[size_iter]}</field>',
                        )
                        size_iter += 1
                    else:
                        pass

                    sys.stdout.write(line)


        def createSizeArray(user_size):
            order_sizes = []
            order_sizes.append(user_size)
            order_sizes *= int(num_in_list)
            return order_sizes

        if size == 'Random':
            order_sizes = []
            while len(order_sizes) < int(num_in_list):
                rand_size = round(random.uniform(100, 1500))
                order_sizes.append(rand_size)
            fill_sizes(order_sizes)
        elif size == '1':
            order_sizes = createSizeArray(1000)
            fill_sizes(order_sizes)
        elif size == '100':
            order_sizes = createSizeArray(100000)
            fill_sizes(order_sizes)
        elif size == '5000':
            order_sizes = createSizeArray(5000000)
            fill_sizes(order_sizes)
        elif size == '10000':
            order_sizes = createSizeArray(10000000)
            fill_sizes(order_sizes)
        else:
            pass

        ##### This section adds random limits between 0-100 with decimal places for order

        if add_limits == "Yes":
            rand_limits = []
            while len(rand_limits) < int(num_in_list):
                rand_limit = round(random.uniform(0, 100), 3)
                rand_limits.append(rand_limit)

            limit_iter = 1
            while limit_iter < int(num_in_list):
                for line in fileinput.input(file_name, inplace=1):
                    if '<field name="Price" id="44">0</field>' in line:
                        line = line.replace(
                            '<field name="Price" id="44">0</field>',
                            f'<field name="Price" id="44">{rand_limits[limit_iter]}</field>',
                        )
                        limit_iter += 1
                    else:
                        pass

                    sys.stdout.write(line)
        else:
            pass

window.close()