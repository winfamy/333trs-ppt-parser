import csv

in_fname = input("Input CSV: ")
out_fname = input("Output CSV: ")
join_str = input("String to separate CSV entries with: ")

with open(in_fname, "r") as in_file:
    combined_text = ""
    csv_reader = csv.reader(in_file, delimiter="|",
                            quotechar='"', quoting=csv.QUOTE_ALL)

    with open(out_fname, "w") as out_file:
        for row in csv_reader:
            out_file.write(row[1] + join_str)
