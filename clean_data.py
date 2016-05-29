import csv

MAX_NORM = 1
MIN_NORM = 0
MAX = "max"
MIN = "min"

def first_process(filename, newfile, use_columns, col_dict):
	with open(filename, 'rb') as csv_read, open(newfile, 'wb') as csv_write:
		row_count = 0
		data_reader = csv.reader(csv_read, delimiter=',')
		data_writer = csv.writer(csv_write, delimiter=',')
		for row in data_reader:
			valid_row = True
			row_to_write = []
			for column in use_columns:
				if not row[column] or row[column] == "nan":
					valid_row = False
					break
				else:
					col_val = float(row[column])
					row_to_write.append(col_val)
					row_count += 1
					if col_val > col_dict[column][MAX]:
						col_dict[column][MAX] = col_val
					if col_val < col_dict[column][MIN]:
						col_dict[column][MIN] = col_val
			if valid_row:
				data_writer.writerow(row_to_write)
	print col_dict
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
				normed = (col_val-col_dict[col_name][MIN])/(col_dict[col_name][MAX]-col_dict[col_name][MIN])
				normalized_row.append(normed)
			data_writer.writerow([row_id] + normalized_row)
			data.append([row_id] + normalized_row)
	return data

def clean(files, lastfile, use_columns, folder=None):
	col_dict= setup(use_columns)
	row_count = 0
	row_breaks = [0]
	newfiles = []
	for i, filename in enumerate(files):
		if folder:
			newfile = folder + "intermediate_" + str(i) + ".csv"
		else:
			newfile = "intermediate_" + str(i) + ".csv"
		newfiles.append(newfile)
		rows = first_process(filename, newfile, use_columns, col_dict)
		row_count += rows
		row_breaks.append(rows)

	for i, newfile in enumerate(newfiles):
		start_id = row_breaks[i]
		data = second_process(newfile, lastfile, use_columns, col_dict, start_id=start_id)
	print(row_count)
	return data
