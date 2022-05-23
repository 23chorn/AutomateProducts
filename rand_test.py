import random

# num_in_list = 10
# lists_from_csv = 20

# rand_indexes = []
# while len(rand_indexes) < (int(num_in_list) + 1):
#     rand_index = random.randint(0, lists_from_csv)
#     if rand_index not in rand_indexes:
#         rand_indexes.append(rand_index)
#     else:
#         pass

# rand_limits = []
# while len(rand_limits) < num_in_list + 1:
#     rand_limit = round(random.uniform(0, 200), 3)
#     rand_limits.append(rand_limit)

# print(rand_limits)

#Create list of random cusips from csv file
# # cusips = [i for i in rand_indexes]
# for i in rand_indexes:
#     cusips.append(lists_from_csv[i].pop())
#     i += 1

num_in_list = 10

percent_lim = input('Enter %: ')

if percent_lim == '100%':
    list_lim = int(num_in_list)
elif percent_lim == '75%':
    list_lim = 0.75 * int(num_in_list)
elif percent_lim == '50%':
    list_lim = 0.5 * int(num_in_list)
elif percent_lim == '25%':
    list_lim = 0.25 * int(num_in_list)
else:
    list_lim = 0

print(int(list_lim))

rand_limits = []
while len(rand_limits) < list_lim:
    rand_limit = round(random.uniform(0, 200), 3)
    rand_limits.append(rand_limit)

print(rand_limits)
print(len(rand_limits))

limit_iter = 0
while limit_iter < len(rand_limits):
    print(rand_limits[limit_iter])
    limit_iter += 1