from ast import Lambda
import json
from msilib.schema import ComboBox, RadioButton
from multiprocessing import connection
from sqlite3 import *
from sqlite3 import Error
import tkinter as tk
from tkinter import IntVar, ttk
from os import *
from tkinter import messagebox
from tkinter.messagebox import showerror, showwarning, showinfo

def connect_to_db(path: str):
    connection = None
    try:
        connection =connect(path)
        print("Connected was successful")
    except Error as e:
        print(f'Tekkis viga: {e}')
    return connection

def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        print("Tabel created")
    except Error as e:
        print(f'Tekkis viga: {e}')

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    except Error as e:
        print(f'Tekkis viga: {e}')





create_table_autorid = """
CREATE TABLE IF NOT EXISTS autorid(
autor_id INTEGER PRIMARY KEY AUTOINCREMENT,
autor_nimi TEXT NOT NULL,
sunnikuupaev date NOT NULL)
"""

create_table_zanrid = """
CREATE TABLE IF NOT EXISTS zanrid(
zanr_id INTEGER PRIMARY KEY AUTOINCREMENT,
zanri_nimi TEXT NOT NULL)
"""

create_table_raamatud = """ 
CREATE TABLE IF NOT EXISTS raamatud(
raamatu_id INTEGER PRIMARY KEY AUTOINCREMENT,
pealkiri TEXT NOT NULL,
valjaandmise_kuup date NOT NULL,
autor_id INTEGER NOT NULL,
zanr_id INTEGER NOT NULL,
FOREIGN KEY (autor_id) REFERENCES autorid(autor_id),
FOREIGN KEY (zanr_id) REFERENCES zanrid(zanr_id)
)
"""

insert_autorid = """
INSERT INTO autorid(autor_nimi, sunnikuupaev) 
VALUES ("Pushkin", '1799-06-06'),
       ("Jessenin", '1895-10-03'),
       ("Majakovski", '1893-07-19'),
       ("Lermontov", '1814-10-15');
"""

insert_zanrid = """
INSERT INTO zanrid(zanri_nimi)
VALUES("Draama"),
("Detektiiv"),
("Romaan"),
("Komöödia"),
("luuletus"),
("Ballada")
"""

insert_raamatud = """
INSERT INTO raamatud(pealkiri, valjaandmise_kuup, autor_id, zanr_id)
VALUES("Jevgeni Onegin", 1833, 1, 3),
("Dubrovski", 1841, 1, 3),
("Borodino", 1837, 4, 6),
("Pugachev", 1921, 2, 1)
"""

filename = path.abspath(__file__)
dbdir = filename.rsplit("Andmebaas.py")
current_dir = getcwd()
dbpath = path.join(current_dir, "data.db")
conn = connect_to_db(dbpath)





drop_table_raamatud = """
DROP TABLE IF EXISTS raamatud
"""

drop_table_autors = """
DROP TABLE IF EXISTS autorid
"""
drop_table_zanr ="""
DROP TABLE IF EXISTS zanrid
"""



execute_query(conn, drop_table_raamatud)
execute_query(conn, drop_table_autors)
execute_query(conn, drop_table_zanr)

execute_query(conn, create_table_autorid)
execute_query(conn, create_table_zanrid)
execute_query(conn, create_table_raamatud)

execute_query(conn, insert_autorid)
execute_query(conn, insert_zanrid)
execute_query(conn, insert_raamatud)

select_raamatud = """SELECT * FROM raamatud"""
select_autors = """SELECT * FROM autorid"""
select_zanrid = """SELECT * FROM zanrid"""



raamatud = execute_read_query(conn, select_raamatud)
autors = execute_read_query(conn, select_autors)
zanrid = execute_read_query(conn, select_zanrid)


print("-------------- TABEL AUTHORS --------------")
for autor in autors:
    print(autors)
print("-------------- TABEL ZANRID --------------")
for zanr in zanrid:
    print(zanrid)
