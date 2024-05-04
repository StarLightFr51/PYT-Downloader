import tkinter
import tkinter.scrolledtext
import customtkinter
from pytube import YouTube
from PIL import ImageTk, Image
import urllib.request
import io
import sounddevice as sd
import soundfile as sf
import os

def download_video():
    try:
        ytLink = link.get()
        ytObj = YouTube(ytLink)

        video_title = ytObj.title
        video_author = ytObj.author
        video_thumbnail_url = ytObj.thumbnail_url
        with urllib.request.urlopen(video_thumbnail_url) as u:
            raw_data = u.read()

        img = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(img)

        photo_label.configure(image=photo)
        finishLabel.configure(text="")
        confirmation_label.configure(text="Are you sure you want to download this video ?", text_color = "white")
        title.configure(text=f"{video_title} by {video_author}")

        photo_label.pack()
        confirmation_button.pack(pady=10)
    except:
        first_error_label.configure(text="url invalid or an unexpected error occurred", text_color="red")

def confirm_download():
    try:
        ytLink = link.get()
        ytObj = YouTube(ytLink)
        video = ytObj.streams.get_highest_resolution()
        file_path = f"{os.getenv('USERPROFILE')}\\Downloads"
        video.download(file_path)
        notif_file = "src\\notification_sound.wav"
        data, fs = sf.read(notif_file, dtype='float32')
        finishLabel.configure(text="Video successfully downloaded (Saved in your download folder) !", text_color="lime")
        sd.play(data, fs)
        status = sd.wait()
    except:
        finishLabel.configure(text="url invalid or an unexpected error occurred", text_color="red")

app = customtkinter.CTk()

width = 1536
height = 864

screen_width = app.winfo_screenwidth()  # Width of the screen
screen_height = app.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

app.geometry('%dx%d+%d+%d' % (width, height, x, y))
app.title("Youtube Video Downloader")

label = customtkinter.CTkLabel(app, text="Insert a youtube link")
label.pack(padx=10, pady=10)

url = tkinter.StringVar()
link = customtkinter.CTkEntry(app, width=550, height=35, textvariable=url)
link.pack()

#Finished Label
first_error_label = customtkinter.CTkLabel(app, text="")
first_error_label.pack()

download = customtkinter.CTkButton(app, text="Download Video", command=download_video)
download.pack(pady=5)

confirmation_label = customtkinter.CTkLabel(app, text="")
confirmation_label.pack(pady=10)

title = customtkinter.CTkLabel(app, text="")
title.pack(pady=2)

photo_label = customtkinter.CTkLabel(app, text="")

confirmation_button = customtkinter.CTkButton(app, text="Finish Download", command=confirm_download)

finishLabel = customtkinter.CTkLabel(app, text="")
finishLabel.pack(pady=5)

app.mainloop()
