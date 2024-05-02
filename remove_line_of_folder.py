def remove_lines(file_path, num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    new_lines = lines[num:]

    with open(file_path, 'w') as file:
        file.writelines(new_lines)


#path = '../FN_new/FNGasCount.log'

lineToRemove = 40000

remove_lines(path, lineToRemove)