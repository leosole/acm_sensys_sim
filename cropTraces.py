

with open("koln.tr", "r") as file:
    lines = file.readlines()
    for line in lines:
        temp = line.split()
        if int(temp[0]) >= 28800 and int(temp[0]) < 29401:
            with open("8am.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 32400 and int(temp[0]) < 33001:
            with open("9am.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 36000 and int(temp[0]) < 36601:
            with open("10am.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 39600 and int(temp[0]) < 40201:
            with open("11am.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 43200 and int(temp[0]) < 43801:
            with open("12am.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 46800 and int(temp[0]) < 47401:
            with open("1pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 50400 and int(temp[0]) < 51001:
            with open("2pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 54000 and int(temp[0]) < 54601:
            with open("3pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 57600 and int(temp[0]) < 58201:
            with open("4pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 61200 and int(temp[0]) < 61801:
            with open("5pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 64800 and int(temp[0]) < 65401:
            with open("6pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 68400 and int(temp[0]) < 69001:
            with open("7pm.txt", "a") as cropped:
                cropped.write(line)
        elif int(temp[0]) >= 72000 and int(temp[0]) < 72601:
            with open("8pm.txt", "a") as cropped:
                cropped.write(line)
