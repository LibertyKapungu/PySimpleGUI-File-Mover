import PySimpleGUI as psg
import os.path
import shutil

layout = [
    [psg.Text('Source Folder: ', size=(15, 1), justification='s'), psg.Input(enable_events=True , key='-INPUT FOLDER-'), psg.FolderBrowse('Browse')],
    [psg.Text('Destination Folder: ' , size=(15, 1), justification='s'), psg.Input(key='-OUTPUT FOLDER-'), psg.FolderBrowse('Browse')],
    [psg.Text('File Extension: ', size= (15,1), justification='s'), psg.Input(enable_events=True, size=(10,1), key = 'File Extension'), psg.FileBrowse(key='browse')],
    [psg.Button('Transfer'), psg.Button('Refresh'),  psg.Button('Exit')],
    [psg.Listbox(values=[], enable_events=True, size=(70,10), key= '-SOURCE FILES-')],
]

window = psg.Window("Simply Moving Files", layout)

def update_file_content(source_key: str, file_buffer_key: str):

    window.refresh()

    in_folder = status[source_key]

    try:
        list_of_files = os.listdir(in_folder)
    except:
        list_of_files = []

    window[file_buffer_key].Update(list_of_files)

    return None

def transfer_files(source_key: str, target_key: str, extension_key: str):

    source_path = status[source_key]
    target_path = status[target_key]
    file_extension = status[extension_key]

    if not os.path.exists(source_path):
        psg.popup_error('Invalid source folder')
        return None

    if not os.path.exists(target_path):
        psg.popup_error('Invalid destination folder')
        return None

    list_of_files = os.listdir(source_path)

    can_pop_up = False

    for file_name in list_of_files:

        if not file_extension:
            pass

        elif file_name.endswith(file_extension):
            can_pop_up = True
            shutil.move(os.path.join(source_path, file_name), target_path)
            
    if can_pop_up:
        psg.popup_ok('File Transfer Complete')
    else:
        psg.popup_ok('No files with this extension')

    return None

while True:

    event, status = window.read()

    print(event, status)

    if event in (psg.WINDOW_CLOSED, "Exit"):
        break

    if event == '-INPUT FOLDER-':
        update_file_content('-INPUT FOLDER-', '-SOURCE FILES-')

    if event == 'Transfer':
        transfer_files('-INPUT FOLDER-', '-OUTPUT FOLDER-', 'File Extension')

    if event == 'Refresh':
        update_file_content('-INPUT FOLDER-', '-SOURCE FILES-')

    if event == 'File Extension':

        filename = status['File Extension']
        extension = os.path.splitext(filename)[1]
        window['File Extension'].Update(extension)
        
window.close()