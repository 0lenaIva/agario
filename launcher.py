from customtkinter import*

class ConnectWindow(CTk):
    def __init__(self):
        super().__init__()
        self.name = None
        self.host = None
        self.port = None

        self.title('Agario')
        self.geometry('400x400')

        CTkLabel(self, text = 'Підключення до сервера...', 
                 font=('Times New Roman', 25, 'bold')).pack(pady=30, padx = 20, anchor='w')

        self.entry_name = CTkEntry(self, height = 50, font=('Times New Roman', 18), placeholder_text='Введіть ім\'я...')
        self.entry_name.pack(padx = 20, fill='x', pady = (5,10))

        self.entry_host = CTkEntry(self, height = 50, font=('Times New Roman', 18), placeholder_text='Введіть HOST...')
        self.entry_host.pack(padx = 20, fill='x', pady = (5,10))

        self.entry_port = CTkEntry(self, height = 50, font=('Times New Roman', 18), placeholder_text='Введіть PORT...')
        self.entry_port.pack(padx = 20, fill='x', pady = (5,10))

        CTkButton(self, text='Приєднатись',font=('Times New Roman', 20), height=50,
                  command=self.open_game).pack(pady=15,padx=20, fill='x')
        
    def open_game(self):
        self.name = self.entry_name.get()
        self.host = self.entry_host.get()
        self.port = int(self.entry_port.get())
        self.destroy()

