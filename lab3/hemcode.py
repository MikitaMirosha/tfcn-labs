#!/usr/local/bin/python
import serial
import sys
import re
from appJar import gui

class HemCode:


    def control_bits(this, bits):
        length = len(bits)
        next_cbit = 1

        while length + next_cbit + 1 > 2**next_cbit:
            next_cbit = next_cbit + 1
        return next_cbit


    def parity(this, bits, next_cbit):
        j = 0
        i = 1
        next = 0
        final_str = []
        bit_length = len(bits)
        length = len(bits) + next_cbit

        while i <= length:
            if i == 2**next:
                final_str.append('x')
                next = next + 1
            elif j < bit_length:
                final_str.append(bits[j])
                j = j + 1
            i = i + 1

        return final_str


    def eject_bits(this, incomp, parity):
        j = 1
        i = parity - 1
        use_bits = []

        while i < len(incomp):
            if j <= (parity * 2) / 2 and incomp[i] != 'x':
                use_bits.append(incomp[i])
            if j == parity * 2:
                j = 0
            j = j + 1
            i = i + 1

        return use_bits


    def make_code(this, array, ev):
        i = 0
        if ev is True:
            while i < len(array):
                if array[i] == 'x':
                    tmp = this.eject_bits(array, i + 1)
                    if this.count(tmp) % 2 == 0:
                        array[i] = '0'
                    else:
                        array[i] = '1'
                i = i + 1

        elif ev is False:
            while i < len(array):
                if array[i] == 'x':
                    tmp = this.eject_bits(array, i + 1)
                    if this.count(tmp) % 2 != 0:
                        array[i] = '0'
                    else:
                        array[i] = '1'
                i = i + 1

        return array


    def count(this, extracted):
        return extracted.count('1')


    def find_error(this, code, ev):
        i = 0
        exp = 0
        error = []

        if ev is True:
            while i < len(code):
                if i == (2**exp) - 1:
                    tmp = this.eject_bits(code, i + 1)
                    if this.count(tmp) % 2 != 0:
                        error.append(i + 1)
                    exp = exp + 1
                i = i + 1

        elif ev is False:
            while i < len(code):
                if i == (2**exp) - 1:
                    tmp = this.eject_bits(code, i + 1)
                    if this.count(tmp) % 2 == 0:
                        error.append(i + 1)
                    exp = exp + 1
                i = i + 1
        print(error)
        return error


def add_zeros(sourse):
    length = len(sourse)
    while length > 23:
        length = length - 23
    return 23 - length


ZERO_STR = "0000000000000000000000"


def write_status():
    cur_str = app.getEntry("Input")
    app.clearTextArea("Status")
    app.setTextArea("Status", "Sequence length: 23\nBin data:\n\n")
    isValid = True
    for look in cur_str:
        if look != '0' and look != '1':
            isValid = False
            app.setValidationEntry("Input", state="invalid")
            return
    if isValid:
        app.setValidationEntry("Input", state="valid")
        zeros = add_zeros(cur_str)
        cur_str += ZERO_STR[0:zeros]
        transferred = []
        out_str = re.findall(r'.{23}', cur_str)
        for i in out_str:
            obj = HemCode()
            cbits = obj.control_bits(i)
            tmp = obj.parity(i, cbits)
            app.setTextArea("Status", tmp, end=True, callFunction=True)
            app.setTextArea("Status", "\n", end=True, callFunction=True)
            ev = True
            bits_pos = "".join(obj.make_code(tmp, ev))
            bits_pos = bits_pos.replace('',' ').strip()
            app.setTextArea("Status", bits_pos + "\n\n", end=True, callFunction=True)
            transferred.append("".join(obj.make_code(tmp, ev)))


def write_output():
    app.clearTextArea("Output")
    cur_str = app.getEntry("Input")
    isValid = True
    for look in cur_str:
        if look != '0' and look != '1':
            isValid = False
            app.setValidationEntry("Input", state="invalid")
            return
    zeros = add_zeros(cur_str)
    cur_str += ZERO_STR[0:zeros]
    out_str = re.findall(r'.{23}', cur_str)
    app.setTextArea("Output", out_str, callFunction=False)


def show():
    app.setResizable(False)
    app.setBg("LightGrey")

    app.addLabel("Input", "Input:")
    app.addValidationEntry("Input")
    app.setValidationEntryLabelBg("Input","white")
    app.setEntryMaxLength("Input", 46)
    app.setFont(14)

    app.addLabel("Output", "Output:")
    app.addTextArea("Output")
    app.setTextAreaHeights("Output", 2)
    app.disableTextArea("Output")
    app.setTextAreaBg("Output", "white")
    app.setTextAreaFont("Output", size=14, family="Arial")

    app.addLabel("Status", "Status:")
    app.addTextArea("Status")
    app.setTextAreaHeights("Status", 9)
    app.disableTextArea("Status")
    app.setTextAreaBg("Status", "white")
    app.setTextAreaFont("Status", size=14, family="Arial")

    write_status()

    app.enableEnter(keyPress)
    app.go()


def keyPress(key):
    write_status()
    write_output()


if __name__ == '__main__':
    app = gui("Hemming_code", "700x500")
    show()
