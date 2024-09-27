from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter.messagebox import showerror
import datetime

root = Tk()
root.title("Фильмы")
root.geometry('200x50')
root.resizable(0, 0)
window = None
filename = 'movies.txt'
first_movie = datetime.date(1896, 1, 25)

class Movie:
    frame = None
    title = None
    date = None
    def __init__(self, f, t, d):
        self.frame = f
        self.title = t
        self.date = d

class Window(Tk):
    index = 0
    
    def __init__(self, t, d, i):
        super().__init__()

        self.title('Изменить фильм')
        self.geometry("250x200")
        self.index = i
        self.entry = ttk.Entry(self)
        self.entry.insert(0, t)
        self.entry.grid(row = 0, column = 0)
        self.de = DateEntry(self, date_pattern='dd/mm/YYYY')
        str_arr = d.split('-')
        d_str = ''
        for s in str_arr:
            d_str += s
        self.de.set_date(datetime.datetime.strptime(d_str, '%Y%m%d'))
        self.de.grid(row = 0, column = 1)
        self.confirm_btn = ttk.Button(self, text = 'Подтвердить', command = self.update_button_clicked)
        #self.confirm_btn.bind('<Button-1>', lambda e, t = entry.get(), d = str(de.get_date(), ind = i)
        self.confirm_btn.grid(row = 1, column = 0)
        self.delete_btn = ttk.Button(self, text = 'Удалить', command = self.delete_button_clicked)
        self.delete_btn.grid(row = 1, column = 1)
 
    def update_button_clicked(self):
        movie_list[self.index].title = self.entry.get()
        movie_list[self.index].date = str(self.de.get_date())
        if movie_list[self.index].title.split() != [] and self.de.get_date() >= first_movie: 
            fread = open(filename, 'r', encoding = 'utf-8')
            lines = fread.readlines()
            fread.close()
            fw = open(filename, 'w', encoding = 'utf-8')
            for i in range(len(lines)):
                if i == self.index:
                    fw.write(str(self.de.get_date()))
                    fw.write(' ')
                    fw.write(self.entry.get())
                else:
                    fw.write(lines[i])
            fw.close()
            update_list()
            self.destroy()
        else:
            showerror(title="Ошибка", message="Не введено название фильма, или дата выхода не корректна.")

    def delete_button_clicked(self):
        #movie_list[self.index].title['text'] = self.entry.get()
        #movie_list[self.index].date['text'] = str(self.de.get_date())
        fread = open(filename, 'r', encoding = 'utf-8')
        lines = fread.readlines()
        fread.close()
        fw = open(filename, 'w', encoding = 'utf-8')
        print(len(lines), self.index)
        for i in range(len(lines)):
            if i != self.index:
                fw.write(lines[i])
        fw.close()
        update_list()
        self.destroy()
        
def add_movie():
    title = entry.get()
    date = de.get_date()
    if not title or title.split() == []:
        showerror(title="Ошибка", message="Введите название")
    elif date < first_movie:
        showerror(title="Ошибка", message="Введите корректную дату")
    else:
        try:
            fread = open(filename, 'r')
            fwrite = open(filename, 'a', encoding = 'utf-8')
            ch = fread.read(1)
            last = ''
            while ch != '':
                last = ch
                ch = fread.read(1)
            fread.close()
            if last != '\n' and last != '':
                fwrite.write('\n')
            fwrite.write(str(de.get_date()))
            fwrite.write(' ')
            fwrite.write(title)
            fwrite.close()
        except:
            showerror(title="Ошибка", message="Не удалось добавить фильм")

def update_list():
    if frame1 != None:
        for widget in frame1.winfo_children():
           widget.destroy()
    f = open(filename, encoding = 'utf-8')
    Lines = f.readlines()
    f.close()
    index = 0
    max_len = 0
    for line in Lines:
        date, name = line.split(None, 1)
        if len(name) > max_len:
            max_len = len(name)
        movie = ttk.Frame(frame1)
        #print(name, date)
        title_lbl = ttk.Label(movie, text = name)
        date_lbl = ttk.Label(movie, text = date)
        upd = ttk.Button(movie, text = 'Редактировать')
        movie_list.append(Movie(movie, title_lbl, date_lbl))
        upd.bind('<Button-1>', lambda e, t = title_lbl['text'], d = date_lbl['text'], i = index: edit(e, t, d, i))
        index += 1
        movie.grid(row = index)
        title_lbl.grid(row = 0, column = 0)
        date_lbl.grid(row = 0, column = 1)
        upd.grid(row = 0, column = 2)
    if index != 0:
        x = str(230 + max_len * 5)
        y = str(index * 35 + 60)
        root.geometry(x + 'x' + y)
    else:
        root.geometry('230x100')
        
    upd_button = ttk.Button(frame1, text = 'Обновить', command = update_list)
    upd_button.grid()

def edit(event, t, d, i):
    window = Window(t, d, i)
    window.geometry("250x75")
    window.resizable(0, 0)

notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)

entry = ttk.Entry(frame2)
entry.grid(row = 0, column = 0)
#cal = Calendar(frame2, selectmode = 'day')
#cal.pack()
de = DateEntry(frame2, date_pattern='dd/mm/YYYY')
de.grid(row = 0, column = 1)
confirm_btn = ttk.Button(frame2, text = 'Подтвердить', command = add_movie)
confirm_btn.grid(row = 1, column = 0)

movie_list = []
update_list()

frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)
 
notebook.add(frame1, text="Список фильмов")
notebook.add(frame2, text="Добавить фильм")

root.mainloop()
