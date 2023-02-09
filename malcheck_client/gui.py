import re
import time
import ctypes
import PySimpleGUI as sg
from unidecode import unidecode

icon_ = b'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'


#  Styles:
#  0 : OK
#  1 : OK | Cancel
#  2 : Abort | Retry | Ignore
#  3 : Yes | No | Cancel
#  4 : Yes | No
#  5 : Retry | Cancel
#  6 : Cancel | Try Again | Continue
def message_box(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def form_validate(values):
    try:
        input_name = values["full_name"]
        input_id = values["user_id"]
        if len(input_name) == 0 or len(input_id) == 0:
            return False
        if len(input_id) != 6:
            return False
        if not input_name.replace(" ", "").isalpha():
            return False
        if not input_id.isnumeric():
            return False
    except Exception as ex:
        return False
    return True


def main_gui():
    sg.theme("SystemDefaultForReal")
    title_ = "MalCheck Client"
    menu_ = [['&File', ['&Exit']], ['&Help', ['&About']], ]
    choices_ = ['HN-T02', 'HN-T04', 'HN-T10', 'HN-T17', 'HN-T19', 'HN-T20', 'HN-T21', 'HN-T22', 'SG-04', 'SG-05', 'SG-06', 'SG-M']
    layout_ = [
        [sg.Menubar(menu_, pad=(0, 0), k='-MENUBAR-')],
        [sg.Text('Please enter your Name, Id, Address')],
        [sg.Text('Name', size=(15, 1)), sg.InputText(key='full_name')],
        [sg.Text('Id', size=(15, 1)), sg.InputText(key='user_id')],
        [sg.Text('Address', size=(15, 1)), sg.Combo(choices_, default_value=choices_[0], key='address', size=43, readonly=True)],
        [sg.Submit(), sg.Cancel()],
        [sg.ProgressBar(100, 'h', size=(30, 20), k='pbar', expand_x=True)]
    ]
    window = sg.Window(title_, layout_, icon=icon_)
    while True:
        event, values = window.read()
        if event == "About":
            window.disappear()
            message_box("About", "MalCheck Client v1.0.0", 0)
            window.reappear()
        if event in (sg.WIN_CLOSED, "Cancel", "Exit"):
            break
        if event == "Submit":
            progress_bar = window['pbar']
            if form_validate(values):
                for i in range(1000):
                    window.read(timeout=0)
                    progress_bar.update_bar(i + 1, 1000)
                sg.popup('Result', 'Name: ' + unidecode(values['full_name'].title()) + '\nId: ' + values['user_id'] + '\nAddress: ' + values['address'])
            else:
                message_box("Oops!", "Something wrong!", 0)
    window.close()
