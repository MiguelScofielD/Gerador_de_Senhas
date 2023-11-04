from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    caracteres = []
    for letter in range(4):
        caracteres.append(letters[random.randint(0, len(letters) - 1)])

    for number in range(4):
        caracteres.append(numbers[random.randint(0, len(numbers) - 1)])

    for symbol in range(4):
        caracteres.append(symbols[random.randint(0, len(symbols) - 1)])

    random.shuffle(caracteres)
    str = ""

    for i in caracteres:
        str += i

    entry_password.insert(0,str)
    pyperclip.copy(str)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def search():
    website = entry_website.get()
    try:
        with open("passwords.json",'r') as data_file:
            # Ler os dados existentes no arquivo.
            data = json.load(data_file)
            if website in data:
                new_data = data[website]
                messagebox.showinfo(title=website,message=f"Email: "
                                            f"{new_data['Email']}\n\nSenha: {new_data['Password']}")
            else:
                messagebox.showinfo(message="Não foram encontrados nenhum resultado!!")

    except FileNotFoundError:
       print("Não existe arquivo com senhas.")
    finally:
        entry_website.delete(0, END)


def add():
    website = entry_website.get()
    password = entry_password.get()
    email = entry_email.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Alerta",message="Os dados precisam ser preenchidos!")

    else:
        is_ok = messagebox.askokcancel(title= website, message= f"As seguintes informações foram preenchidas:\n\n"
                                                                f"Email:{email}\n\nPassword:{password}\n\nElas estão corretas?")

        if is_ok:
            try:
                with open("passwords.json", 'r') as file:
                    #Ler os dados existentes no arquivo.
                    data = json.load(file)
            except FileNotFoundError:
                with open("passwords.json", 'w') as file:
                    #Cria um arquivo de senhas
                    json.dump(new_data,file,indent= 4)
            except json.decoder.JSONDecodeError:
                with open("passwords.json", 'w') as file:
                    # Cria um arquivo de senhas
                    json.dump(new_data, file, indent=4)
            else:
                #Atualiza o arquivo com novas informações.
                data.update(new_data)
                with open("passwords.json", 'w') as file:
                    #Salva as atualizações no arquivo.
                    json.dump(data,file,indent= 4)
            finally:
                entry_website.delete(0,END)
                entry_password.delete(0,END)

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Generate password")
window.config(padx=50,pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file= "logo.png")
canvas.create_image(100,100, image=logo_img)
canvas.grid(column=1,row=0)

#Labels

website = Label(text="Website:", font=(FONT_NAME,11,"bold"))
website.grid(column=0, row=1)

email = Label(text="E-mail/Username:", font=(FONT_NAME,11,"bold"))
email.grid(column=0,row=2)

password = Label(text="Password:", font=(FONT_NAME,11,"bold"))
password.grid(column=0,row=3)


#Entries
entry_website = Entry(width=32)
entry_website.focus()
entry_website.grid(column=1,row=1)
entry_email = Entry(width=50)
entry_email.insert(0,"@gmail.com")
entry_email.grid(column=1,row=2,columnspan = 2)
entry_password = Entry(width=32)
entry_password.grid(column=1,row=3)

#Buttons
generate_button = Button(text="Gener.Password", command=password_generator,width=14,height=1)
generate_button.grid(column=2,row=3)

add_button = Button(text="Add", command=add,width=43,height=1)
add_button.grid(column=1,row=4,columnspan = 2)

search_button = Button(text="Search", command=search,width=14,height=1)
search_button.grid(column=2,row=1)

window.mainloop()