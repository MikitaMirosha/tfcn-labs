import serial
import sys
from appJar import gui

def read():
    bitStr = a.getEntry("Input")
    a.clearTextArea("Status")
    a.setTextArea("Status", "Flag: 01110011\n")
    isValid = True
    for look in bitStr:
        if look != '0' and look != '1':
            isValid = False
            a.setValidationEntry("Input", state="invalid")
            return
    if isValid:
        a.setValidationEntry("Input", state="valid")
        bitStr = bitStr.replace("0111001", "01110010")
        a.setTextArea("Status", bitStr, callFunction = False)
        index = bitStr.find("01110010") + 3
        while index != 2:
            a.textAreaApplyFontRange("Status", "underline", "2." + str(index + 4), "2." + str(index + 5))
            index = bitStr.find("01110010", index) + 3

def write():
    a.clearTextArea("Output")
    bitStr = a.getTextArea("Status")
    bitStr = bitStr[15:len(bitStr)]
    bitStr = bitStr.replace("01110010", "0111001")
    a.setTextArea("Output", bitStr, end = False, callFunction = False)

def graphics():
    a.setResizable(False)
    a.addLabel("Input", "Input:")
    a.addValidationEntry("Input")
    a.setValidationEntryLabelBg("Input","white")

    a.addLabel("Output", "Output:")
    a.addTextArea("Output")
    a.setTextAreaHeights("Output", 4)
    a.disableTextArea("Output")
    a.setTextAreaFont("Output", size=15, family="Calibri")
    a.setTextAreaBg("Output", "white")

    a.addLabel("Status", "Status:")
    a.addTextArea("Status")
    a.setTextAreaHeights("Status", 4)
    a.disableTextArea("Status")
    a.setTextAreaFont("Status", size=15, family="Calibri")
    a.setTextAreaBg("Status", "white")

    read()

    a.enableEnter(keyPress)
    a.go()

def keyPress(key):
    read()
    write()

a = gui("Bit Stuffing Application", "500x500")

a.setBg("lightgrey")
graphics()
