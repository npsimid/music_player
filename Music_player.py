# importul bibliotecilor
import tkinter as tk
from tkinter import *
from tkinter import filedialog, messagebox
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import sys, os
from random import randint

# Crearea unei functii de blocare a printarii in consola (pentru a exclude mesajele de la pygame)
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Crearea unei functii de deblocare a printarii in consola (dupa ce s-a importat pygame)
def enablePrint():
    sys.stdout = sys.__stdout__

# apelarea functie de blocare a printarii
blockPrint()
# Importul modulului mixer din biblioteca pygame
from pygame import mixer
#apelarea functiei de deblocare a printarii
enablePrint()

# crearea ferestrei root
root=tk.Tk()

# adaugarea unui icon ferestrei
root.iconbitmap("icons/favicon.ico")

# setarea titlului ferestrei
root.title('Music player')

# setarea dimensiunilor ferestrei
root.geometry('500x470')

# blocare redimensionarii ferestrei
root.resizable(0,0)

# setarea culorii ferestrei
root.config(bg="#228B22")

# initierea pachetului mixel pentur lucru cu muzica
mixer.init()

# crearea functiei de determinare a timpului actual al cantecului si a lungimii acestuia
def play_time():
    """
    Functia de determinare a timpului actual al cantecului si a lungimii lui
    """
    if stopped:
        return
    # Determinarea timpului curent in secunde
    timpul_curent=mixer.music.get_pos()/1000
    # determinare cantecului activ
    song = cantec_list.get(ACTIVE)
    # adaugarea intregului directoriu catre cantec activ
    song = f'{path}{song}.mp3'
    # incarcare cantecului cu mutagen
    song_mut=MP3(song)
    # determinarea lungimii cantecului in secunde
    global lung_song
    lung_song=song_mut.info.length
    # conversia lungimii cantecului in format timp
    conv_lung_song = time.strftime('%H:%M:%S', time.gmtime(lung_song))
    # se verifica daca timpul de pe bara nu este egal cu lungimea cantecului
    if int(music_bar.get()) == int(lung_song):
        # daca este egal se afiseaza lungimea cantecului in timpul curent in bara de starea
        status_bar.config(text=f'Timpul scurs: {conv_lung_song} din {conv_lung_song}  ')
        # se afiseaza lungimea cantecului in labelul timpului curent
        start_bar_label.config(text=conv_lung_song)
        # se afiseaza lungimea cantecului in labelul corespunzator
        stop_bar_label.config(text=conv_lung_song)
        # se verifica daca este ultimul cantec din lista si daca sunt dezactivate regimurile de repetare si amestecare
        if cantec_list.curselection()[0]+1==cantec_list.size() and repeat_var == False and random_var==False:
            # se opreste muzica
            stop_song()
        else:
            # se trece la urmatorul cantec
            next_song()
    # se verifica daca cantecul nu este pe pauza
    elif paused:
        pass
    # se verifica daca timpul de pe bara este egal cu timpul curent
    elif int(music_bar.get()) == int(timpul_curent):
        # actualizarea barei cu muzica
        pozitia_bar = int(lung_song)
        music_bar.config(to=pozitia_bar, value=int(timpul_curent))
    else:
        # actualizarea barei cu muzica
        pozitia_bar = int(lung_song)
        music_bar.config(to=pozitia_bar, value=int(music_bar.get()))
        # conversia timpului curent in format timp
        timp_curent_convert = time.strftime('%H:%M:%S', time.gmtime(int(music_bar.get())))
        # Afisare timpului in bara de stare
        status_bar.config(text=f'Timpul scurs: {timp_curent_convert} din {conv_lung_song}  ')
        # se afiseaza tipul in labelul corespunzator
        start_bar_label.config(text=timp_curent_convert)
        # se afiseaza lungimea cantecului in labelul corespunzator
        stop_bar_label.config(text=conv_lung_song)
        # modificarea timpului de pe bara cu o secunda
        next_time=int(music_bar.get())+1
        music_bar.config(value=next_time)
    # actualizarea timpului
    status_bar.after(1000, play_time)

