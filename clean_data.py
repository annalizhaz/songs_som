import csv
import string


MAX_NORM = 1
MIN_NORM = 0
MAX = "max"
MIN = "min"
LABELS = []

def column_to_number(alpha_column):
    '''
    Takes column labels as they are in excel(i.e., "A", "AB", etc.) an translates 
    them to the corresponding number
    '''

    #add exception for incorrect value types given for columns

    column_label = list(alpha_column)

    num = 0

    for letter in alpha_column:
        if letter in string.ascii_letters:
            num = num * 26 + (ord(letter.upper()) - ord("A"))+1

    return num-1

def first_process(filename, newfile, use_columns, col_dict):
    with open(filename, 'rb') as csv_read, open(newfile, 'wb') as csv_write:
        row_count = 0
        data_reader = csv.reader(csv_read, delimiter=',')
        data_writer = csv.writer(csv_write, delimiter=',')
        for row in data_reader:
            valid_row = True
            row_to_write = []
            for column in use_columns:
                if (column == 2 and row[column] == '0') or not row[column] or row[column] == "nan":
                    valid_row = False
                    break
                else:
                    col_val = float(row[column])
                    row_to_write.append(col_val)
                    if col_val > col_dict[column][MAX]:
                        col_dict[column][MAX] = col_val
                    if col_val < col_dict[column][MIN]:
                        col_dict[column][MIN] = col_val
            if valid_row:
                row_count += 1
                data_writer.writerow(row_to_write)
                LABELS.append((row_count, row[0], row[1], row[2]))
    return row_count

def setup(use_columns):
    col_dict = {}
    for column in use_columns:
        col_dict[column] = {MAX: 0, MIN: float("inf")}
    return col_dict

def second_process(newfile, lastfile, use_columns, col_dict, start_id = 0):
    data = []
    with open(newfile, 'rb') as csv_read, open(lastfile, 'wb') as csv_write:
        data_reader = csv.reader(csv_read, delimiter=',')
        data_writer = csv.writer(csv_write, delimiter=',')
        row_id = start_id
        for row in data_reader:
            row_id += 1
            normalized_row = []
            for i, column in enumerate(row):
                col_val = float(column)
                col_name = use_columns[i]
                if col_dict[col_name][MAX] == col_dict[col_name][MIN]:
                    print("No variation in column %s", col_name)
                    normed = 0
                else:
                    normed = (col_val-col_dict[col_name][MIN])/(col_dict[col_name][MAX]-col_dict[col_name][MIN])
                normalized_row.append(normed)
            data_writer.writerow([row_id] + normalized_row)
            data.append([row_id] + normalized_row)
    return data

def clean(files, final_file, use_columns, folder=None):
    col_dict= setup(use_columns)
    row_count = 0
    row_breaks = [0]
    newfiles = []
    data = []
    for i, filename in enumerate(files):
        if folder:
            newfile = folder + "intermediate_" + str(i) + ".csv"
        else:
            newfile = "intermediate_" + str(i) + ".csv"
        newfiles.append(newfile)
        rows = first_process(filename, newfile, use_columns, col_dict)
        row_count += rows
        row_breaks.append(row_count)

    print(row_breaks)

    for i, newfile in enumerate(newfiles):
        if folder:
            lastfile = folder + "final_" + str(i) + ".csv"
        else:
            lastfile = "final_" + str(i) + ".csv"
        start_id = row_breaks[i]
        new_data = second_process(newfile, lastfile, use_columns, col_dict, start_id=start_id)
        data = data + new_data

    with open(final_file, 'wb') as csv_write:
        data_writer = csv.writer(csv_write, delimiter=',')
        for row in data:
            data_writer.writerow(row)
    print(row_count)
    return data, LABELS
