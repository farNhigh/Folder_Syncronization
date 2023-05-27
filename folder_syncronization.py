import os
import shutil
import hashlib
import argparse
import logging
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def md5_checksum(filename, block_size=65536):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            md5.update(block)
    return md5.hexdigest()

def sync_folders(source, replica, log_file_path):
    logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')
    for root, dirs, files in os.walk(source):
        for filename in files:
            source_path = os.path.join(root, filename)
            replica_path = source_path.replace(source, replica, 1)
            if os.path.exists(replica_path):
                if md5_checksum(source_path) != md5_checksum(replica_path):
                    logging.info(f'Updating file: {filename}')
                    shutil.copy2(source_path, replica_path)
            else:
                logging.info(f'Creating file: {filename}')
                shutil.copy2(source_path, replica_path)
        for dirname in dirs:
            source_path = os.path.join(root, dirname)
            replica_path = source_path.replace(source, replica, 1)
            if not os.path.exists(replica_path):
                logging.info(f'Creating directory: {dirname}')
                os.makedirs(replica_path)
    for root, dirs, files in os.walk(replica):
        for filename in files:
            replica_path = os.path.join(root, filename)
            source_path = replica_path.replace(replica, source, 1)
            if not os.path.exists(source_path):
                logging.info(f'Removing file: {filename}')
                os.remove(replica_path)
        for dirname in dirs:
            replica_path = os.path.join(root, dirname)
            source_path = replica_path.replace(replica, source, 1)
            if not os.path.exists(source_path):
                logging.info(f'Removing directory: {dirname}')
                os.rmdir(replica_path)

def sync_with_gui():
    root = tk.Tk()
    root.title("Folder Synchronization")
    language = "English"

    def browse_source():
        folder_path = filedialog.askdirectory()
        source_entry.delete(0, tk.END)
        source_entry.insert(tk.END, folder_path)

    def browse_replica():
        folder_path = filedialog.askdirectory()
        replica_entry.delete(0, tk.END)
        replica_entry.insert(tk.END, folder_path)

    def browse_log_directory():
        log_directory = filedialog.askdirectory()
        log_directory_entry.delete(0, tk.END)
        log_directory_entry.insert(tk.END, log_directory)

    def start_sync():
        source = source_entry.get()
        replica = replica_entry.get()
        interval = int(interval_entry.get())
        log_directory = log_directory_entry.get()

        log_file_path = os.path.join(log_directory, "sync_log.txt")
        logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(message)s')

        while True:
            sync_folders(source, replica, log_file_path)
            time.sleep(interval)

    def show_about():
        if language == "English":
            messagebox.showinfo("About", "This software was created by Ionut-Alexandru VIZUROIU.\nContact alexandru.vizuroiu@gmail.com for further info.")
        if language == "Romanian":
            messagebox.showinfo("Despre", "Acest software a fost creat de Ionut-Alexandru VIZUROIU.\nPentru mai multe informații: alexandru.vizuroiu@gmail.com.")

    def change_language():
        nonlocal language
        if language == "English":
            language = "Romanian"
            source_label.config(text="Folder Sursă:")
            replica_label.config(text="Folder Replică:")
            interval_label.config(text="Interval de sincronizare (secunde):")
            log_label.config(text="Locație Salvare Jurnal:")
            start_button.config(text="Pornire Sincronizare")
            about_button.config(text="Despre")
            root.title("Sincronizare Foldere")
            language_button.config(text="Schimbă limba")
            source_button.config(text="Încarcă")
            replica_button.config(text="Încarcă")
            log_directory_button.config(text="Încarcă")
        else:
            language = "English"
            source_label.config(text="Source Folder:")
            replica_label.config(text="Replica Folder:")
            interval_label.config(text="Sync Interval (seconds):")
            log_label.config(text="Log Saving Location:")
            start_button.config(text="Start Sync")
            about_button.config(text="About")
            root.title("Folder Synchronization")
            language_button.config(text="Change Language")
            source_button.config(text="Browse")
            replica_button.config(text="Browse")
            log_directory_button.config(text="Browse")

    source_label = tk.Label(root, text="Source Folder:")
    source_label.grid(row=1, column=0, padx=5, pady=5)

    source_entry = tk.Entry(root)
    source_entry.grid(row=1, column=1, padx=5, pady=5)

    source_button = tk.Button(root, text="Browse", command=browse_source)
    source_button.grid(row=1, column=2, padx=5, pady=5)

    replica_label = tk.Label(root, text="Replica Folder:")
    replica_label.grid(row=2, column=0, padx=5, pady=5)

    replica_entry = tk.Entry(root)
    replica_entry.grid(row=2, column=1, padx=5, pady=5)

    replica_button = tk.Button(root, text="Browse", command=browse_replica)
    replica_button.grid(row=2, column=2, padx=5, pady=5)

    interval_label = tk.Label(root, text="Sync Interval (seconds):")
    interval_label.grid(row=3, column=0, padx=5, pady=5)

    interval_entry = tk.Entry(root)
    interval_entry.grid(row=3, column=1, padx=5, pady=5)

    log_label = tk.Label(root, text="Log Saving Location:")
    log_label.grid(row=4, column=0, padx=5, pady=5)
	
    log_directory_entry = tk.Entry(root)
    log_directory_entry.grid(row=4, column=1, padx=5, pady=5)

    log_directory_button = tk.Button(root, text="Browse", command=browse_log_directory)
    log_directory_button.grid(row=4, column=2, padx=5, pady=5)

    start_button = tk.Button(root, text="Start Sync", command=start_sync)
    start_button.grid(row=5, column=0, columnspan=3, padx=5, pady=10)

    about_button = tk.Button(root, text="About", command=show_about)
    about_button.grid(row=6, column=2, columnspan=3, padx=5, pady=10)

    language_button = tk.Button(root, text="Change Language", command=change_language)
    language_button.grid(row=0, column=0, columnspan=3, padx=5, pady=10)

    root.mainloop()

if __name__ == '__main__':
    sync_with_gui()
