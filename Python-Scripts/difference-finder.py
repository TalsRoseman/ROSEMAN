import os

#DECLERATIONS
date = input("Please enter the date in a format of DDMM: ")  # Get the date from the user
shift = input("Please enter the shift in a format of A, B, C: ")  # Get the shift from the user
amount_pump = input("Please enter the amount of pumps in the station: ")  # Get the amount of pumps in the station from the user
rs_path = "/Users/talshaubi/Documents/ROSEMAN/data/RS" + date + "24.D1" + shift  # The path to the RS file
#END OF DECLERATIONS

def pump_difference(rs_path, pump, nzl):
    tran_start = 45
    tran_end = 51
    pump_start = 38
    pump_end = 44
    nzl_start = 34
    nzl_end = 37
    money_start = 0
    money_end = 9
    start = False
    if not os.path.isfile(rs_path):
        print("File not found")
        return
    else:
        with open(rs_path, 'r', errors="ignore") as file:
            lines = file.readlines()
            reversed_lines = reversed(lines)
        for line in lines[1:]:#Sum the money starting count with all the transactions
            if (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) == nzl and line[tran_start:tran_end].replace(" ", "") == "Open" and not start): #Finds that the pump and nzl has been opened and initializes the money count
                money = float(line[money_start:money_end].replace(" ", ""))
                start = True
                continue
            elif (int(line[pump_start:pump_end].replace(" ", "")) == pump and int(line[nzl_start:nzl_end].replace(" ", "")) == nzl and line[tran_start:tran_end].replace(" ", "").isdigit() and start):# Adds the transaction amount to the total money count
                money += float(line[money_start:money_end].replace(" ", ""))
        if(not start):
            print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been opened")
            return 9999
        for reveresed_line in reversed(lines):#Loop from the end line to find the last closing counter of the pump and nzl and checks if it matches the total money count
            if (int(reveresed_line[pump_start:pump_end].replace(" ", "")) == pump and int(reveresed_line[nzl_start:nzl_end].replace(" ", "")) == nzl and reveresed_line[tran_start:tran_end].replace(" ", "") == "Close"):
                #Money comparison with a precision of 1 digits after the decimal point
                money = int(money*10)
                money = float(money)/10
                close_money_counter = float(reveresed_line[money_start:money_end].replace(" ", ""))
                close_money_counter = int(close_money_counter*10)
                close_money_counter = float(close_money_counter)/10
                if(money == close_money_counter):
                    if (money > close_money_counter):
                        return (money - close_money_counter)
                    else:
                        return (close_money_counter - money)
    print("Pump: " + str(pump) + " NZL: " + str(nzl) + " has not been closed")
    return 9999
