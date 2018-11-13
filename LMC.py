#Little Man Computer

from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askinteger

def openfile():
    try:
        with open(askopenfilename(), "r") as file:
            file = file.read().replace("    ", " ").split("\n")
        array = ["" for x in range(100)]
        with open("array.txt", "r") as inputs:
            inputs = inputs.read().replace(",", " ").replace("    ", " ").split("\n")
            for item in range(len(inputs)):
                inputs[item] = inputs[item].split(" ")
                array[int(inputs[item][0])] = inputs[item][1]
            for item in range(len(array)):
                if array[item] == '':
                    array[item] = "000"
                if len(array[item]) < 3:
                    array[item] = ("0" * (3 - len(array[item]))) + array[item]
                elif len(array[item]) > 3:
                    raise Exception("Your array contains a value of length >3. Please check array.txt.")
            if len(array) != 100:
                array = array + ["000" for x in range(100 - len(array))]
        print(file)
    except:
        showerror("ERROR.", "Invalid file address.")
        raise Exception("This file is invalid. Program terminated.")
    return file, array

def init(file, array):
    def readline(line):            
        line.replace(" ", "")
        line = line.upper()
        if "INP" in line:
            num = "901"
        elif "OUT" in line:
            num = "902"
        elif "OTC" in line:
            num = "903"
        elif "HLT" in line:
            num = "000"
        elif line == "":
            return True, ""
        else:
            if "ADD" in line:
                num = "1"
                code = "ADD"
            elif "SUB" in line:
                num = "2"
                code = "SUB"
            elif "STA" in line:
                num = "3"
                code = "STA"
            elif "LDA" in line:
                num = "5"
                code = "LDA"
            elif "BRA" in line:
                num = "6"
                code = "BRA"
            elif "BRZ" in line:
                num = "7"
                code = "BRZ"
            elif "BRP" in line:
                num = "8"
                code = "BRP"
            elif "DAT" in line:
                num = ""
                code = "DAT"
            else:
                return True, "ERROR"
            line = line.replace(" ", "").replace(code, "") #eval('"' + code + '"')
            if code != "DAT":
                if len(line) != 2:
                    if len(line) == 1:
                        num = num + "0" + line
                    else:
                        raise Exception("This is not right. Check your code.")
                else:
                    num += line
        return False, num

    for line in range(len(file)):
        error, num = readline(file[line])
        if not error:
            array[line] = num
        else:
            if line == "ERROR":
                raise Exception("Line", array.index(line), "is invalid. Please change your code.")
            else:
                continue
    return array

def LMC(array):
    def add(intval, flag, acc):
        acc = int(acc)
        acc += int(array[int(intval)])
        if acc > 1000 and flag:
            flag = False
            acc -= 1000
        return acc, flag

    def subtract(intval, flag, acc):
        acc = int(acc)
        acc -= int(array[int(intval)])
        if acc < 0 and not flag:
            flag = True
            acc += 1000
        return acc, flag

    def store(intval, array, acc):
        array[intval] = ("0" * (3 - len(str(acc)))) + str(acc)
        return array

    def load(intval):
        return array[int(intval)]

    def brancha(intval):
        return int(intval) - 1

    def branchz(intval, pc):
        if acc == 0:
            return int(intval) - 1
        else:
            return pc + 1

    def branchp(intval, pc, flag):
        if not flag:
            return int(intval)
        else:
            return pc + 1
    
    pc = 0
    acc = 0
    cir = 'INIT'
    flag = False

    while cir != '000':
        cir = array[pc]
        print(cir)
        if cir[0] == "0":
            if cir == '000':
                quit()
            else:
                pc += 1
        elif cir[0] == "1":
            acc, flag = add(int(cir[1:]), flag, acc)
            pc += 1
        elif cir[0] == "2":
            acc, flag = subtract(int(cir[1:]), flag, acc)
            pc += 1
        elif cir[0] == "3":
            array = store(int(cir[1:]), array, acc)
            pc += 1
        elif cir[0] == "5":
            acc = load(int(cir[1:]))
            pc += 1
        elif cir[0] == "6":
            pc = brancha(int(cir[1:]))
        elif cir[0] == "7":
            pc = branchz(int(cir[1:]), pc)
        elif cir[0] == "8":
            pc = branchp(int(cir[1:]), pc, flag)
        elif cir[0] == "9":
            if cir == '901':
                acc = askinteger("Input", "Please enter a integer")
                pc += 1
            elif cir == '902':
                showinfo("Output", str(acc))
                print(acc)
                pc += 1
            elif cir == '903':
                showinfo("Output", chr(int(acc)))
                pc += 1
            else:
                pc += 1 # 904-999 (data)
        else:
            pc += 1
        


#Initialise
file, array = openfile()

array = init(file, array)

#Main
LMC(array)