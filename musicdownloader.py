from __future__ import unicode_literals 
import tkinter as tk 
from tkinter import ttk , messagebox as m_box , filedialog
import youtube_dl , os , urllib.request , subprocess , webbrowser
from bs4 import BeautifulSoup
import threading

# LINKS 

facebook_link = "https://www.facebook.com/aryan.shridhar.1"
instagram_link = "https://www.instagram.com/aryanshridhar_007/"
twitter_link = "https://twitter.com/ShridharAryan"
gmail_link = "https://mail.google.com/mail/u/0/#inbox"
github_link = "https://github.com/aryanshridhar"
linkdln_link = "https://www.linkedin.com/in/aryan-shridhar-b3a44b19a/"

win = tk.Tk() 
win.geometry('640x400')
win.title('Music Downloader')

#VARIABLE

label_text = ''

# FUNCTIONS 

def get_title(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ytdl:
        result = ytdl.extract_info(url)
    return result

def handle_click():   #THREADING DATA USED : http://stupidpythonideas.blogspot.com/2013/10/why-your-gui-app-freezes.html
    def download():
        search_result = entry_var.get()
        if search_result == '':
            m_box.showerror('Error' , 'Enter the song name')
            return
        try:
            query = urllib.parse.quote(search_result)
            url = "https://www.youtube.com/results?search_query=" + query
            response = urllib.request.urlopen(url)
        except urllib.error.URLError:
            m_box.showerror('Error' , 'Make sure you are connected to internet !')
        else:
            global label_text
            label_text = 'Status  :  Connecting to server ....'
            download_.config(text = label_text)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            vid = soup.find(attrs={'class':'yt-uix-tile-link'})
            # for vid in soup.findall(attrs={'class':'yt-uix-tile-link'}): To dug more deeper to look for music
            result = 'https://www.youtube.com' + vid['href']
            label_text = 'Status :  Downloading ... \n\tPlease wait '
            download_.config(text = label_text)
            download_.grid(row = 2 , column = 0 , columnspan = 30)
            file_name = get_title(result)
            label_text = f'Downloaded and saved in \n{os.getcwd()}'
            download_.config(text = label_text)
            latest_file = max(os.listdir() , key = lambda item : os.path.getctime(item))
            new_name = latest_file.split('.')[0]
            try:
                os.rename(latest_file, new_name + '.mp3')
            except FileExistsError:
                m_box.showerror('Error' , 'File already exists\nCreated a mp4 instead !')
    
    thread1 = threading.Thread(target=download)
    thread1.start()

def changefunc():
    result = filedialog.askdirectory(parent = win , initialdir = os.getcwd() , title = "Select a Folder")
    os.chdir(result)
#MENU 

main_menu = tk.Menu(win)

open_menu = tk.Menu(main_menu , tearoff = 0)
main_menu.add_cascade(label = "Open" , menu = open_menu)
open_menu.add_command(label = "Open download folder" , command = lambda: webbrowser.open(os.path.realpath(os.getcwd())))

edit_menu = tk.Menu(main_menu , tearoff = 0)
main_menu.add_cascade(label = 'Edit' , menu = edit_menu)
edit_menu.add_command(label = 'Current Download folder' , command = lambda : m_box.showinfo('Info' , os.getcwd())) 
edit_menu.add_command(label = 'Change Download folder' , command = changefunc)

dev_menu = tk.Menu(main_menu , tearoff = 0)
main_menu.add_cascade(label = "Socialize" , menu = dev_menu)
dev_menu.add_command(label = "Github" , command = lambda : webbrowser.open_new(github_link)) 
dev_menu.add_command(label = "Linkedln", command = lambda : webbrowser.open_new(linkdln_link)) 
dev_menu.add_separator()
dev_menu.add_command(label = "Instagram", command = lambda : webbrowser.open_new(instagram_link))
dev_menu.add_command(label = "Twitter", command = lambda : webbrowser.open_new(twitter_link)) 
dev_menu.add_command(label = "Facebook", command = lambda : webbrowser.open_new(facebook_link)) 

feedback_menu = tk.Menu(main_menu , tearoff = 0)
main_menu.add_cascade(label = "Feedback" , menu = feedback_menu)
feedback_menu.add_command(label = "Send Feedback" , command = lambda : webbrowser.open_new(gmail_link))

win.config(menu = main_menu)


# LABELFRAME 

label_frame = tk.LabelFrame(win , text = "Music Downloader")
label_frame.grid(row = 0 , column = 0 , padx = 60 , pady = (60,10))

download_ = ttk.Label(label_frame , text = label_text)
download_.grid(row = 2 , column = 0 , sticky = tk.W , pady = (20,0) , padx = 21)

# MUSIC LABEL

music_label = ttk.Label(label_frame , text = 'Enter the name of song :  ' , justify = 'center' , font = ('Times' , 13))
music_label.grid(row = 0 , column = 0 , padx = 20 , pady = 30)
music_label.config(anchor ='center')

tip_label = ttk.Label(label_frame , text= 'Tip : Try to be a bit more specific ')
tip_label.grid(row=1 , column=0)

# ENTRY MUSIC 

entry_var = tk.StringVar()
music_entry = ttk.Entry(label_frame , width = 27, justify = 'center' , textvariable = entry_var)
music_entry.grid(row = 0 , column= 1 , padx = (0,30) , ipady = 2)

# DOWNLOAD BUTTON 

down_button = ttk.Button(win , text = 'Download' , width = 12 , command = handle_click)
down_button.grid(row = 1, column = 0)

win.mainloop() 