import ctypes
import PySimpleGUI as sg
import time
from unidecode import unidecode
import re

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


sg.theme('Reddit')   
sg.set_options(font='Lucida')

menu_def =[['&File', ['&Open', '&Save', '&Exit']],
                ['&Tool', ['Start', 'Clear Data']],
                ['&Help', ['&About']], ]
def main():
    layout = [  [sg.Menubar(menu_def, pad=(0,0), k='menubar')],
            [sg.Text('Họ Tên (VD: Nguyen Van A)')],
            [sg.InputText(key='name',size=(80,40),do_not_clear=True)],
            [sg.Text('Mã Nhân Sự (VD: 100123)')], 
            [sg.InputText(key='mns',size=(80,40), do_not_clear=True)],
            [sg.Text('Khu Vực')],
            [sg.Combo(['HN-T02','HN-T04','HN-T10','HN-T17', 'HN-T19','HN-T20','HN-T21','HN-T22','HCM-M','HCM-04','HCM-05','HCM-06'],default_value='HN-02',key='place', size=(80,40))],
            [sg.Button('Bắt đầu kiểm tra',font=('Lucida',12), key='OK'), sg.Button('Hủy',font=('Lucida',12))],
            [sg.ProgressBar(100, orientation='h', expand_x=True, size=(20, 20),  key='pbar', bar_color='red')]]
    
    window = sg.Window('MalAuto', layout, size=(400,300))

    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Hủy') or event == 'Exit':
            break
        if event == 'OK' or event == 'Start': 
            validation_result = validate(values)
            progress_bar = window['pbar']
            if not validation_result:
                for i in range(10000):
                    window.read(timeout=0)
                    progress_bar.update_bar(i+1, 10000)
                sg.popup('Check', 'Họ tên nhân sự: ' + unidecode(values['name'].title()) + '\nMã nhân sự: ' + values['mns'] + '\nKhu Vực: ' + values['place'])
            else: 
                validation_result
        # Menu choices
        if event=='About':
            window.disappear()
            sg.popup('About this program', sg.get_versions(),  grab_anywhere=True, keep_on_top=True)
            window.reappear()
        elif event == 'Open':
            filename = sg.popup_get_file('File to open', no_window=True)
            print(filename)

    window.close()
    
def validate(values):
    ten_ns = values['name']
    ma_ns = values['mns']
    if len(ten_ns) == 0 or len(ma_ns) == 0:
        return sg.popup('Notice','Thông tin nhân sự không được trống')
    if len(ma_ns) != 6:
        return sg.popup('Notice', 'Sai mã nhân sự')
    for x in ten_ns:
        for y in ma_ns:
            if not (x.isalpha() or x.isspace()):
                return sg.popup('Notice','Sai tên nhân sự')
            if y.isalpha():
                return sg.popup('Notice', 'Sai mã nhân sự')
    
   
        