# crearea functiei de adaugare a unui cantec in playlist
def add_song():
    """
    Functia de incarcarea a unui cantec in playlist
    """
    # adaugarea cantecelor prin deschiderea directoriului
    songs=filedialog.askopenfilename(initialdir="Music", title='Adaugare cantece', filetypes=(('mp3 Files' , '*.mp3'),))
    # se creaza o lista in urma divizarii directorului dupa simbolul /
    lista = songs.split("/")
    # se creaza o variabila globala care va reprezenta calea catre folderul cu cantece
    global path
    # se creaza calea din uniunea cu ajutorul simbolului / a tuturor elemtelor liste exceptandul pe ultimul
    path="/".join(lista[0:len(lista)-1])+"/"
    # se creaza denumirea cantecului stergand calea si extensia
    songs1 = songs.replace(path, '').replace(".mp3", '')
    # fixarea cantecelor in lista cu cantece
    cantec_list.insert(END,songs1)
    # se activeaza primul cantec din lista
    cantec_list.selection_set(0)
    # se verifica daca sunt mai mult de 10 cantece
    if cantec_list.size() > 10:
        # se reduce latimea playlist-ului
        cantec_list.config(width=56)
        # se plaseaza playlistul doar pe 2 coloane
        cantec_list.grid(row=4, column=0, columnspan=2, pady=10, sticky=E)
        # se fixeaza scrollbarul in celula eliberata de playlist
        scrollbar.grid(row=4, column=2, sticky="nsw", pady=10)
        # se ataseza scrollbarul la playlist
        cantec_list.config(yscrollcommand=scrollbar.set)
        # se configuraza scrollbarul sa urmareasca lungimea playlistului
        scrollbar.config(command=cantec_list.yview)

# crearea functiei de adaugare mai multor cantece in playlist
def add_songs():
    """
    Functia de incarcarea mai multor cantece in playlist
    """
    # adaugarea cantecelor prin deschiderea directoriului
    songs=filedialog.askopenfilenames(initialdir="Music", title='Adaugare cantece', filetypes=(('mp3 Files' , '*.mp3'),))
    # se selecteaza primul cantec din lista de cantece
    song_0 = songs[0]
    # se creaza o lista in urma divizarii directorului dupa simbolul /
    lista = song_0.split("/")
    # se creaza o variabila globala care va reprezenta calea catre folderul cu cantece
    global path
    # se creaza calea din uniunea cu ajutorul simbolului / a tuturor elemtelor liste exceptandul pe ultimul
    path="/".join(lista[0:len(lista)-1])+"/"
    # se formeaza o bucla cu care se trece prin lista de cantece
    for song in songs:
        # selectarea denumirii cantecului din directoriu cartre acesta
        songs1 = song.replace(path, '').replace(".mp3", '')
        # fixarea cantecelor in lista cu cantece
        cantec_list.insert(END,songs1)
        # se activeaza primul cantec din lista
        cantec_list.selection_set(0)
    # se verifica daca sunt mai mult de 10 cantece
    if cantec_list.size() > 10:
        # se reduce latimea playlist-ului
        cantec_list.config (width = 56)
        # se plaseaza playlistul doar pe 2 coloane
        cantec_list.grid(row=4, column=0, columnspan=2, pady=10, sticky=E)
        # se creaza crollbar-ul
        global scrollbar
        scrollbar = Scrollbar(master_frame)
        # se fixeaza scrollbarul in celula eliberata de playlist
        scrollbar.grid(row=4, column=2, sticky="nsw", pady=10)
        # se ataseza scrollbarul la playlist
        cantec_list.config(yscrollcommand=scrollbar.set)
        # se configuraza scrollbarul sa urmareasca lungimea playlistului
        scrollbar.config(command=cantec_list.yview)

# crearea functiei de stergere a unui cantec din playlist
def del_song():
    """
    Functia de stergere a unui cantec din playlist
    """
    # oprirea cantecului selecta
    stop_song()
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație', message="Nu ați incarcat nici un cântec")
    # stergerea cantecului selectat
    cantec_list.delete(ANCHOR)
    # se verifica daca au ramas mai putin de 10 cantece
    if cantec_list.size() <= 10 and scrollbar.winfo_exists():
        # se distruge srollbar-ul
        scrollbar.destroy()
        # se extinte latimea playlistului
        cantec_list.config(width=60)
        # se plaseaza playlistul pe 3 coloane
        cantec_list.grid(row=4, column=0, columnspan=3, pady=10, sticky=E)

