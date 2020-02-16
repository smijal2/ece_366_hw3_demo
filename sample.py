
################################################################
############    MIPS Disassembler/Assembler Demo    ############
################################################################
#...... Supported instructions: sub, andi, addi and j...........
#.......Hex values are not supported ...........................
#.......Does not detect invalid assembly code................... 

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

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)        
    return val                 

#hex to binary conversion function
def hex_to_bin(instr):
    integer = int(instr, 16)
    binary = '{:032b}'.format(integer)
    return binary

def bin_to_hex(instr):
    integer = int(instr,2)
    hexadecimal = hex(integer).replace("0x","")
    hexadecimal="0x"+hexadecimal.zfill(8)
    return hexadecimal

def saveJumpLabel(asm, labelIndex, labelName):
    lineCount = 0
    for line in asm:
        line = line.replace(" ", "")
        if (line.count(":")):
            labelName.append(line[0:line.index(":")])  # append the label name
            labelIndex.append(lineCount)  # append the label's index
            asm[lineCount] = line[line.index(":") + 1:]
        lineCount += 1

#dissasembler function
def dissasembler(instr, functions):
    if(instr[0:6]=="000000"):
        print("The instruction is of R-type")
        rs = instr[6:11] 
        rt= instr[11:16]
        rd= instr[16:21]
        func = instr[26:32]
        assembly = functions[func] + " $" + str(int(rd,2)) + ", $"+str(int(rs,2)) + ", $" + str(int(rt,2))
    elif(instr[0:6]=="000010"):
        print("The instruction is of J-type")
    else:
        print("The instruction is of I-type")
        func = instr[0:6]
        rs = instr[6:11]
        rt = instr[11:16]
        imm = twos_comp(int(instr[16:32],2), 16)
        imm = large_val_limiter(imm)
        assembly = functions[func] + " $" + str(int(rt,2)) + ", $" + str(int(rs, 2)) + ", " + imm

    return assembly


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
    while(True):
        instr = input("\nEnter instruction in hex: 0x")
        instr = instr.lower()
        if(instr=="#"):
            break
        if any(c>'f' for c in instr):
            print("Illegal characters")
        if not instr.isalnum():
            print("Special characters are not allowed")
        elif len(instr)!=8:
            print("Hex instruction must contain 8 characters")
        else:
            binIstr = hex_to_bin(instr)
            out = dissasembler(binIstr, functions)
            print(out)
if(mode==2):
    print("********************************")
    print("         MIPS ASSEBMLER         ")
    print("********************************")
    r = open("readfile.asm" , "r")
    w = open("writefile.txt", "w+")
    print("Translating MIPS assembly to machine code in hex...")
    labelIndex = []
    labelName = []

    dataFile = r.readlines()
    for data in range(dataFile.count('\n')):
        dataFile.remove("\n")
    
    saveJumpLabel(dataFile, labelIndex, labelName)

    for line in dataFile:
        line = line.replace("\n", "")  # Removes extra chars
        line = line.replace("$", "")
        line = line.replace(" ", "")
        line = line.replace("zero", "0")  # assembly can also use both $zero and $0
        
        if (line[0:4] == "addi"):  # ADDI
            line = line.replace("addi", "")
            line = line.split(",")
            imm = format(int(line[2]), '016b') if (int(line[2]) >= 0) else format(65536 + int(line[2]), '016b') #if negative value add + 2^16 + value
            rs = format(int(line[1]), '05b')
            rt = format(int(line[0]), '05b')
            binary = "001000" + str(rs) + str(rt) + str(imm)
            w.write(bin_to_hex(binary) + "\n")
        
        elif(line[0:1]=='j'):
            line = line.replace("j", "")
            line = line.split(",")
            # Since jump instruction has 2 options:
            # 1) jump to a label
            # 2) jump to a target (integer)
            # We need to save the label destination and its target location
            if (line[0].isdigit()):  # First,test to see if it's a label or an integer (this won't support labels like ex: 1loop or 2exit)
                binary = '000010' + str(format(int(line[0]) ,'026b'))
                w.write(bin_to_hex(binary) + "\n")
            else:  # Jumping to label
                for i in range(len(labelName)):
                    if (labelName[i] == line[0]):
                        binary = '000010' + str(format(int(labelIndex[i]), '026b'))
                        w.write(bin_to_hex(binary) + '\n')
            
    print("Translation finished.\nMachine code saved as writefile.txt")


    
