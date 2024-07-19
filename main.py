import tkinter as tk
from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import os
from PIL import Image, ImageTk
from pathlib import Path
import shutil
import send2trash

HEIGHT = 700
WIDTH = 600
CURRENT_FOLDER = "Choose folder"
MOVE_TO_FOLDER = ''
IMAGES = []
IMAGE_POSITION = -1


def get_image_names(folder):
    global IMAGES
    os.chdir(Path(folder))
    IMAGES = []
    for filename in os.listdir('.'):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith(
                '.gif') or filename.endswith('.tiff') or filename.endswith('.webp') or filename.endswith('.bmp'):
            IMAGES.append(filename)


def choose_folder():
    global CURRENT_FOLDER, IMAGE_POSITION
    prev_folder = current_folder_name['text']
    CURRENT_FOLDER = askdirectory()

    # if cancel button was clicked
    if prev_folder != '' and CURRENT_FOLDER == '':
        CURRENT_FOLDER = prev_folder
    # if same folder was chosen again
    if CURRENT_FOLDER == prev_folder:
        return  # so as to not refresh the IMAGES list and restart

    current_folder_name['text'] = 'Current Folder: ' + CURRENT_FOLDER
    label_move_to_folderpath['text'] = '[Current Folder]' if MOVE_TO_FOLDER == '' else MOVE_TO_FOLDER
    get_image_names(CURRENT_FOLDER)

    # no IMAGES found in the folder
    if not IMAGES:
        label_image_name['text'] = 'No IMAGES found in this folder'
        image_icon.delete("all")
        image_icon['bg'] = 'grey'
        label_image_number['text'] = ''
        return

    IMAGE_POSITION = -1
    open_image('next')  # opens image at index 0


# shows relevant status in the status labels
def refresh_status(arg):
    if arg == 'delete':
        label_delete_status['fg'] = 'black'
        label_delete_status['text'] = 'Delete status'
    elif arg == 'rename':
        label_rename_status['fg'] = 'black'
        label_rename_status['text'] = 'Rename status'
    elif arg == 'move':
        label_move_status['fg'] = 'black'
        label_move_status['text'] = 'Move status'


def open_image(arg):
    global CURRENT_FOLDER, IMAGE_POSITION, image_icon, label_image_number, IMAGES

    # input validation
    if CURRENT_FOLDER in ["Choose folder", ""] or current_folder_name == 'Selected folder path will appear here':
        current_folder_name['text'] = 'Choose a folder first!'
        image_icon.delete("all")
        image_icon = Canvas(label_image_name, bg='grey', highlightthickness=0)
        image_icon.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        label_image_name['text'] = 'Image name will appear here'
        label_image_number['text'] = 'Image #'
        return

    if arg == 'next':  # next button action
        IMAGE_POSITION += 1
        IMAGE_POSITION = 0 if IMAGE_POSITION >= len(IMAGES) else IMAGE_POSITION
    elif arg == 'previous':  # previous button action
        IMAGE_POSITION -= 1
        IMAGE_POSITION = len(IMAGES) - 1 if IMAGE_POSITION < 0 else IMAGE_POSITION

    try:  # tries opening an image at a given index
        img = ImageTk.PhotoImage(Image.open(CURRENT_FOLDER + '/' + IMAGES[IMAGE_POSITION]).resize((400, 300)))
    except IndexError:  # image not found
        label_image_name['text'] = 'No IMAGES found in this folder'
        label_image_number['text'] = ''
        IMAGE_POSITION = -1
        return

    # places a new canvas widget at the same spot for each image
    image_icon = Canvas(label_image_name, bg='grey', highlightthickness=0)
    image_icon.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    image_icon.create_image(227, 157, anchor=CENTER, image=img)
    image_icon.image = img

    label_image_name['text'] = IMAGES[IMAGE_POSITION]

    label_image_number = Label(label_image_name, text=f'Image {IMAGE_POSITION + 1} of {len(IMAGES)}',
                               font=('Courier', 14), anchor=N, justify=CENTER)
    label_image_number.place(relx=0.1, rely=0.92, relwidth=0.75, relheight=0.2)

    label_rename_status['fg'] = 'black'
    label_rename_status['text'] = 'Rename status'


def change_destination():
    global MOVE_TO_FOLDER
    MOVE_TO_FOLDER = askdirectory()

    # input validation
    if MOVE_TO_FOLDER == '' or MOVE_TO_FOLDER == CURRENT_FOLDER:
        label_move_to_folderpath['text'] = '[Current Folder]'
        return

    label_move_to_folderpath['text'] = MOVE_TO_FOLDER


