
################################################################
############    MIPS Disassembler/Assembler Demo    ############
################################################################
#...... Supported instructions Q1: addi, andi, sub  ............
#.......Supported instructions Q2: addi, j......................
#.......Hex values are not supported ...........................S
#.......Does not detect invalid assembly code................... 
#.......Only supports jump to label + instr in a same line......
#.......Ex-> label: addi $22, $8, 88............................

#dictionary for easier conversion funct/opcode to name of instruction... more instruction to be added
functions = {}
functions["100010"] = "sub"
functions["001100"] = "andi"
functions["001000"] = "addi"

#for conversion, large values to be displayed in hex format
# the value 255 is not fixed feel free to change it to any other value
def large_val_limiter(strVal):
    if(strVal>255):
        strVal = hex(strVal)
    return str(strVal)

#twos_complement
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)        
    return val                 

#hex to binary conversion function
def hex_to_bin(instr):
    integer = int(instr, 16)
    binary = '{:032b}'.format(integer)
    return binary
#binary to hex conversion
def bin_to_hex(instr):
    integer = int(instr,2)
    hexadecimal = hex(integer).replace("0x","")
    hexadecimal="0x"+hexadecimal.zfill(8)
    return hexadecimal

#saves the labels 
def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
        lineCount += 1

#error checker for hex input in mode 1
def formatChecker(instr):
    checker = False
    if any(c>'f' for c in instr):
        print("Illegal characters")
    if not instr.isalnum():
        print("Special characters are not allowed")
    elif len(instr)!=8:
        print("Hex instruction must contain 8 characters")
    else:
        checker = True
    return checker

#disassembler function
def dissasembler(instr, functions): #supports addi, andi and sub
    if(instr[0:6]=="000000"):
        rs = instr[6:11] 
        rt= instr[11:16]
        rd= instr[16:21]
        func = instr[26:32]
        assembly = functions[func] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
    elif(instr[0:6]=="000010"):
        print("The instruction is of J-type")
        # code not finished for J type
    else:
        func = instr[0:6]
        rs = instr[6:11]
        rt = instr[11:16]
        imm = twos_comp(int(instr[16:32],2), 16)
        imm = large_val_limiter(imm)
        assembly = functions[func] + " $" + str(int(rt,2)) + ", $" + str(int(rs, 2)) + ", " + imm
    
    #keep adding more instructions

    return assembly

#assembler function
def assembler(dataFile, labelName, labelIndex, w): #supports addi and j
    for line in dataFile:
        line = line.replace("\n", "") # Removes extra chars 
        line = line.replace("$", "")    # Removes extra chars
        line = line.replace(" ", "")    # Removes extra chars
        line = line.replace("zero", "0")  #can use both $zero and $0
        
        if (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b') #if negative value add + 2^16 + value
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "001000" + str(rs) + str(rt) + str(imm)
            w.write(bin_to_hex(binary) + "\n")
        
        elif(line[0:1]=='j'): #Jump
            line = line.replace("j", "")
            line = line.split(",")
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if (line[0].isdigit()):  # First,test to see if it's a label or an immediate (this won't support labels like ex: 1loop or 2exit)
                binary = '000010' + str(format(int(line[0]) ,'026b'))
                w.write(bin_to_hex(binary) + "\n")
            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        binary = '000010' + str(format(int(labelIndex[i]), '026b'))
                        w.write(bin_to_hex(binary) + '\n')
            
            #keep adding more instructions

###############################################################################################
#Main

print("********************************")
print("         ECE 366 HW3            ")
print("********************************")

mode = int(input("Press 1 to run the demo for Q1\nPress 2 to run the demo for Q2\n>"))
if(mode==1):
    print("********************************")
    print("       MIPS DISASSEBMLER        ")
    print("********************************")
    print("To exit enter #...")
    while(True):
        instr = input("Enter instruction in hex: 0x")
        instr = instr.lower()
        if(instr=="#"):
            exit()
        if(formatChecker(instr)):
            binIstr = hex_to_bin(instr)
            out = dissasembler(binIstr, functions)
            print(out)
            print("------------------------------")

if(mode==2):
    print("********************************")
    print("         MIPS ASSEMBLER         ")
    print("********************************")
    r = open("readfile.asm" , "r")
    w = open("writefile.txt", "w+")
    labelIndex = []
    labelName = []

    dataFile = r.readlines()
    for data in range(dataFile.count('\n')):
        dataFile.remove("\n")
    
    saveJumpLabel(dataFile, labelIndex, labelName)
    
    print("Translating MIPS assembly to machine code in hex...")
    assembler(dataFile,labelName,labelIndex,w)
    print("Translation finished.\nMachine code saved as writefile.txt")


    
