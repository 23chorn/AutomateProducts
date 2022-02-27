list_mktseg = 'HG'

def instrument_src(mktseg):
    if mktseg == 'HG' :
        instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
    elif mktseg == 'HY':
        instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
    elif mktseg == 'EM':
        instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
    elif mktseg == 'AG':
        instruments = open(f'instruments\\QA\\ALL{mktseg}.csv', 'r')
    return instruments

print(instrument_src(list_mktseg))