def move_image():
    global IMAGE_POSITION, IMAGES, MOVE_TO_FOLDER

    move_to = MOVE_TO_FOLDER

    # input validation
    if label_move_to_folderpath['text'] == '':
        label_move_status['fg'] = 'red'
        label_move_status['text'] = 'Select a folder first!'
        label_move_status.after(2000, lambda: refresh_status('move'))
        return
    if current_folder_name['text'] in ['', 'Selected folder path will appear here'] or label_image_name[
        'text'] == 'No IMAGES found in this folder':
        label_move_status['fg'] = 'red'
        label_move_status['text'] = 'Choose an image to move first!'
        label_move_status.after(2000, lambda: refresh_status('move'))
        return
    if label_move_to_folderpath['text'] == '[Current Folder]' or CURRENT_FOLDER == MOVE_TO_FOLDER:
        label_move_status['fg'] = 'orange'
        label_move_status['text'] = 'You are in the same folder!'
        label_move_status.after(2000, lambda: refresh_status('move'))
        return

    # renames file if a similar name already exists in the folder
    renamed_image_file = ''
    count = 1
    os.chdir(Path(move_to))
    while IMAGES[IMAGE_POSITION] in os.listdir('.'):
        renamed_image_file = f'{IMAGES[IMAGE_POSITION].split(".")[0].replace(".", "-")} ({count}).{IMAGES[IMAGE_POSITION].split(".")[1]}'
        if renamed_image_file not in os.listdir('.'):
            break
        count += 1

    os.chdir(Path(CURRENT_FOLDER))
    if renamed_image_file == '':  # if file was not renamed before moving
        label_move_status['fg'] = 'orange'
        label_move_status['text'] = f'Image moved to ./{os.path.basename(move_to)}'
        renamed_image_file = IMAGES[IMAGE_POSITION]
    else:  # if file was renamed before moving
        renamed_image_file = renamed_image_file
        label_move_status['fg'] = 'orange'
        label_move_status['text'] = f'Image renamed to {renamed_image_file} and moved ./{os.path.basename(move_to)}'
    renamed_image_file = IMAGES[IMAGE_POSITION] if renamed_image_file == '' else renamed_image_file
    shutil.move(Path(CURRENT_FOLDER.replace('/', '//')) / IMAGES[IMAGE_POSITION],
                Path(move_to.replace('/', '//')) / renamed_image_file)

    app.wm_attributes("-disabled", True)  # freezes the window

    # updates the IMAGES list
    IMAGES.remove(IMAGES[IMAGE_POSITION])
    try:  # moves to the next image in list
        IMAGE_POSITION = IMAGE_POSITION - 1 if 0 <= IMAGE_POSITION < len(IMAGES) else -1
    except TypeError:  # if no IMAGES left after move
        label_image_name['text'] = 'No IMAGES found in this folder'
        image_icon.delete("all")
        label_image_number['text'] = ''
        label_move_status.after(2000, lambda: refresh_status('move'))
        return
    open_image('next')

    app.wm_attributes("-disabled", False)  # unfreezes the window after the IMAGES list is updated

    label_move_status.after(5000, lambda: refresh_status('move'))


def delete_image():
    global IMAGE_POSITION, IMAGES

    # input validation
    if label_image_name['text'] in ['Image name will appear here', '', 'No IMAGES found in this folder']:
        label_delete_status['fg'] = 'red'
        label_delete_status['text'] = 'Choose an image!'
        label_delete_status.after(2000, lambda: refresh_status('delete'))
        return

    # deletes the image and sends it to the recylce bin
    os.chdir(Path(CURRENT_FOLDER))
    send2trash.send2trash(IMAGES[IMAGE_POSITION])

    # update label
    label_delete_status['fg'] = 'orange'
    label_delete_status['text'] = 'Sent to recycle bin!'

    app.wm_attributes("-disabled", True)  # freezes the window

    # update IMAGES list
    IMAGES.remove(IMAGES[IMAGE_POSITION])
    try:  # moves the next image in list if found
        IMAGE_POSITION = IMAGE_POSITION - 1 if 0 <= IMAGE_POSITION < len(IMAGES) else -1
    except TypeError:  # if no IMAGES left
        label_image_name['text'] = 'No IMAGES found in this folder'
        image_icon.delete("all")
        label_image_number['text'] = ''
        label_move_status.after(2000, lambda: refresh_status('delete'))
        return
    open_image('next')

    app.wm_attributes("-disabled", False)  # unfreezes the window after the IMAGES list is updated

    label_delete_status.after(2000, lambda: refresh_status('delete'))


