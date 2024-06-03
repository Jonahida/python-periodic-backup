import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import subprocess


class FileTransferGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("File Transfer")
        
        self.label = tk.Label(master, text="Select operation:")
        self.label.pack()
        
        self.client_button = tk.Button(master, text="Client (sender)", command=self.run_client)
        self.client_button.pack()
        
        self.server_button = tk.Button(master, text="Server (receiver)", command=self.run_server)
        self.server_button.pack()
        
    def run_client(self):
        self.master.withdraw()  # Hide the main window
        ClientConfigGUI(self.master)  # Passing master window here

    def run_server(self):
        self.master.withdraw()  # Hide the main window
        ServerConfigGUI(self.master)  # Passing master window here

    def close_application(self):
        self.master.destroy()  # Destroying master window


class ClientConfigGUI:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent)  # Creating Toplevel window
        self.root.title("Client Configuration")

        self.host_label = tk.Label(self.root, text="Host:")
        self.host_label.grid(row=0, column=0)
        self.host_entry = tk.Entry(self.root)
        self.host_entry.grid(row=0, column=1)
        self.host_entry.insert(0, "127.0.0.1")

        self.port_label = tk.Label(self.root, text="Port:")
        self.port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=1, column=1)
        self.port_entry.insert(0, "5000")

        self.source_label = tk.Label(self.root, text="Source Directory:")
        self.source_label.grid(row=2, column=0)
        self.source_entry = tk.Entry(self.root)
        self.source_entry.grid(row=2, column=1)
        self.source_entry.insert(0, "src")

        self.backup_label = tk.Label(self.root, text="Backup Directory:")
        self.backup_label.grid(row=3, column=0)
        self.backup_entry = tk.Entry(self.root)
        self.backup_entry.grid(row=3, column=1)
        self.backup_entry.insert(0, "backup")

        self.task_label = tk.Label(self.root, text="Task Period (minutes):")
        self.task_label.grid(row=4, column=0)
        self.task_entry = tk.Entry(self.root)
        self.task_entry.grid(row=4, column=1)
        self.task_entry.insert(0, "15")

        self.transmit_button = tk.Button(self.root, text="Transmit Files", command=self.run_transmit)
        self.transmit_button.grid(row=5, column=0, columnspan=2)

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_main)
        self.back_button.grid(row=6, column=0, columnspan=2)

        self.close_button = tk.Button(self.root, text="Close", command=self.close_application)
        self.close_button.grid(row=7, column=0, columnspan=2)

    def run_transmit(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        source_dir = self.source_entry.get()
        backup_dir = self.backup_entry.get()
        task_period = int(self.task_entry.get())

        args = ["python3", "client.py", "-i", host, "-p", str(port), "-s", source_dir, "-b", backup_dir, "-t", str(task_period)]
        subprocess.Popen(args)
        self.root.destroy()

    def back_to_main(self):
        self.root.destroy()
        self.parent.deiconify()  # Deiconify parent window

    def close_application(self):
        self.root.destroy()
        self.parent.destroy()  # Terminate the process when child GUI is closed


class ServerConfigGUI:
    def __init__(self, parent):
        self.parent = parent
        self.root = tk.Toplevel(parent)  # Creating Toplevel window
        self.root.title("Server Configuration")

        self.host_label = tk.Label(self.root, text="Host:")
        self.host_label.grid(row=0, column=0)
        self.host_entry = tk.Entry(self.root)
        self.host_entry.grid(row=0, column=1)
        self.host_entry.insert(0, "127.0.0.1")

        self.port_label = tk.Label(self.root, text="Port:")
        self.port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(self.root)
        self.port_entry.grid(row=1, column=1)
        self.port_entry.insert(0, "5000")

        self.target_label = tk.Label(self.root, text="Target Directory:")
        self.target_label.grid(row=2, column=0)
        self.target_entry = tk.Entry(self.root)
        self.target_entry.grid(row=2, column=1)
        self.target_entry.insert(0, "dst")

        self.clients_label = tk.Label(self.root, text="Max Simultaneous Clients:")
        self.clients_label.grid(row=3, column=0)
        self.clients_entry = tk.Entry(self.root)
        self.clients_entry.grid(row=3, column=1)
        self.clients_entry.insert(0, "1")

        self.receive_button = tk.Button(self.root, text="Receive Files", command=self.run_receive)
        self.receive_button.grid(row=4, column=0, columnspan=2)

        self.back_button = tk.Button(self.root, text="Back", command=self.back_to_main)
        self.back_button.grid(row=5, column=0, columnspan=2)

        self.close_button = tk.Button(self.root, text="Close", command=self.close_application)
        self.close_button.grid(row=6, column=0, columnspan=2)

    def run_receive(self):
        host = self.host_entry.get()
        port = int(self.port_entry.get())
        target_dir = self.target_entry.get()
        n_clients = int(self.clients_entry.get())

        args = ["python3", "server.py", "-i", host, "-p", str(port), "-t", target_dir, "-c", str(n_clients)]
        subprocess.Popen(args)
        self.root.destroy()

    def back_to_main(self):
        self.root.destroy()
        self.parent.deiconify()

    def close_application(self):
        self.root.destroy()
        self.parent.destroy()  # Terminate the process when child GUI is closed


def main():
    root = tk.Tk()
    app = FileTransferGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()