# crearea unui functii de stergere a tuturor cantecelor din playlist
def del_songs():
    """
    Functia de stergere a tuturor cantecelor din playlist
    """
    # oprirea cantecului care canta la moment
    stop_song()
    # stergerea tuturor cantecelor
    cantec_list.delete(0,END)
    # se verifica daca exista crollbar-ul
    if scrollbar.winfo_exists():
        # se distruge srollbar-ul
        scrollbar.destroy()
        # se extinte latimea playlistului
        cantec_list.config(width=60)
        # se plaseaza playlistul pe 3 coloane
        cantec_list.grid(row=4, column=0, columnspan=3, pady=10, sticky=E)

# crearea functiei de pornirea cantecului selectat
def play_song():
    """
    Functia de pornire a cantecului selectat
    """
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație' , message="Nu ați incarcat nici un cântec")
    # Variabila ce specifica ca cantecul este oprit se seteaza in false
    global stopped
    stopped = False
    # Variabila ce specifica ca cantecul este pe pauza se seteaza in false
    global paused
    paused = False

    # Resetarea timpului din bara de stare
    status_bar.config(text='')
    # Resetarea labelului timpului
    start_bar_label.config(text="00:00:00")
    # Stergerea lungimii cantecului anterior
    stop_bar_label.config(text="")
    # Resetarea barei cu muzica
    music_bar.config(value=0)

    # alegerea cantecului selectat
    song=cantec_list.get(ACTIVE)
    # adaugarea intregului directoriu catre cantec
    song = f'{path}{song}.mp3'
    # incarcarea cantelului
    mixer.music.load(song)
    #pornirea cantecului
    mixer.music.play(loops=0)
    #Apelara funtiei de timp pentru a afisa timpul
    play_time()

#setarea unei variabile globale ce va indica cant cantecul este oprit
global stopped
stopped=False
# crearea functiei de oprire a cantecului
def stop_song():
    """
    Functia de oprire a cantecului
    """
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație' , message="Nu ați incarcat nici un cântec")
    # Resetarea timpului din bara de stare
    status_bar.config(text='')
    # Resetarea labelului timpului
    start_bar_label.config(text="00:00:00")
    # Stergerea lungimii cantecului oprit
    stop_bar_label.config(text="")
    # Resetarea barei cu muzica
    music_bar.config(value=0)
    # oprirea cantecului
    mixer.music.stop()
    #setarea variabilei de oprire in true
    global  stopped
    stopped=True

# se creaza o variabila globala ce va fixa faptul ca cantecul este pe pauza
global paused
paused=False

# crearea functiei de punere in pauza a cantecului
def pause_song():
    """
    Functia de pauzare a cantecului
    """
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație' , message="Nu ați incarcat nici un cântec")
    #verificarea daca cantecul este pe pauza
    global paused
    if paused:
        # cantecul se scoate de pe pauza
        mixer.music.unpause()
        # se specifica ca cantecul nu mai e pe pauza
        paused = False
    # se verifica daca cantecul nu este pe pauza
    else:
        # cantecul se scoate de pe pauza
        mixer.music.pause()
        # se specifica ca cantecul e pe pauza
        paused = True

# se creaza o variabila globala care va specifica regimul random
global num_random
num_random= False

