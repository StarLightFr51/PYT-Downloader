#App's Version 1.2.0
#Open Source Project (Do what you want with it)

import tkinter
import customtkinter
from pytube import YouTube
from PIL import ImageTk, Image
import urllib.request
import winsound
import datetime
import io
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
        thumbnail_image.configure(image=photo)
        video_time = datetime.timedelta(seconds=ytObj.length)
        video_release_date = ytObj.publish_date

        releaseLabel.configure(text=f"Video release the {video_release_date}")
        timeLabel.configure(text=f"Duration : {video_time}")
        finishLabel.configure(text="")
        confirmation_label.configure(text="Are you sure you want to download this video ?")
        title.configure(text=f"{video_title} by {video_author}")

        thumbnail_image.pack()
        confirmation_button.pack(pady=10)
    except Exception as e:
        finishLabel.configure(text="url invalid or an unexpected error occurred", text_color="red")
        print(e)

def confirm_download():
    try:
        ytLink = link.get()
        ytObj = YouTube(ytLink)
        video = ytObj.streams.get_highest_resolution()
        file_path = f"{os.getenv('USERPROFILE')}\\Downloads"
        video.download(file_path)
        finishLabel.configure(text="Video successfully downloaded (Check your download folder) !", text_color="lime")
        notif_path = "src\\notification_sound"
        winsound.PlaySound(notif_path, winsound.SND_FILENAME)

    except Exception as e:
        finishLabel.configure(text="url invalid or an unexpected error occurred", text_color="red")
        print(e)
        
app = customtkinter.CTk()

width = 1536
height = 864

screen_width = app.winfo_screenwidth()  # Width of the screen
screen_height = app.winfo_screenheight() # Height of the screen
 
# Calculate Starting X and Y coordinates for Window
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)

app.geometry('%dx%d+%d+%d' % (width, height, x, y))
app.title("PYT Video Downloader")
app.resizable(False, False)

scroll = customtkinter.CTkScrollableFrame(app, width= width, height= height, orientation="vertical")
scroll.pack()

label = customtkinter.CTkLabel(scroll, text="Insert a youtube link")
label.pack(padx=10, pady=10)

url = tkinter.StringVar()
link = customtkinter.CTkEntry(scroll, width=550, height=35, textvariable=url)
link.pack()

download = customtkinter.CTkButton(scroll, text="Download Video", command=download_video)
download.pack(pady=5)

confirmation_label = customtkinter.CTkLabel(scroll, text="")
confirmation_label.pack(pady=10)

title = customtkinter.CTkLabel(scroll, text="")
title.pack()

releaseLabel = customtkinter.CTkLabel(scroll, text="")
releaseLabel.pack()

timeLabel = customtkinter.CTkLabel(scroll, text="")
timeLabel.pack()

thumbnail_image = customtkinter.CTkLabel(scroll, text="")

confirmation_button = customtkinter.CTkButton(scroll, text="Finish Download", command=confirm_download)

finishLabel = customtkinter.CTkLabel(scroll, text="")
finishLabel.pack(pady=5)

app.mainloop()