print("-------------- TABEL RAAMATUD --------------")
for raamat in raamatud:
    print(raamat)




root = tk.Tk()
root.title("RAAMATUKOGU ANDMEBAASIL")
tree = ttk.Treeview(root, column= ("c1", "c2", "c3", "c4", "c5"), show ="headings")
tree.column("#1", anchor=tk.CENTER)
tree.heading("#1", text = "ID")
tree.column("#2", anchor=tk.CENTER)
tree.heading("#2", text = "pealkiri")
tree.column("#3", anchor=tk.CENTER)
tree.heading("#3", text = "valjaandmise_kuup")
tree.column("#4", anchor=tk.CENTER)
tree.heading("#4", text = "autor_id")
tree.column("#5", anchor=tk.CENTER)
tree.heading("#5", text = "zanr_id")

tree.pack()


def clear_all():
    for i in tree.get_children():
        tree.delete(i)

def zanr_tabeli():
    root = tk.Tk()
    root.title("Tabel 'Zanrid'")
    tree = ttk.Treeview(root, column= ("c1", "c2"), show ="headings")
    tree.column("#1", anchor=tk.CENTER)
    tree.heading("#1", text = "ID")
    tree.column("#2", anchor=tk.CENTER)
    tree.heading("#2", text = "Zanri nimi")
    tree.pack()
    con1 = connect(dbpath)
    cur1 = con1.cursor()
    cur1.execute(f'SELECT * FROM zanrid')
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values = row)
    con1.close()

    root.mainloop()
    
   


def autors_tabeli():
    root = tk.Tk()
    root.title("Tabel 'Raamatud'")
    tree = ttk.Treeview(root, column= ("c1", "c2", "c3"), show ="headings")
    tree.column("#1", anchor=tk.CENTER)
    tree.heading("#1", text = "ID")
    tree.column("#2", anchor=tk.CENTER)
    tree.heading("#2", text = "autor_nimi")
    tree.column("#3", anchor=tk.CENTER)
    tree.heading("#3", text = "sunnikuupaev")
    tree.pack()
    con1 = connect(dbpath)
    cur1 = con1.cursor()
    cur1.execute("SELECT * FROM autorid ")
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values = row)
    con1.close()

    root.mainloop()



def andmed(tabel: str):
    con1 = connect(dbpath)
    cur1 = con1.cursor()
    cur1.execute(f'SELECT * FROM {tabel}')
    rows = cur1.fetchall()
    for row in rows:
        print(row)
        tree.insert("", tk.END, values = row)
    con1.close()

  
    
def lisa_andmed_zanrid():
    

    #def on_button_click():
       # selected_year = spinbox.get()

    
    def lisa_andmed_destroy():
        root1.destroy()

    def insert():
        zanr_nimi_value = zanr_nimi.get()

        insert_query = "INSERT INTO zanrid (zanri_nimi) VALUES (?)"

        cursor = conn.cursor()
        cursor.execute(insert_query, (zanr_nimi_value,))

        conn.commit()

        cursor.close()
    
    def all():
        insert()
        lisa_andmed_destroy()
        


    root1 = tk.Tk()
    root1.title("Lisa andmeid zanrisse") 
    root1.geometry('600x600')

    

    zanrr = tk.Label(
        root1, 
        text="Zanri lisamine",
        font = "Arial 35"
        )
    zanrr.pack()
    
    zanr_ = tk.Label(
        root1,
        text = "Sisesta zanr nimi: ",
        font = "Arial 12"
        )
    zanr_.place(x = 100, y = 69)

    zanr_nimi = tk.Entry(
        root1
        )
    zanr_nimi.place(x = 100, y = 100)

    lisada = tk.Button(
        root1,
        text = "Lisada",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 150)