def rename_image():
    global IMAGE_POSITION, IMAGES

    # input validation
    old_response = label_image_name['text']
    new_response = f'{entry_rename_image.get().replace(".", "-")}.{old_response.split(".")[len(old_response.split(".")) - 1]}'
    if old_response == new_response:
        label_rename_status['fg'] = 'orange'
        label_rename_status['text'] = 'Image already has the same name!'
        label_rename_status.after(3000, lambda: refresh_status('rename'))
        return
    if label_image_name['text'] in ['Image name will appear here', '', 'No IMAGES found in this folder']:
        label_rename_status['fg'] = 'red'
        label_rename_status['text'] = 'Choose an image first!'
        label_rename_status.after(3000, lambda: refresh_status('rename'))
        return
    new_image_name = entry_rename_image.get().replace(".", "-")
    if new_image_name.strip() == '':
        label_rename_status['fg'] = 'red'
        label_rename_status['text'] = 'Enter a valid name!'
        label_rename_status.after(3000, lambda: refresh_status('rename'))
        return

    # file name validation
    invalid_file_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for letter in new_image_name:
        if letter in invalid_file_chars:
            new_image_name = new_image_name.replace(letter, '-')

    # adds extension at the end of the file name
    new_image_file = f'{new_image_name.strip().replace(".", "-")}.{IMAGES[IMAGE_POSITION].split(".")[len(IMAGES[IMAGE_POSITION].split(".")) - 1]}'

    # renames file if a similar name already exists in the folder
    count = 1
    os.chdir(Path(CURRENT_FOLDER))
    while new_image_file in os.listdir('.'):
        new_image_file = f'{new_image_name} ({count}).{IMAGES[IMAGE_POSITION].split(".")[len(IMAGES[IMAGE_POSITION].split(".")) - 1]}'
        if new_image_file not in os.listdir('.'):
            break
        count += 1

    # renames file to new file name
    shutil.move(Path(CURRENT_FOLDER.replace('/', '//')) / IMAGES[IMAGE_POSITION],
                Path(CURRENT_FOLDER.replace('/', '//')) / new_image_file)

    # update IMAGES list and updates img position to where the image file with the updated name is
    IMAGES[IMAGE_POSITION] = new_image_file

    # shows related status
    label_rename_status['fg'] = 'orange'
    label_rename_status['text'] = 'Image renamed!'

    label_image_name['text'] = new_image_file

    # reopen image with the updated name
    img = ImageTk.PhotoImage(Image.open(CURRENT_FOLDER + '/' + IMAGES[IMAGE_POSITION]).resize((400, 300)))
    image_icon = Canvas(label_image_name, bg='grey', highlightthickness=0)
    image_icon.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
    image_icon.create_image(227, 157, anchor=CENTER, image=img)
    image_icon.image = img
    # updates number
    label_image_number = Label(label_image_name, text=f'Image {IMAGE_POSITION + 1} of {len(IMAGES)}',
                               font=('Courier', 14), anchor=N, justify=CENTER)
    label_image_number.place(relx=0.1, rely=0.92, relwidth=0.75, relheight=0.2)

    # deletes text in the textbox
    entry_rename_image.delete(0, END)

    label_rename_status.after(4000, lambda: refresh_status('rename'))


def leftKey(event):
    open_image('previous')


def rightKey(event):
    open_image('next')


def enterKey(event):
    rename_image()


def upKey(event):
    global IMAGES, IMAGE_POSITION
    os.chdir(Path(CURRENT_FOLDER))
    os.system(f'"{IMAGES[IMAGE_POSITION]}"')


def shiftKey(event):
    global CURRENT_FOLDER
    CURRENT_FOLDER = CURRENT_FOLDER.replace("/", "\\")
    print(CURRENT_FOLDER)
    os.system(r'start %windir%\explorer.exe' + rf' "{CURRENT_FOLDER}"')


app = tk.Tk()  # app window
app.title("Image Manager")

app.bind('<Left>', leftKey)
app.bind('<Right>', rightKey)
app.bind('<Return>', enterKey)  # enter key - renames image
app.bind('<Up>', upKey)  # Up key - opens image
app.bind('<Shift_L>', shiftKey)  # any shift key - opens image folder

##### ALL THE WIDGETS IN OUR APP GOES IN HERE #####
canvas = Canvas(app, height=HEIGHT, width=WIDTH)
canvas.pack()

# use frames to organize widgets #
##### CURRENT FOLDER FRAME #####
current_folder_frame = Frame(app, bg='#73BB71', bd=5)
current_folder_frame.place(relx=0, rely=0, relwidth=1, relheight=0.05, anchor=NW)

current_folder_name = Label(current_folder_frame, text="Selected folder path will appear here")
current_folder_name.place(relwidth=1, relheight=1)
##### END CURRENT FOLDER FRAME ####

