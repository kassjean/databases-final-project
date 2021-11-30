# Name:       Kassady Herriott
# Professor:  Chad Mourning
# Class:      CS4620
# Date:       21 November 2021
# Assignment: Final Project 

from tkinter import *
import psycopg2
from tkinter import ttk
import passkey as configs
import webbrowser
import platform
from tkinter import messagebox


#Database set up 

conn = psycopg2.connect(user = "postgres", password = configs.password, host = "databases-final.cvrf9yw5octw.us-east-2.rds.amazonaws.com", port = "5432")
print("Opened database successfully")

cur = conn.cursor()

gui = Tk()
geo = "400x450+10+20"
gui.title('Youtube Jukebox')
gui.config(bg='black')
gui.geometry(geo)


#FILTERING
def filter_by_artist(window):
    playlistWindow = window
    cur.execute("SELECT last_name, first_name, song_title FROM songs ORDER BY last_name ASC")
    songs = cur.fetchall()

    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(playlistWindow, height=10, bg = 'red')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()
    
    
    
def filter_by_song(window):
    playlistWindow = window

    cur.execute("SELECT song_title, first_name, last_name FROM songs ORDER BY song_title ASC")
    songs = cur.fetchall()

    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(playlistWindow, height=10, bg = 'red')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()

def filter_by_duration(window):
    playlistWindow = window

    cur.execute("SELECT song_duration, last_name, first_name, song_title FROM songs ORDER BY song_duration DESC")
    songs = cur.fetchall()

    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(playlistWindow, height=10, bg = 'red')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()


def retrieve_new_song(title, first, last, duration, link, username, window):
    titleValue=title.get("1.0","end-1c")
    firstName=first.get("1.0","end-1c")
    lastName=last.get("1.0","end-1c")
    durationValue=duration.get("1.0","end-1c")
    linkValue=link.get("1.0","end-1c")
    usernameValue = username.get("1.0","end-1c")

    try:
        cur.execute("INSERT INTO songs(song_title, first_name, last_name, song_duration, song_link, username) VALUES (%s, %s, %s,%s,%s,%s)", [titleValue, firstName, lastName, durationValue, linkValue, usernameValue])
        conn.commit() 
        messagebox.showinfo("showinfo", "Song Added Successfully!")

    except:
        messagebox.showinfo("showinfo", "Invalid Input or Username")
    
    
def retrieve_song_to_delete(delete):
    titleValue=delete.get("1.0","end-1c")

    cur.execute("DELETE FROM songs WHERE song_title = %s", [titleValue])
    conn.commit()
    
    messagebox.showinfo("showinfo", "Song Deleted Successfully!")
    
def retrieve_user_name(username):
    user=username.get("1.0","end-1c")
    return user
    
def create_user(user, first, last):
    username=user.get("1.0","end-1c")
    firstName=first.get("1.0","end-1c")
    lastName=last.get("1.0","end-1c")
    
    try:
        cur.execute("INSERT INTO users(user_id, user_first, user_last) VALUES (%s, %s, %s)", [username, firstName, lastName])
        conn.commit()
        messagebox.showinfo("showinfo", "User Added Successfully!")

    except:
        messagebox.showinfo("showinfo", "User already exists")

    
def retrieve_duration(dur, window):
    durValue=dur.get("1.0","end-1c")
    durTemp = " "
    if '-' in durValue:
        durTemp = durValue[1:]
        durNum = float(durTemp) * -1
    else: 
        durNum = float(durValue)

    
    cur.execute("SELECT song_title, song_duration FROM songs WHERE song_duration >= %s ORDER BY song_duration ASC", [abs(durNum)])
    goe = cur.fetchall()
    
    cur.execute("SELECT song_title, song_duration FROM songs WHERE song_duration <= %s ORDER BY song_duration ASC", [abs(durNum)])
    loe = cur.fetchall()
    
    songsGreater = []
    for song in goe:
        songsGreater.append(song)
        
    songsLesser = []
    for song in loe:
        songsLesser.append(song)
    
    text = Text(window, height=2, bg = 'pink')

    if '-' in durValue:
        charCount = "1.0"
        temp = 0
        for playSong in songsLesser: 
            text.insert(charCount, playSong)
            text.insert(END, "\n")
            temp = float(charCount)
            temp = temp + 1.0
            temp2 = str(temp)
            charCount = temp2
        text['state'] = 'disabled'
        text.pack()
    else:
        charCount = "1.0"
        temp = 0
        for playSong in songsGreater: 
            text.insert(charCount, playSong)
            text.insert(END, "\n")
            temp = float(charCount)
            temp = temp + 1.0
            temp2 = str(temp)
            charCount = temp2
        text['state'] = 'disabled'
        text.pack()
    