def lisa_andmed_raamatud():
    

    #def on_button_click():
       # selected_year = spinbox.get()

    
    def lisa_andmed_destroy():
        root1.destroy()

    def insert():
        pealkiri_value = pealkiri.get()
        valjaandmise_value = valjaandmise_kuup.get()
        autor_id_value = autor_id.get()
        zanr_id_value = zanr_id.get()
        if pealkiri_value.isalnum():
            showinfo(title="Добавление книги", message="Добавление произошло успешно!")
        else:
            showerror(title="Ошибка", message="Введите год выпуска книги корректно!")

        # if zanr_id_value in zanr:
        #     showinfo(title="Добавление книги", message="Добавление произошло успешно!")
        # else:
        #     showerror(title="Ошибка", message="Введите год выпуска книги корректно!")

        insert_query = "INSERT INTO raamatud (pealkiri, valjaandmise_kuup, autor_id, zanr_id) VALUES (?, ?, ?, ?)"

        cursor = conn.cursor()
        cursor.execute(insert_query, (pealkiri_value, valjaandmise_value, autor_id_value, zanr_id_value,))

        conn.commit()

        cursor.close()

        
    def all():
        insert()
        lisa_andmed_destroy()



    root1 = tk.Tk()
    root1.title("Lisa andmeid raamatuid") 
    root1.geometry('600x600')

    

    raamatudd = tk.Label(
        root1, 
        text="Raamatu lisamine",
        font = "Arial 35"
        )
    raamatudd.pack()
    

    raamat_ = tk.Label(
        root1,
        text = "Sisesta raamatu pealkiri: ",
        font = "Arial 12"
        )
    raamat_.place(x = 100, y = 69)

    pealkiri = tk.Entry(
        root1
        )
    pealkiri.place(x = 300, y = 73)



    valjaandmise_kuup_ = tk.Label(
        root1,
        text = "Sisesta valjaandmise kuupäev: ",
        font = "Arial 12"
        )
    valjaandmise_kuup_.place(x = 100, y = 99)

    valjaandmise_kuup = tk.Entry(
        root1
        )
    valjaandmise_kuup.place(x = 330, y = 104)



    autor_id_ = tk.Label(
        root1,
        text = "Sisesta autori id: ",
        font = "Arial 12"
        )
    autor_id_.place(x = 100, y = 129)

    autor_id = tk.Entry(
        root1
        )
    autor_id.place(x = 240, y = 133)



    zanr_id_ = tk.Label(
        root1,
        text = "Sisesta zanri id: ",
        font = "Arial 12"
        )
    zanr_id_.place(x = 100, y = 159)

    zanr_id = tk.Entry(
        root1
        )
    zanr_id.place(x = 240, y = 162)
    



    lisada = tk.Button(
        root1,
        text = "Lisada",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 250)





def lisa_andmed_autorid():
    

    #def on_button_click():
       # selected_year = spinbox.get()
    
    
    def lisa_andmed_destroy():
        root1.destroy()

    def insert():
        
        autor_nimi_value = autor_nimi.get()
        sunnikuupaev_value = sunnikuupaev__.get()

        if autor_nimi_value.isalpha():
            showinfo(title="Добавление автора", message="Добавление произошло успешно!")
        else:
            showerror(title="Ошибка", message="Введите имя автора корректно!")




        insert_query = "INSERT INTO autorid (autor_nimi, sunnikuupaev) VALUES (?, ?)"

        cursor = conn.cursor()
        cursor.execute(insert_query, (autor_nimi_value, sunnikuupaev_value,))

        conn.commit()

        cursor.close()




    def all():
        insert()
        lisa_andmed_destroy()




    root1 = tk.Tk()
    root1.title("Lisa andmeid Autorisse") 
    root1.geometry('600x600')

    

    autoridd = tk.Label(
        root1, 
        text="Autorid lisamine",
        font = "Arial 35"
        )
    autoridd.pack()
    
    autor_ = tk.Label(
        root1,
        text = "Sisesta Autor nimi: ",
        font = "Arial 12"
        )
    autor_.place(x = 100, y = 69)

    sunnikuupaev_ = tk.Label(
        root1,
        text = "Sisesta autori sunniaeg (YEAR-M-D): ",
        font = "Arial 12"
        )
    sunnikuupaev_.place(x = 100, y = 100)

    autor_nimi = tk.Entry(
        root1
        )
    autor_nimi.place(x = 300, y = 72)

    sunnikuupaev__ = tk.Entry(
        root1
        )
    sunnikuupaev__.place(x = 367, y = 102)


    lisada = tk.Button(
        root1,
        text = "Lisada",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 150)



    root1.mainloop()


