class ButtonStyle:
    """Estilo dos botões."""
    def __init__(self, button):
        self.button = button
        self.button.config(font=("Arial", 10, "bold"),
                           bd=3,
                           bg="#3E5879",
                           fg="#F5EFE7",
                           relief="raised",
                           activebackground="#F5EFE7",
                           activeforeground="#3E5879")
    
    def set_command(self, command):
        self.button.config(command=command)
    
    def grid(self, row, column):
        self.button.grid(row=row, column=column)
    
    def pack(self, pady=5):
        self.button.pack(pady=pady)
        