def retrieve_artist(first, last, window):
    firstValue=first.get("1.0","end-1c")
    lastValue=last.get("1.0","end-1c")

    cur.execute("SELECT * FROM songs WHERE first_name = %s and last_name = %s", [firstValue, lastValue])
    songs = cur.fetchall()
    
    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(window, height=5, bg = 'blue')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()
    
def retrieve_title(title, window):
    titleValue=title.get("1.0","end-1c")

    cur.execute("SELECT * FROM songs WHERE song_title = %s", [titleValue])
    songs = cur.fetchall()
    
    cur.execute("SELECT song_link FROM songs WHERE song_title = %s", [titleValue])
    songLink = cur.fetchone()
    
    url = songLink[0]
    
    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(window, height=2, bg = 'magenta')
    charCount = "1.0"
    for s in playlistSongs: 
        text.insert(charCount, s)
        charCount+=charCount
    text['state'] = 'disabled'
    playSong=Button(window, height=1, bg ='magenta', text="Play Song", command=lambda: play_song(url))
    text.pack()
    playSong.pack()

    
def play_song(url):
    os = platform.system()
    
    #For MacOS
    if "Darwin" in os:
        chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
        webbrowser.get(chrome_path).open(url)
        
    #For Windows
    elif "Windows" in os: 
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(url)
        
    #For Linux
    elif "Linux" in os:
        chrome_path = '/usr/bin/google-chrome %s'
        webbrowser.get(chrome_path).open(url)
       
def retrieve_title_and_artist(first, last, title, window):
    firstValue=first.get("1.0","end-1c")
    lastValue=last.get("1.0","end-1c")
    titleValue=title.get("1.0","end-1c")

    cur.execute("SELECT song_title, first_name FROM songs WHERE first_name = %s and last_name = %s and song_title = %s", [firstValue, lastValue, titleValue])
    songs = cur.fetchall()
    
    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(window, height=2, bg = 'pink')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()
  
#CREATES NEW WINDOWS THAT BUTTON CLICKS LEAD TO     
def openPlaylistWindow():
    playlistWindow = Toplevel(gui)
    playlistWindow.config(bg='red')
    playlistWindow.title("Playlist")
    playlistWindow.geometry("600x650+10+20")

    cur.execute('SELECT * from songs')
    songs = cur.fetchall()
    # print(rows)

    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(playlistWindow, height=10, bg = 'red')
    charCount = "1.0"
    temp = 0
    for playSong in playlistSongs: 
        text.insert(charCount, playSong)
        text.insert(END, "\n")
        temp = float(charCount)
        temp = temp + 1.0
        temp2 = str(temp)
        charCount = temp2
    text['state'] = 'disabled'
    text.pack()
    sortA=Button(playlistWindow, height=1, bg ='red', text="sort by artist", command=lambda: filter_by_artist(playlistWindow))
    sortS=Button(playlistWindow, height=1, bg ='red', text="sort by song", command=lambda: filter_by_song(playlistWindow))
    sortD=Button(playlistWindow, height=1, bg ='red', text="sort by duration", command=lambda: filter_by_duration(playlistWindow))
    sortA.pack()
    sortS.pack()
    sortD.pack()

def openMySongsWindow():
    mySongsWindow = Toplevel(gui)
    mySongsWindow.config(bg='black')
    mySongsWindow.title("My Songs")
    mySongsWindow.geometry(geo)

    userName = " "
    login = input("Do you want to login? (Y/N): ")
    if login == "Y" or login == "y":
        userName = input("What is your username?: ")
    else:
        mySongsWindow.destroy()
        mySongsWindow.update()

    cur.execute("SELECT song_title, username, user_first, user_last FROM songs INNER JOIN users u on songs.username = u.user_id WHERE user_id = %s", [userName])
    songs = cur.fetchall()
    # print(rows)

    playlistSongs = []
    for song in songs:
        playlistSongs.append(song)
    
    #Insert songs to be printed for playlist 
    text = Text(mySongsWindow, height=10, bg = 'black')
    charCount = "1.0"
    temp = 0

    if len(playlistSongs) == 0:
        text.insert(charCount, "No Songs to Display")
    else:
        for playSong in playlistSongs: 
            text.insert(charCount, playSong)
            text.insert(END, "\n")
            temp = float(charCount)
            temp = temp + 1.0
            temp2 = str(temp)
            charCount = temp2
    text['state'] = 'disabled'
    text.pack()
    