##### TOP NAV BUTTONS FRAME #####
top_frame = Frame(app, bg='#75A09F', bd=5)  # bd defines border width/space for a widget
top_frame.place(relx=0, rely=0.05, relwidth=1, relheight=0.05, anchor=NW)

previous_button = Button(top_frame, text="Previous", command=lambda: open_image('previous'))
previous_button.place(relx=0, rely=0, relwidth=0.3, relheight=1)

choose_button = Button(top_frame, text=CURRENT_FOLDER, width=0, command=choose_folder)
choose_button.place(relx=0.35, rely=0, relwidth=0.3, relheight=1)

next_button = Button(top_frame, text="Next", command=lambda: open_image('next'))
next_button.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
##### END TOP NAV BUTTONS FRAME #####

##### IMAGE FRAME #####
image_frame = Frame(app, bg='#73BB71', bd=10)
image_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.6, anchor=NW)

label_image_name = Label(image_frame, text="Image name will appear here", font=('Courier', 14), anchor=N,
                         justify=CENTER,
                         bd=4)
label_image_name.place(relwidth=1, relheight=1)

image_icon = Canvas(label_image_name, bg='grey', highlightthickness=0)
image_icon.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)

label_image_number = Label(label_image_name, text="Image #", font=('Courier', 14), anchor=N, justify=CENTER)
label_image_number.place(relx=0.1, rely=0.92, relwidth=0.75, relheight=0.2)
##### END IMAGE FRAME #####

##### MANAGE IMAGE FRAME ######
manage_image_frame = Frame(app, bg='#75A09F', bd=10)
manage_image_frame.place(relx=0, rely=0.7, relwidth=1, relheight=0.3, anchor=NW)

label_rename = Label(manage_image_frame, text="Rename Image:", width=0, font=40)
label_rename.place(relx=0.01, rely=0.01, relheight=0.1, anchor=NW)

label_rename_status = Label(manage_image_frame, text="Rename status", bg='grey', width=0)
label_rename_status.place(relx=0.22, rely=0.01, relheight=0.1, anchor=NW)

label_delete = Label(manage_image_frame, text="Delete Image:", width=0, font=40)
label_delete.place(relx=0.6, rely=0.01, relheight=0.1, anchor=NW)

label_delete_status = Label(manage_image_frame, text="Delete status", bg='grey', width=0)
label_delete_status.place(relx=0.785, rely=0.01, relheight=0.1, anchor=NW)

delete_button = Button(manage_image_frame, text='DELETE IMAGE', bg='red', fg='white', width=0, command=delete_image)
delete_button.place(relx=0.7, rely=0.15, relheight=0.2, anchor=NW)

entry_rename_image = Entry(manage_image_frame)
entry_rename_image.place(relx=0.01, rely=0.13, relwidth=0.4, relheight=0.2, anchor=NW)

button_rename = Button(manage_image_frame, text="Rename", width=0, command=rename_image)
button_rename.place(relx=0.43, rely=0.13, relheight=0.2, anchor=NW)

label_move_to = Label(manage_image_frame, text="Move Image To:", width=0, font=40)
label_move_to.place(relx=0.01, rely=0.5, relheight=0.1, anchor=NW)

label_move_status = Label(manage_image_frame, text="Move status", bg='grey', width=0)
label_move_status.place(relx=0.22, rely=0.5, relheight=0.1, anchor=NW)

label_move_to_folderpath = Label(manage_image_frame)
label_move_to_folderpath.place(relx=0.01, rely=0.64, relwidth=0.55, relheight=0.2, anchor=NW)

button_move = Button(manage_image_frame, text="Move Image", width=0, command=move_image)
button_move.place(relx=0.58, rely=0.64, relheight=0.2, anchor=NW)

button_change_destination = Button(manage_image_frame, text="Change Destination", width=0, command=change_destination)
button_change_destination.place(relx=0.73, rely=0.64, relheight=0.2, anchor=NW)

button_quit = Button(manage_image_frame, text='QUIT APP', bg='#E73927', command=app.quit)
button_quit.place(relx=0, rely=0.91, relwidth=1, relheight=0.1)
##### END MOVE IMAGE FRAME #####

messagebox.showinfo("Keyboard Shorcuts", "Following shortcuts are available:\n"
                                         "\nUP ARROW - Opens image"
                                         "\nSHIFT KEY - Opens image folder"
                                         "\nRIGHT ARROW - Moves to next image if available"
                                         "\nLEFT ARROW - Moves to previous image if available"
                                         "\nENTER KEY - Renames image if available")

app.mainloop()  # runs main application window