# crearea functiei de trecere la urmatorul cantec
def next_song():
    """
    Functia de trecere la urmatorul cantec
    """
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație' , message="Nu ați incarcat nici un cântec")
    # Resetarea timpului din bara de stare
    status_bar.config(text='')
    # Resetarea labelului timpului
    start_bar_label.config(text="00:00:00")
    # Stergerea lungimii cantecului oprit
    stop_bar_label.config(text="")
    # Resetarea barei cu muzica
    music_bar.config(value=0)
    # selectarea unui numar random din numarul cantecelor in playlist
    number = randint(0, cantec_list.size() - 1)
    # se formeaza un tuple cu un element ce corespunde numarului random
    tuple_list=(number,)
    #se cauta daca este vre-un cantec selectat
    try:
        # se verifica daca este activata obtiunea random
        if random_var:
            # numarul urmatorului cantec va fi random
            next_song=tuple_list
        else:
            #vizualizarea numarului de ordine a cantecului selectat
            next_song =cantec_list.curselection()
            # incrementarea numarului de ordine
            next_song = next_song[0]+1
    # daca nu este nici un cantecul selectat
    except IndexError:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație', message="Nu exista nici un cantec activ")
    # se verifica daca cantecul curent este ultimul in lista
    if next_song==cantec_list.size():
        #cantecul urmator va fi primul cantec din lista
        next_song=0
    # determinare cantecului de pe pozitia urmatoare
    song = cantec_list.get(next_song)
    # adaugarea intregului directoriu catre cantec de pe pozitia urmatoare
    song = f'{path}{song}.mp3'
    # incarcarea cantelului de pe pozitia urmatoare
    mixer.music.load(song)
    # pornirea cantecului de pe pozitia urmatoare
    mixer.music.play(loops=0)
    # deselectarea tuturor cantecelor
    cantec_list.selection_clear(0,END)
    # activarea cantecului urmator
    cantec_list.activate(next_song)
    # selectarea urmatorului cantec
    cantec_list.selection_set(next_song, last=None)

# crearea functiei de trecere la cantecul anterior
def previous_song():
    """
    Functia de e trecere la cantecul anterior
    """
    # verificare daca playlist-ul nu este gol
    if cantec_list.size() == 0:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație' , message="Nu ați incarcat nici un cântec")
    # Resetarea timpului din bara de stare
    status_bar.config(text='')
    # Resetarea labelului timpului
    start_bar_label.config(text="00:00:00")
    # Stergerea lungimii cantecului oprit
    stop_bar_label.config(text="")
    # Resetarea barei cu muzica
    music_bar.config(value=0)
    # selectarea unui numar random din numarul cantecelor in playlist
    number = randint(0, cantec_list.size() - 1)
    # se formeaza un tuple cu un element ce corespunde numarului random
    tuple_list = (number,)
    # se verifica daca variabila cu informatie de la checkbox este 1
    if random_var == 1:
        # se seteaza regimul random
        num_random = True
    else:
        # se deconecteaza regimul random
        num_random = False
    # se cauta daca este vre-un cantec selectat
    try:
        # se verifica daca este activata obtiunea random
        if random_var:
            # numarul urmatorului cantec va fi random
            prev_song = tuple_list
        else:
            #vizualizarea numarului de ordine a cantecului selectat
            prev_song =cantec_list.curselection()
            # incrementarea numarului de ordine
            prev_song = prev_song[0]-1
    # daca nu este nici un cantecul selectat
    except IndexError:
        # se afiseaza mesajul de atentionare
        messagebox.showinfo(title='Informație', message="Nu exista nici un cantec activ")
    # se verifica daca cantecul curent este primul in lista
    if prev_song==-1:
        # cantecul anterior se va considera ultimul cantec din lista
        prev_song=cantec_list.size()-1
    # determinare cantecului de pe pozitia urmatoare
    song = cantec_list.get(prev_song)
    # adaugarea intregului directoriu catre cantec de pe pozitia urmatoare
    song = f'{path}{song}.mp3'
    # incarcarea cantelului de pe pozitia urmatoare
    mixer.music.load(song)
    # pornirea cantecului de pe pozitia urmatoare
    mixer.music.play(loops=0)
    # deselectarea tuturor cantecelor
    cantec_list.selection_clear(0,END)
    # activarea cantecului anterior
    cantec_list.activate(prev_song)
    # selectarea urmatorului cantec
    cantec_list.selection_set(prev_song, last=None)

# crearea functiei de deplasare a barei cu muzica
def bar_song(x):
    """
    Functia de deplasare a barei cu muzica
    """
    # alegerea cantecului selectat
    song=cantec_list.get(ACTIVE)
    # adaugarea intregului directoriu catre cantec
    song = f'{path}{song}.mp3'
    # incarcarea cantelului
    mixer.music.load(song)
    #pornirea cantecului
    mixer.music.play(loops=0, start=int(music_bar.get()))