def delete_andmed_raamatud():

    def lisa_andmed_destroy():
        root.destroy()

    def delete():
        
        raamatu_id_value = raamatuu_id.get()

        insert_query = "DELETE FROM raamatud where raamatu_id = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (raamatu_id_value,))

        conn.commit()
        for raamatu in raamatud:
            print(raamatu)
        cursor.close()

    def all():
        delete()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Kustuta andmed tabelist 'Raamatud'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    Raamatud = tk.Label(
        root, 
        text="Raamatu kustutamine",
        font = "Arial 35"
        )
    Raamatud.place(x = 180, y = 20)


    raamatu_text = tk.Label(
        root,
        text = "Sisesta raamatu id: ",
        font = "Arial 12"
        )
    raamatu_text.place(x = 100, y = 100)

    raamatuu_id = tk.Entry(
        root
        )
    raamatuu_id.place(x = 245, y = 100)

    lisada = tk.Button(
        root,
        text = "Kustata",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 150)



    root.mainloop()





def delete_andmed_autorid():

    def lisa_andmed_destroy():
        root.destroy()

    def delete():
        
        autorid_id_value = autoridd_id.get()

        insert_query = "DELETE FROM autorid where autor_id = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (autorid_id_value,))

        conn.commit()

        cursor.close()

    def all():
        delete()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Kustuta andmed tabelist 'Autorid'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    Autorid = tk.Label(
        root, 
        text="Autori kustutamine",
        font = "Arial 35"
        )
    Autorid.place(x = 180, y = 20)


    autori_text = tk.Label(
        root,
        text = "Sisesta autori id: ",
        font = "Arial 12"
        )
    autori_text.place(x = 100, y = 100)

    autoridd_id = tk.Entry(
        root
        )
    autoridd_id.place(x = 245, y = 100)

    lisada = tk.Button(
        root,
        text = "Kustuta",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 150)



    root.mainloop()



def delete_andmed_zanrid():

    def lisa_andmed_destroy():
        root.destroy()

    def delete():
        
        zanri_id_value = zanri_id.get()

        insert_query = "DELETE FROM zanrid where zanr_id = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (zanri_id_value,))

        conn.commit()

        cursor.close()

    def all():
        delete()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Kustuta andmed tabelist 'Autorid'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    zanrid = tk.Label(
        root, 
        text="Zanri kustutamine",
        font = "Arial 35"
        )
    zanrid.place(x = 180, y = 20)


    zanri_text = tk.Label(
        root,
        text = "Sisesta zanri id: ",
        font = "Arial 12"
        )
    zanri_text.place(x = 100, y = 100)

    zanri_id = tk.Entry(
        root
        )
    zanri_id.place(x = 245, y = 100)

    lisada = tk.Button(
        root,
        text = "Kustuta",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 100, y = 150)



    root.mainloop()




def update_raamatud():


    def lisa_andmed_destroy():
        root.destroy()

    def updates():
        
        pealkiri_value = pealkiri.get()
        pealkiri_change_value = newPealkiri.get()


        insert_query = "UPDATE raamatud SET pealkiri = ? where pealkiri = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (pealkiri_change_value, pealkiri_value,))

        conn.commit()

        cursor.close()

    def all():
        updates()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Muuda pealkiri tabelis 'Raamatud'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    raamat = tk.Label(
        root, 
        text="Pealkiri muuda",
        font = "Arial 35"
        )
    raamat.place(x = 180, y = 20)


    vanaPealkiri_text = tk.Label(
        root,
        text = "Vana raamatu pealkiri: ",
        font = "Arial 12"
        )
    vanaPealkiri_text.place(x = 100, y = 100)

    pealkiri = tk.Entry(
        root
        )
    pealkiri.place(x = 265, y = 102)

    uusPealkiri_text = tk.Label(
        root,
        text = "Uue raamatu pealkiri: ",
        font = "Arial 12"
        )
    uusPealkiri_text.place(x = 100, y = 130)

    newPealkiri = tk.Entry(
        root
        )
    newPealkiri.place(x = 265, y = 134)
    


    lisada = tk.Button(
        root,
        text = "Muuda",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 200, y = 260)



    root.mainloop()




