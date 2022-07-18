import tkinter as tk
import os
import tkinter.messagebox as box
from pytube import YouTube
from pytube import Playlist
import re

desktop = os.path.join(os.path.join(os.environ['USERPROFILE']),'Onedrive', 'Desktop')

class Youtube_link:
    def __init__(self, url, is_video, is_playlist, destination=desktop):
        """destination of mp3 files is defaulted at 'this directory'"""
        self.url = url
        self.is_video = is_video   # IS VIDEO means is it a yt link at all
        self.is_playlist = is_playlist
        self.destination = destination

    def playlist_or_video_to_mp3(self): 
        """Validates youtube link"""
        yt_link_regex = re.compile( 
            "^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
        )   # is it a youtube link

        yt_playlist_link_regex = re.compile(
            "^https?:\/\/(www.youtube.com|youtube.com)\/playlist(.*)$"
        )   # is it a playlist link

        mo = yt_link_regex.search(self.url) #   is it a link
        mo1 = yt_playlist_link_regex.search(self.url)   # is it a playlist 

        if mo and not mo1:
            self.is_video = True
            self.is_playlist = False
            continute_response = box.askquestion('Continue', "This is a video link; do you wish to continue?")
            if continute_response == 'no': 
                return
            else: 
                pass

        elif mo and mo1:
            self.is_video = True
            self.is_playlist = True
            continute_response = box.askquestion('Continute?', "This is a playlist link; do you wish to continue?")
            if continute_response == 'no': 
                return
            else: 
                pass

        else:
            self.is_playlist = False
            self.is_video = False
            box.showerror('ERROR', "URL ERROR")
            return

        """Checks for if it's just a video or it's a playlist; turns them into mp3 files"""
        if self.is_playlist == False and self.is_video:   # it is just a video
            try:
                yt = YouTube(self.url)
            except: 
                box.showerror('ERROR', 'ERROR CONNECTING')
            video = yt.streams.filter(only_audio=True).first()
            outfile = video.download(output_path=self.destination)
            base, ext = os.path.splitext(outfile)
            file_new_name = base + '.mp3'
            os.rename(outfile, file_new_name)
            box.showinfo('INFO', f'{file_new_name} downloaded')

        elif self.is_playlist and self.is_video:   # it is a playlist 
            try: 
                p = Playlist(self.url)
            except:
                box.showerror('ERROR','ERROR CONNECTING')
            for videos in p.videos: 
                outfile = videos.streams.filter(only_audio=True).first().download(output_path=self.destination)
                base, ext = os.path.splitext(outfile)
                file_new_name = base + '.mp3'
                os.rename(outfile, file_new_name)
            box.showinfo('INFO', f'Playlist Downloaded')
                
        else: 
            box.showerror('ERROR', 'URL ERROR')

root = tk.Tk()

# Dimensions of GUI
window_width, window_height = 400, 375
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.resizable(False, False)

# Colors and fonts with Scaling
bg_color = "#F1DAD5"
font_regular = ("Roboto", 6)
font_entry = ("Roboto", 5)
root.tk.call("tk", "scaling", 2.75)

# Title, background, and icon
root.title("Youtube URL to MP3")
root.config(bg=bg_color)
root.iconbitmap("icon.ico")

# Center GUI with Geometry
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / (3 / 2))
root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# Loading image widgets
mp3_image = tk.PhotoImage(file="mp3_128.png")
mp3_label = tk.Label(root, image=mp3_image, bg=bg_color)

arrow_image = tk.PhotoImage(file="transfer_32.png")
arrow_label = tk.Label(root, image=arrow_image, bg=bg_color)

yt_image = tk.PhotoImage(file="youtube_128.png")
yt_label = tk.Label(root, image=yt_image, bg=bg_color)

# Loading link entry widget
frame = tk.Frame(root, bg=bg_color)
entry_link = tk.Entry(frame, width=30, font=font_entry)
link_label = tk.Label(root, text="Enter Video Link:", font=font_regular, bg=bg_color)

# Loading radio pole
choice_video_playlist = tk.StringVar()
radio_1 = tk.Radiobutton(
    root,
    text="Video",
    variable=choice_video_playlist,
    value=1,
    font=font_entry,
    bg=bg_color,
    pady=5,
)
radio_2 = tk.Radiobutton(
    root,
    text="Playlist",
    variable=choice_video_playlist,
    value=2,
    font=font_entry,
    bg=bg_color,
    pady=5,
)
radio_1.select()

# Loading path entry widget
frame_2 = tk.Frame(root, bg=bg_color)
entry_destination = tk.Entry(frame_2, width=30, font=font_entry)
entry_destination.insert(0, "DESKTOP DEFAULT")
destination_label = tk.Label(
    root, text="Destination Path:", font=font_regular, bg=bg_color
)

def master_commander():
    """Validates path and calls playlist_or_video_to_mp3()"""
    Url = entry_link.get()  # first argument
    video_valid = False  # second argument
    playlist_valid = False  # thrid arugment
    Radio_poll_response = choice_video_playlist.get()
    if Radio_poll_response == 1:
        video_valid = True
        playlist_valid = False
    elif Radio_poll_response == 2:
        video_valid = True
        playlist_valid = True
    destinationer_desired = entry_destination.get()
    if destinationer_desired != "DESKTOP DEFAULT":
        is_dir = os.path.isdir(destinationer_desired)
        if is_dir == False:
            box.showerror("Error", "Path/directory does not exist!")
            return
        else:
            YT_obj = Youtube_link(
                Url, video_valid, playlist_valid, destinationer_desired
            )
            YT_obj.playlist_or_video_to_mp3()
    else:
        YT_obj = Youtube_link(Url, video_valid, playlist_valid)
        YT_obj.playlist_or_video_to_mp3()


# Object = classer.Youtube_link(self, url, is_video, is_playlist, destination='.')
# Object.playlist_or_video_to_mp3

submit_button = tk.Button(
    root, text="convert to mp3", font=font_regular, command=master_commander
)


# How to grid widget.grid(column, row, sticky, padx, pady, ipadx, ipady)
# Configuring grids
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=1)


# Gridding images
yt_label.grid(column=0, row=0, sticky=tk.SE)
arrow_label.grid(column=1, row=0, sticky=tk.S)
mp3_label.grid(column=2, row=0, sticky=tk.SW)

# Gridding Link entry
frame.grid(row=1, column=1, sticky=tk.W, columnspan=2)
entry_link.grid(row=1, column=1, sticky=tk.W, columnspan=2)
link_label.grid(row=1, column=0)

# Gridding radio pole
radio_1.grid(row=1, column=0, sticky=tk.SW)
radio_2.grid(row=1, column=0, sticky=tk.S, columnspan=2)

# Gridding destination entry
frame_2.grid(column=1, row=2, sticky=tk.NW, columnspan=2)
entry_destination.grid(column=0, row=2, columnspan=2, sticky=tk.NW)
destination_label.grid(column=0, row=2, sticky=tk.NW)
# Gridding submit button
submit_button.grid(column=0, row=2, columnspan=3)

root.mainloop()