# crearea functiei de reglare a volumului si de afisare a imaginii corespunzatoare nivelului
def volume(x):
    """
    Functia de reglare a volumului si de afisare a imaginii corespunzatoare nivelului
    """
    # seteaza reglarea volumului de la bara
    mixer.music.set_volume(volum_slider.get())
    #se obtine nivelul curent al volumului
    volum_curent = mixer.music.get_volume()*100

    #Schimbarea imagimii pentru volum meter in functie de nivelul acestuia
    if int(volum_curent)<1:
        volum_meter.config(image=vol0)
    elif int(volum_curent)>=1 and int(volum_curent)<=11:
        volum_meter.config(image=vol1)
    elif int(volum_curent)>=12 and int(volum_curent)<=22:
        volum_meter.config(image=vol2)
    elif int(volum_curent)>=23 and int(volum_curent)<=33:
        volum_meter.config(image=vol3)
    elif int(volum_curent)>=34 and int(volum_curent)<=45:
        volum_meter.config(image=vol4)
    elif int(volum_curent)>=45 and int(volum_curent)<=55:
        volum_meter.config(image=vol5)
    elif int(volum_curent)>=56 and int(volum_curent)<=66:
        volum_meter.config(image=vol6)
    elif int(volum_curent)>=67 and int(volum_curent)<=77:
        volum_meter.config(image=vol7)
    elif int(volum_curent)>=78 and int(volum_curent)<=88:
        volum_meter.config(image=vol8)
    elif int(volum_curent)>=89 and int(volum_curent)<=99:
        volum_meter.config(image=vol9)
    elif int(volum_curent) > 99:
        volum_meter.config(image=vol10)

# se creaza o variabila globala care va monitoriza regimul random
global random_var
random_var=False

# crearea functiei de stabilirea a regimului random
def random_song():
    """
        Functia de stabilirea a regimului random
    """
    global random_var
    # se verifica daca nu este regim random
    if not random_var:
        # se modifica imaginea butonului random
        buton_random.config(image=norandom_img)
        # se include regimul random
        random_var = True
    # se verifica daca este regim random
    elif random_var:
        # se modifica imaginea butonului random
        buton_random.config(image=random_img)
        # se deconecteaza regimul random
        random_var = False

# se creaza o variabila globala care va monitoriza regimul repeat
global repeat_var
repeat_var=False

# crearea functiei de stabilirea a regimului repeat
def repeat_song():
    """
        Functia de stabilirea a regimului repeat
    """
    global repeat_var
    # se verifica daca nu este regim repeat
    if not repeat_var:
        # se modifica imaginea butonului repeat
        buton_repeat.config(image=norepeat_img)
        # se include regimul repeat
        repeat_var = True
    # se verifica daca este regim repeat
    elif repeat_var:
        # se modifica imaginea butonului repeat
        buton_repeat.config(image=repeat_img)
        # se deconecteaza regimul repeat
        repeat_var = False

# crearea unui cadru de baza
master_frame=Frame(root, bg="#228B22")
#fixarea cadrului de baza
master_frame.pack()

# crearea unui scrollbar pentru playlist
scrollbar = Scrollbar(master_frame)

# crearea unui listbox pentru playlist
cantec_list=tk.Listbox(master_frame, width=60, bg="#9ACD32", fg="#0000FF", selectbackground='#B22222', activestyle=None)
#fixarea playlist-ului in fereastra
cantec_list.grid(row=4, column=0, columnspan=3, pady=10, sticky=E)

# definirea imaginilor pentru volum meter
vol0=PhotoImage(file="icons/vol0.png")
vol1=PhotoImage(file="icons/vol1.png")
vol2=PhotoImage(file="icons/vol2.png")
vol3=PhotoImage(file="icons/vol3.png")
vol4=PhotoImage(file="icons/vol4.png")
vol5=PhotoImage(file="icons/vol5.png")
vol6=PhotoImage(file="icons/vol6.png")
vol7=PhotoImage(file="icons/vol7.png")
vol8=PhotoImage(file="icons/vol8.png")
vol9=PhotoImage(file="icons/vol9.png")
vol10=PhotoImage(file="icons/vol10.png")

#Crearea label pentru meter
volum_meter = Label(master_frame, image=vol5)
volum_meter.grid(row=0, column=0, columnspan=4, pady=20)

# Label pentru afisarea timpului curent pe bara de muzica
start_bar_label=Label(master_frame, text='00:00:00', bg="#228B22", fg='white')
start_bar_label.grid(row=1, column=0, sticky=W)

