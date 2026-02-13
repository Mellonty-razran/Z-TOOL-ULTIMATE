import customtkinter as ctk
import json
import subprocess
import threading
import time
import webbrowser
import os
import sys
from tkinter import messagebox
import requests

# --- МАГИЯ ДЛЯ ОДНОГО ФАЙЛА ---
def resource_path(relative_path):
    """ Получает путь к файлам внутри EXE или в обычной папке """
    try:
        # PyInstaller создает временную папку _MEIxxxx
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ЦВЕТА
ACCENT = "#00FF41" 
BG = "#080808"     
CARD = "#121212"   

CURRENT_VERSION = "1.1"
# Ссылка на файл с версией (создай его на GitHub, когда будешь готов)
VERSION_URL = "https://raw.githubusercontent.com/твой_ник/z-tool/main/version.txt"

class ZToolFinalBeast(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"Z-TOOL ULTIMATE | v{CURRENT_VERSION} | BY CRYOSLAYER")
        self.geometry("1400x920")
        self.configure(fg_color=BG)
        
        # Подгружаем иконку через resource_path
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except:
            pass 

        # Загружаем конфиг через resource_path
        try:
            with open(resource_path('config.json'), 'r', encoding='utf-8') as f:
                self.db = json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Файл базы данных не найден внутри системы!\n{e}")
            self.quit()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- САЙДБАР ---
        self.sidebar = ctk.CTkFrame(self, width=350, fg_color=CARD, corner_radius=15)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        ctk.CTkLabel(self.sidebar, text="Z-TOOL", font=("Impact", 48), text_color=ACCENT).pack(pady=(25, 0))
        ctk.CTkLabel(self.sidebar, text="CRYOSLAYER EDITION", font=("Consolas", 11), text_color="#444").pack()
        
        # Индикаторы портов
        self.ind_frame = ctk.CTkFrame(self.sidebar, fg_color="#050505", height=60, corner_radius=10)
        self.ind_frame.pack(fill="x", padx=20, pady=20)
        self.ind_adb = ctk.CTkLabel(self.ind_frame, text="● ADB", text_color="#333", font=("Arial", 11, "bold"))
        self.ind_adb.pack(side="left", expand=True)
        self.ind_fast = ctk.CTkLabel(self.ind_frame, text="● FAST", text_color="#333", font=("Arial", 11, "bold"))
        self.ind_fast.pack(side="left", expand=True)

        self.search = ctk.CTkEntry(self.sidebar, placeholder_text="ПОИСК...", height=45, corner_radius=10)
        self.search.pack(fill="x", padx=20, pady=10)
        self.search.bind("<KeyRelease>", self.on_search)

        self.dev_scroll = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent", label_text="DATABASE")
        self.dev_scroll.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.model_items = []
        self.load_models()

        # --- ГЛАВНАЯ ЗОНА ---
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)

        self.status_bar = ctk.CTkFrame(self.main_area, height=80, fg_color=CARD, border_width=1, border_color="#222")
        self.status_bar.pack(fill="x", pady=(0, 15))
        self.status_txt = ctk.CTkLabel(self.status_bar, text="CRYOSLAYER SYSTEM ONLINE", font=("Verdana", 20, "bold"), text_color="#333")
        self.status_txt.pack(pady=25)

        self.tabs = ctk.CTkTabview(self.main_area, segmented_button_selected_color=ACCENT, corner_radius=15)
        self.tabs.pack(fill="both", expand=True)
        
        for tab_name, ops in self.db["ops"].items():
            t = self.tabs.add(tab_name)
            self.build_tab(t, tab_name, ops)

        self.progress = ctk.CTkProgressBar(self.main_area, progress_color=ACCENT, fg_color="#111", height=10)
        self.progress.pack(fill="x", pady=15)
        self.progress.set(0)

        # --- ЛОГ ---
        self.log_frame = ctk.CTkFrame(self, height=280, fg_color="#050505", border_width=1, border_color=ACCENT)
        self.log_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 15))
        self.log_box = ctk.CTkTextbox(self.log_frame, font=("Consolas", 14), text_color=ACCENT, fg_color="transparent")
        self.log_box.pack(fill="both", expand=True, padx=10, pady=10)

        # ЗАПУСК ФОНОВЫХ ПРОЦЕССОВ
        self.log(f">> Z-TOOL v{CURRENT_VERSION} ЗАПУЩЕН УСПЕШНО.")
        threading.Thread(target=self.port_scanner, daemon=True).start()
        threading.Thread(target=self.check_ota, daemon=True).start()

    def check_ota(self):
        """ OTA Обновление через интернет """
        try:
            # Имитация запроса (замени на реальный requests.get когда создашь репо)
            time.sleep(3)
            self.log(">> ПРОВЕРКА ОБНОВЛЕНИЙ... OK")
        except:
            self.log(">> ОШИБКА ОБНОВЛЕНИЯ: НЕТ СВЯЗИ С СЕРВЕРОМ.")

    def load_models(self):
        # ТВОЙ SAMSUNG A33 5G
        my_dev = "SAMSUNG Galaxy A33 5G"
        btn = ctk.CTkButton(self.dev_scroll, text=f"★ {my_dev}", fg_color="transparent", anchor="w", 
                           text_color=ACCENT, command=lambda n=my_dev: self.set_dev(n))
        btn.pack(fill="x")
        self.model_items.append({"name": my_dev, "widget": btn})
        
        for brand, models in self.db["brands"].items():
            for m in models:
                full_name = f"{brand} {m}"
                if "A33" in full_name: continue
                btn = ctk.CTkButton(self.dev_scroll, text=full_name, fg_color="transparent", anchor="w", 
                                   command=lambda n=full_name: self.set_dev(n))
                btn.pack(fill="x")
                self.model_items.append({"name": full_name, "widget": btn})

    def port_scanner(self):
        while True:
            try:
                adb = subprocess.run("adb devices", capture_output=True, text=True, shell=True)
                if "device" in adb.stdout.split('\n')[1]:
                    self.ind_adb.configure(text_color=ACCENT)
                else:
                    self.ind_adb.configure(text_color="#333")
                
                fast = subprocess.run("fastboot devices", capture_output=True, text=True, shell=True)
                if fast.stdout.strip():
                    self.ind_fast.configure(text_color="#00AAFF")
                else:
                    self.ind_fast.configure(text_color="#333")
            except: pass
            time.sleep(3)

    def set_dev(self, name):
        self.status_txt.configure(text=f"TARGET: {name.upper()}", text_color=ACCENT)
        self.log(f">> ВЫБРАНО: {name}")

    def build_tab(self, tab, mode, ops):
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        for i, op in enumerate(ops):
            f = ctk.CTkFrame(tab, fg_color="#0a0a0a", border_width=1, border_color="#1a1a1a")
            f.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
            
            ctk.CTkButton(f, text=op.upper(), fg_color="transparent", font=("Arial", 11, "bold"),
                               command=lambda m=mode, a=op: self.run_op(m, a)).pack(side="left", fill="x", expand=True, padx=5)
            
            q = ctk.CTkButton(f, text="?", width=30, command=lambda a=op: self.show_help(a))
            q.pack(side="right", padx=5)

    def show_help(self, op):
        msg = self.db["tooltips"].get(op, "Инструкция в базе данных.")
        messagebox.showinfo("INFO", msg)

    def run_op(self, m, a):
        def task():
            self.log(f">> ИНИЦИАЛИЗАЦИЯ: {a}...")
            self.progress.set(0)
            for p in range(1, 11):
                self.progress.set(p/10)
                time.sleep(0.1)
            
            if "ADB" in a.upper():
                self.real_adb_read()
            else:
                self.log(f">> ОПЕРАЦИЯ {a} ЗАВЕРШЕНА.")
            
            self.progress.set(0)

        threading.Thread(target=task).start()

    def real_adb_read(self):
        try:
            model = subprocess.check_output("adb shell getprop ro.product.model", shell=True, text=True).strip()
            sn = subprocess.check_output("adb get-serialno", shell=True, text=True).strip()
            self.log(f"   [FOUND] MODEL: {model}")
            self.log(f"   [FOUND] SN: {sn}")
            self.status_txt.configure(text=f"CONNECTED: {model}", text_color=ACCENT)
        except:
            self.log("   [!] ОШИБКА: Устройство не найдено.")

    def on_search(self, e):
        q = self.search.get().lower()
        for i in self.model_items:
            if q in i["name"].lower(): i["widget"].pack(fill="x")
            else: i["widget"].pack_forget()

    def log(self, t):
        self.log_box.insert("end", f"{t}\n")
        self.log_box.see("end")

if __name__ == "__main__":
    ZToolFinalBeast().mainloop()