def openAddSongWindow():
    addSongWindow = Toplevel(gui)
    addSongWindow.config(bg='orange')
    addSongWindow.title("Add Song")
    addSongWindow.geometry(geo)
    songs = []
        
    #Insert songs to be printed for playlist 
    songTitle = Text(addSongWindow, height=1, bg = 'orange', fg = 'black')
    songArtistFirst = Text(addSongWindow, height=1, bg = 'orange',fg = 'black')
    songArtistLast = Text(addSongWindow, height=1, bg = 'orange',fg = 'black')
    songDuration = Text(addSongWindow, height=1, bg = 'orange',fg = 'black')
    songLink = Text(addSongWindow, height=1, bg = 'orange',fg = 'black')
    username = Text(addSongWindow, height=1, bg = 'orange',fg = 'black')


    submitSong=Button(addSongWindow, height=1, bg ='orange', text="submit title", command=lambda: retrieve_new_song(songTitle, songArtistFirst, songArtistLast, songDuration,songLink, username, addSongWindow))
    songTitle.insert("1.0", "enter song title")
    songArtistFirst.insert("1.0", "enter artist first name")
    songArtistLast.insert("1.0", "enter artist last name")
    songDuration.insert("1.0", "enter song duration")
    songLink.insert("1.0", "enter song link")
    username.insert("1.0", "enter your username")

    songTitle.pack()    
    songArtistFirst.pack()
    songArtistLast.pack()
    songDuration.pack()
    songLink.pack()
    username.pack()

    submitSong.pack()
    
def openDeleteSongWindow():
    deleteSongWindow = Toplevel(gui)
    deleteSongWindow.config(bg='yellow')
    deleteSongWindow.title("Delete Song")
    deleteSongWindow.geometry(geo)
    
    songTitleDelete = Text(deleteSongWindow, height=1, bg = 'yellow', fg = 'black')

    submitDelete=Button(deleteSongWindow, height=1, fg = 'black', bg ='orange', text="submit title", command=lambda: retrieve_song_to_delete(songTitleDelete))
    songTitleDelete.insert("1.0", "Enter Title of Song to Delete")
    songTitleDelete.pack()
    submitDelete.pack()

def openSearchDurWindow():
    searchDurWindow = Toplevel(gui)
    searchDurWindow.config(bg='green')
    searchDurWindow.title("Search Duration")
    searchDurWindow.geometry(geo)
    
    searchLessOrGreater = Text(searchDurWindow, height=1, bg = 'green', fg = 'black')

    submitDuration=Button(searchDurWindow, height=1, fg = 'black', bg ='green', text="submit duration", command=lambda: retrieve_duration(searchLessOrGreater, searchDurWindow))
    searchLessOrGreater.insert("1.0", "Enter '1.23' for > 1:23 or '-1.23' for < 1:23")
    searchLessOrGreater.pack()
    submitDuration.pack()
    
def openSearchArtistWindow():
    searchArtistWindow = Toplevel(gui)
    searchArtistWindow.config(bg='blue')
    searchArtistWindow.title("Search Artist")
    searchArtistWindow.geometry(geo)
    
    searchArtistFirst = Text(searchArtistWindow, height=1, bg = 'blue', fg = 'white')
    searchArtistLast = Text(searchArtistWindow, height=1, bg = 'blue', fg = 'white')
    
        
    searchArtistFirst.insert("1.0", "Enter artist first name")
    searchArtistLast.insert("1.0", "Enter artist last name")
    
    artist_first = ""
    artist_last = ""
    
    submitArtist=Button(searchArtistWindow, height=1, fg = 'black', bg ='blue', text="Submit Artist", command=lambda: retrieve_artist(searchArtistFirst, searchArtistLast, searchArtistWindow))

    searchArtistFirst.pack()
    searchArtistLast.pack()
    submitArtist.pack()
    