# Label pentru afisarea timpului final pe bara de muzica
stop_bar_label=Label(master_frame, text='', bg="#228B22", fg='white')
stop_bar_label.grid(row=1, column=1, columnspan=2, sticky=E)

# crearea barei cu pozitia muzicii
music_bar=ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, length=360, value=0, command=bar_song)
music_bar.grid(row=2, column=0, columnspan=3)

# crearea cadrului pentru butoane
frame=tk.Frame(master_frame, bg="#228B22")
#fixarea cadrului pentru butoanele de manipulare
frame.grid(row=3, column=0, columnspan=3, pady=20)

#Definirea imaginilor pentru butoane
random_img= PhotoImage(file="icons/shuffle30.png")
norandom_img= PhotoImage(file="icons/noshuffle30.png")
previous_img = PhotoImage(file="icons/previous40.png")
play_img = PhotoImage(file="icons/play40.png")
pause_img = PhotoImage(file="icons/pause40.png")
stop_img = PhotoImage(file="icons/stop40.png")
next_img = PhotoImage(file="icons/next40.png")
repeat_img= PhotoImage(file="icons/reapeat30.png")
norepeat_img= PhotoImage(file="icons/noreapeat30.png")

# crearea butoanelor de manipulare
buton_random=tk.Button(frame, image=random_img, borderwidth=0, bg="#228B22", command=random_song)
buton_anterior=tk.Button(frame, image=previous_img, borderwidth=0, bg="#228B22", command=previous_song)
buton_play=tk.Button(frame, image=play_img, borderwidth=0, bg="#228B22", command=play_song)
buton_pauza=tk.Button(frame, image=pause_img, borderwidth=0, bg="#228B22", command=pause_song)
buton_stop=tk.Button(frame, image=stop_img, borderwidth=0, bg="#228B22", command=stop_song)
buton_urmator=tk.Button(frame, image=next_img, borderwidth=0, bg="#228B22", command=next_song)
buton_repeat=tk.Button(frame, image=repeat_img, borderwidth=0, bg="#228B22", command=repeat_song)

# fixarea butoanelor in cadru
buton_random.grid(row=0, column=0, padx=7, sticky=S)
buton_anterior.grid(row=0, column=1, padx=7)
buton_play.grid(row=0, column=2, padx=7)
buton_pauza.grid(row=0, column=3, padx=7)
buton_stop.grid(row=0, column=4, padx=7)
buton_urmator.grid(row=0, column=5, padx=7)
buton_repeat.grid(row=0, column=6, padx=7, sticky=S)

# crearea meniului
meniu=Menu(root)
#Adaugarea meniului la fereastră
root.config(menu=meniu)

# crearea unui submeniu de adaugare cantece
meniu_ad=Menu(meniu)
#adaugarea submeniului la meniu
meniu.add_cascade(label='Adăugare cântece', menu=meniu_ad)
# crearea unui buton in submeniu pentru adaugarea unui singur cantec
meniu_ad.add_command(label='Adăugați un cântec', command = add_song)
# crearea unui buton in submeniu pentru adaugarea mai multor cantece
meniu_ad.add_command(label='Adăugați mai multe cântece', command = add_songs)

# crearea unui submeniu de stergere cantece
meniu_del=Menu(meniu)
#adaugarea submeniului la meniu
meniu.add_cascade(label='Ștergere cântece', menu=meniu_del)
# crearea unui buton in submeniu pentru stergerea unui singur cantec
meniu_del.add_command(label='Ștergeți un cântec', command = del_song)
# crearea unui buton in submeniu pentru stergerea tuturor cantecelor
meniu_del.add_command(label='Ștergeți tot playilist-ul', command = del_songs)

#Crearea barei de stare
status_bar=Label(root, text='', bd=1, relief=GROOVE,anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Crearea unui label in care se va afla bara de volum
volum_frame=LabelFrame(master_frame, text='Volum', bg="#228B22", fg='white')
volum_frame.grid(row=1, column=3, sticky=N, rowspan=4, padx=20)

#Crearea barei de volum
volum_slider=ttk.Scale(volum_frame, from_=1, to=0, orient=VERTICAL, length=286, value=0.5, command=volume)
volum_slider.pack(pady=0)

# crearea buclei de afisare permanenta
root.mainloop()