def update_zanrid():


    def lisa_andmed_destroy():
        root.destroy()

    def updates():
        
        zanri_nimi_value = zanrii_nimi.get()
        zanri_nimi_change_value = newZanri_nimi.get()


        insert_query = "UPDATE zanrid SET zanri_nimi = ? where zanri_nimi = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (zanri_nimi_change_value, zanri_nimi_value,))

        conn.commit()

        cursor.close()

    def all():
        updates()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Muuda pealkiri tabelis 'Zanrid'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    zanrr = tk.Label(
        root, 
        text="Zanri muuda",
        font = "Arial 35"
        )
    zanrr.place(x = 180, y = 20)


    zanri_nimi_text = tk.Label(
        root,
        text = "Vana zanri nimi: ",
        font = "Arial 12"
        )
    zanri_nimi_text.place(x = 100, y = 100)

    zanrii_nimi = tk.Entry(
        root
        )
    zanrii_nimi.place(x = 265, y = 102)

    newZanri_nimi_text = tk.Label(
        root,
        text = "Uue zanri nimi: ",
        font = "Arial 12"
        )
    newZanri_nimi_text.place(x = 100, y = 130)

    newZanri_nimi = tk.Entry(
        root
        )
    newZanri_nimi.place(x = 265, y = 134)
    


    lisada = tk.Button(
        root,
        text = "Muuda",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 200, y = 260)



    root.mainloop()



def update_autorid():
    def lisa_andmed_destroy():
        root.destroy()

    def updates():
        
        autor_nimi_value = autori_nimi.get()
        autor_nimi_change_value = newAutori_nimi.get()


        insert_query = "UPDATE autorid SET autor_nimi = ? where autor_nimi = ?"

        cursor = conn.cursor()
        cursor.execute(insert_query, (autor_nimi_change_value, autor_nimi_value,))

        conn.commit()

        cursor.close()

    def all():
        updates()
        lisa_andmed_destroy()

    root = tk.Tk()
    root.title("Muuda pealkiri tabelis 'Autorid'")
    canvas = tk.Canvas(root, width = 600, height = 400)
    canvas.pack()
    

    autorr = tk.Label(
        root, 
        text="Autori muuda",
        font = "Arial 35"
        )
    autorr.place(x = 180, y = 20)


    autori_nimi_text = tk.Label(
        root,
        text = "Vana autori nimi: ",
        font = "Arial 12"
        )
    autori_nimi_text.place(x = 100, y = 100)

    autori_nimi = tk.Entry(
        root
        )
    autori_nimi.place(x = 265, y = 102)

    newAutori_nimi_text = tk.Label(
        root,
        text = "Uue autori nimi: ",
        font = "Arial 12"
        )
    newAutori_nimi_text.place(x = 100, y = 130)

    newAutori_nimi = tk.Entry(
        root
        )
    newAutori_nimi.place(x = 265, y = 134)
    


    lisada = tk.Button(
        root,
        text = "Muuda",
        height = 4,
        width = 7,
        command = lambda: all()
        )
    lisada.place(x = 200, y = 260)



    root.mainloop()