def openSearchTitleWindow():
    searchTitleWindow = Toplevel(gui)
    searchTitleWindow.config(bg='violet')
    searchTitleWindow.title("Search Title")
    searchTitleWindow.geometry(geo)
    
    searchTitle = Text(searchTitleWindow, height=1, bg = 'violet', fg = 'black')

    submitTitle=Button(searchTitleWindow, height=1, fg = 'black', bg ='violet', text="submit title", command=lambda: retrieve_title(searchTitle, searchTitleWindow))
    searchTitle.insert("1.0", "Enter song title")
    searchTitle.pack()
    submitTitle.pack()
    
def openUserWindow():
    userWindow = Toplevel(gui)
    userWindow.config(bg='white')
    userWindow.title("Search Title")
    userWindow.geometry(geo)
    
    userName = Text(userWindow, height=1, bg = 'white', fg = 'black')
    firstName = Text(userWindow, height=1, bg = 'white', fg = 'black')
    lastName = Text(userWindow, height=1, bg = 'white', fg = 'black')


    createUser=Button(userWindow, height=1, fg = 'black', bg ='white', text="Create My User", command=lambda: create_user(userName, firstName, lastName))
    
    userName.insert("1.0", "Enter Username")
    firstName.insert("1.0", "Enter First Name")
    lastName.insert("1.0", "Enter Last Name")

    userName.pack()
    firstName.pack()
    lastName.pack()
    createUser.pack()
     
def openSearchAandTWindow():
    searchAandTWindow = Toplevel(gui)
    searchAandTWindow.config(bg='pink')
    searchAandTWindow.title("Search By Song and Artist")
    searchAandTWindow.geometry(geo)
   
    searchTitle = Text(searchAandTWindow, height=1, bg = 'pink', fg = 'black')

    searchTitle.insert("1.0", "Enter song title")
    searchTitle.pack()
    
    searchArtistFirst = Text(searchAandTWindow, height=1, bg = 'pink', fg = 'black')
    searchArtistLast = Text(searchAandTWindow, height=1, bg = 'pink', fg = 'black')


    submitArtist=Button(searchAandTWindow, height=1, fg = 'black', bg ='pink', text="Submit Artist", command=lambda: retrieve_title_and_artist(searchArtistFirst, searchArtistLast, searchTitle, searchAandTWindow))
    searchArtistFirst.insert("1.0", "Enter artist first name")
    searchArtistLast.insert("1.0", "Enter artist last name")

    searchArtistFirst.pack()
    searchArtistLast.pack()
    submitArtist.pack()
    
#OPEN NEW WINDOWS
def playlistClicked():
    openPlaylistWindow()

def addSongClicked():
    openAddSongWindow()

def deleteSongClicked():
    openDeleteSongWindow()
    
def searchDurClicked():
    openSearchDurWindow()
    
def searchArtistClicked():
    openSearchArtistWindow()
    
def searchTitleClicked():
    openSearchTitleWindow()
    
def searchAandTClicked():
    openSearchAandTWindow()
    
def createUserClicked():
    openUserWindow()
    
def searchMySongs():
    openMySongsWindow()

#BUTTONS
user=Button(gui, text="Create User", highlightbackground= 'white',fg='black', command=createUserClicked)
user.place(x=200, y=310)

playlist=Button(gui, text="View Playlist",highlightbackground= 'red', fg= 'black', command=playlistClicked)
playlist.place(x=10, y=10)

addSong=Button(gui, text="Add Song",highlightbackground= 'orange', fg= 'black', command=addSongClicked)
addSong.place(x=10, y=110)

deleteSong=Button(gui, text="Delete Song", highlightbackground= 'yellow',fg='black', command=deleteSongClicked)
deleteSong.place(x=10, y=210)

duration=Button(gui, text="Search by Duration", highlightbackground= 'green',fg='black', command=searchDurClicked)
duration.place(x=10, y=310)

artist=Button(gui, text="Search by Artist", highlightbackground= 'blue',fg='black', command=searchArtistClicked)
artist.place(x=200, y=10)

title=Button(gui, text="Search by Title",highlightbackground= 'violet', fg='black', command=searchTitleClicked)
title.place(x=200, y=110)

artistTitle=Button(gui, text="Search by Artist and Title", highlightbackground= 'pink',fg='black', command=searchAandTClicked)
artistTitle.place(x=200, y=210)

mySongs=Button(gui, text="My Songs", highlightbackground= 'lime',fg='black', command=searchMySongs)
mySongs.place(x=10, y=410)


#LOOP CHECKING FOR ACTIVITY 
gui.mainloop()