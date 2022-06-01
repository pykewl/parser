import tkinter
from tkinter import *
import pymorphy2
import requests
from io import BytesIO
from PIL import Image, ImageTk
from pprint import pprint

import PIL.Image
import concurrent.futures



ans = requests.get(url=f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing',
                        stream=True
        ).json()
lst = []
for i in ans['data']['cryptoCurrencyList']:
    lst.append(i['symbol'])


def check_input(_event=None):
    value = entry.get().lower()

    if value == '':
        listbox_values.set(lst)
    else:
        data = []
        for item in lst:
            if value.lower() in item.lower():
                data.append(item)

        listbox_values.set(data)


def on_change_selection(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        a = event.widget.get(index)
        entry_text.set(a)
        check_input()
    curr = a.lower()

    for item in ans['data']['cryptoCurrencyList']:
        if curr in item['symbol'].lower() == curr:
            lbl.configure(text=(f"{item['name']}({item['symbol']})"))
            lbl2.configure(text=(f"{round(item['quotes'][0]['price'], 2)}$"))
            lbl3.configure(text=(f"{round(item['quotes'][0]['percentChange1h'], 4)}%"))
            lbl6.configure(text=(f"Дополнительная информация:\n Количество монет - {round(item['totalSupply'], 1)}\n Рыночная капитализация - {round(item['quotes'][0]['marketCap'], 1)}USD"))
            color_change = item['quotes'][0]['percentChange1h']
            col_ch(color_change)
            entry.delete(0, END)
            check_input()

    for item in ans['data']['cryptoCurrencyList']:
        if curr in item.get('symbol').lower() == curr:
            r = requests.get(url=f'https://s2.coinmarketcap.com/static/img/coins/64x64/{item.get("id")}.png')
            pil_image = Image.open(BytesIO(r.content))
            pil_image.save(BytesIO(), format='PNG')
            pil_image.thumbnail((64, 64))

            img = ImageTk.PhotoImage(pil_image)
            Label1 = tkinter.Label(image=img)
            Label1.image = img
            Label1.place(x=55, y=330)


def col_ch(color_change):
    if color_change > 0:
        lbl2.configure(fg='green')
        lbl3.configure(fg='green')
    elif color_change == 0:
        lbl2.configure(fg='black')
        lbl3.configure(fg='black')
    elif color_change < 0:
        lbl2.configure(fg='red')
        lbl3.configure(fg='red')


root = Tk()

root.title('Crypto parser')
root.geometry('500x540')
root['background']

lbl5 = Label(root, text="")
lbl5.pack()

lbl4 = Label(root, text="Введите название криптовалюты или выберите ее из списка\n", font=("Arial Black", 10), fg = 'grey')
lbl4.pack()

entry_text = StringVar()
entry = Entry(root, textvariable=entry_text, bd =5, relief = 'groove', width= 22 , font=("Arial Black", 10))
entry.bind('<KeyRelease>', check_input)
entry.pack()

my_frame = Frame(root)
my_scrollbar = Scrollbar(my_frame)

listbox_values = Variable()
listbox = Listbox(my_frame, listvariable=listbox_values, height=10, yscrollcommand=my_scrollbar.set, bd =5, relief = 'groove', font=("Arial Black", 10))
listbox.bind('<<ListboxSelect>>', on_change_selection)
listbox.pack(side = LEFT, fill =X)
listbox_values.set(lst)

my_scrollbar.config(command=listbox.yview)
my_scrollbar.pack(side = RIGHT, fill =Y)
my_frame.pack()


lbl = Label(root, text=" ", font=("Arial Black", 25))
lbl.place(x=150,y=310)

lbl2 = Label(root, text=" ", font=("Arial Black", 25))
lbl2.place(x=150,y=360)


lbl3 = Label(root, text=" ", font=("Arial Black", 10))
lbl3.place(x=350,y=380)

lb = Listbox(root, height = 5, width= 72, bd= 5, relief = 'groove')
lb.place(x=30,y=440)

lbl6 = Label(root, text=" ", font=("Arial Black", 10), bg= 'white')
lbl6.place(x=60,y=455)

root.mainloop()