def all_lisamine():

    root = tk.Tk()
    root.title("Lisamine andmeid")
    canvas = tk.Canvas(root, width = 500, height = 500)
    canvas.pack()

    def destroy_window():
        root.destroy()

    def all1():
        destroy_window()
        lisa_andmed_raamatud()
        

    def all2():
        destroy_window()
        lisa_andmed_autorid()
        
    def all3():
        destroy_window()
        lisa_andmed_zanrid()

    but1 = tk.Button(
        root,
        text = "Lisa andmed tabelisse 'Raamatud' ",
        command = lambda: all1()
        )
    but1.place(x = 100, y = 100)

    but2 = tk.Button(
        root,
        text = "Lisa andmed tabelisse 'Autorid'",
        command = lambda: all2()
        )
    but2.place(x = 100, y = 130)
    but3 = tk.Button(
        root,
        text = "Lisa andmed tabelisse 'Zanrid'",
        command = lambda: all3()
        )
    but3.place(x = 100, y = 160)

    root.mainloop()

def all_delete():


    root = tk.Tk()
    root.title("Kustuta andmeid")
    canvas = tk.Canvas(root, width = 500, height = 500)
    canvas.pack()

    def destroy_window():
        root.destroy()

    def all1():
        destroy_window()
        delete_andmed_raamatud()
        

    def all2():
        destroy_window()
        delete_andmed_autorid()
        
    def all3():
        destroy_window()
        delete_andmed_zanrid()

    but1 = tk.Button(
        root,
        text = "Kustuta andmed tabelist 'Raamatud' ",
        command = lambda: all1()
        )
    but1.place(x = 100, y = 100)

    but2 = tk.Button(
        root,
        text = "Kustuta andmed tabelist 'Autorid'",
        command = lambda: all2()
        )
    but2.place(x = 100, y = 130)
    but3 = tk.Button(
        root,
        text = "Kustuta andmed tabelist 'Zanrid'",
        command = lambda: all3()
        )
    but3.place(x = 100, y = 160)

    root.mainloop()




def all_updates():
    root = tk.Tk()
    root.title("Muuda andmeid")
    canvas = tk.Canvas(root, width = 500, height = 500)
    canvas.pack()

    def destroy_window():
        root.destroy()

    def all1():
        destroy_window()
        update_raamatud()
        

    def all2():
        destroy_window()
        update_autorid()
        
    def all3():
        destroy_window()
        update_zanrid()
        
    but1 = tk.Button(
        root,
        text = "Muuda andmed tabelisse 'Raamatud' ",
        command = lambda: all1()
        )
    but1.place(x = 100, y = 100)

    but2 = tk.Button(
        root,
        text = "Muuda andmed tabelisse 'Autorid'",
        command = lambda: all2()
        )
    but2.place(x = 100, y = 130)
    but3 = tk.Button(
        root,
        text = "Muuda andmed tabelisse 'Zanrid'",
        command = lambda: all3()
        )
    but3.place(x = 100, y = 160)

    root.mainloop()



label = tk.Label(root, text="Sisestage tabel: ")

label.pack(pady=10)

#entry = tk.Entry(root, width=30)
#entry.pack(pady=10)

#button = tk.Button(root, text="Näitus on sisestatud", command= lambda: andmed())
#button.pack(pady=10)    

btn = tk.Button(text = "TABEL 'RAAMATUD'", command = lambda: andmed("raamatud"))
btn.pack(pady=10)
btn = tk.Button(text = "TABEL 'ZANRID'", command = lambda: zanr_tabeli())
btn.pack(pady=10)
btn = tk.Button(text = "TABEL 'AUTORID'", command = lambda: autors_tabeli())
btn.pack(pady=10)
btn = tk.Button(text = "CLEAR", command = lambda: clear_all())
btn.pack(pady = 10, padx=20)

btn = tk.Button(text = "lisa andmed tabelist'", command = lambda: all_lisamine())
btn.pack(pady = 10)

btn = tk.Button(text = "Kustuta tabeli", command = lambda: all_delete())
btn.pack(pady = 10)

btn = tk.Button(text = "Muuda tabeli", command = lambda: all_updates())
btn.pack(pady = 10)

root.mainloop()
