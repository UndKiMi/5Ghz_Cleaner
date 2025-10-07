import os
import sys
import ctypes
import shutil
import threading
import time
import subprocess
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import webbrowser

# Dark Theme
BG_MAIN = "#0d1b2a" #Fond
BG_SECONDARY = "#1b263b" #FondBarre
ACCENT_COLOR = "#e0e1dd"
FG_MAIN = "#778da9"
FG_SECONDARY = "#e0e1dd"

def open_github(event=None):
    webbrowser.open_new("https://github.com/UndKiMi")

def secure_elevation():
    try:
        if not ctypes.windll.shell32.IsUserAnAdmin():
            params = ' '.join([f'"{arg}"' for arg in sys.argv])
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
            sys.exit(0)
    except Exception:
        sys.exit(0)
secure_elevation()

def run_hidden(cmd):
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    return subprocess.run(cmd, shell=False, startupinfo=si, creationflags=subprocess.CREATE_NO_WINDOW,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def get_recycle_bin_count():
    try:
        c = run_hidden(['PowerShell.exe', '-Command', '(Get-ChildItem -Path "Shell:RecycleBinFolder").Count'])
        return int(c.stdout.decode().strip())
    except: return 0

def clear_temp(progress, results):
    total = 0
    for d in [os.getenv('TEMP'), os.path.join(os.getenv('WINDIR'), 'Temp')]:
        if os.path.exists(d):
            try:
                for f in os.listdir(d):
                    fpath = os.path.join(d, f)
                    try:
                        if os.path.isfile(fpath) or os.path.islink(fpath):
                            os.unlink(fpath)
                        elif os.path.isdir(fpath):
                            shutil.rmtree(fpath)
                        total += 1
                    except:
                        pass
            except:
                pass
    results["temp_deleted"] = total

def clear_windows_update_cache(progress, results):
    folder = os.path.join(os.getenv('WINDIR'), 'SoftwareDistribution', 'Download')
    deleted = 0
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath) or os.path.islink(fpath):
                        os.unlink(fpath)
                    elif os.path.isdir(fpath):
                        shutil.rmtree(fpath)
                    deleted += 1
                except:
                    pass
            shutil.rmtree(folder, ignore_errors=True)
        except:
            pass
    results["update_deleted"] = deleted

def empty_recycle_bin(progress, results):
    before = get_recycle_bin_count()
    run_hidden(['PowerShell.exe', '-Command', 'Clear-RecycleBin -Force'])
    results["recycle_bin_deleted"] = before

def stop_services(services, progress, results):
    stopped = []
    for s in services:
        if run_hidden(['sc', 'stop', s]).returncode == 0:
            stopped.append(s)
    results["services_stopped"] = stopped

SERVICES_TO_STOP = ["Fax", "MapsBroker", "WMPNetworkSvc", "Spooler", "RemoteRegistry"]

def clear_prefetch(progress, results):
    folder = os.path.join(os.getenv('WINDIR'), 'Prefetch')
    deleted = 0
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    results["prefetch_cleared"] = deleted

def clear_recent(progress, results):
    folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Recent')
    deleted = 0
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    results["recent_cleared"] = deleted

def clear_thumbnail_cache(progress, results):
    folder = os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\Windows\Explorer')
    deleted = 0
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                if f.startswith("thumbcache") and f.endswith(".db"):
                    fpath = os.path.join(folder, f)
                    try:
                        os.unlink(fpath)
                        deleted += 1
                    except:
                        pass
        except:
            pass
    results["thumbs_cleared"] = deleted

def clear_crash_dumps(progress, results):
    deleted = 0
    folder = os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps')
    if os.path.isdir(folder):
        try:
            for f in os.listdir(folder):
                fpath = os.path.join(folder, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    minidump = os.path.join(os.getenv("WINDIR"), "Minidump")
    if os.path.isdir(minidump):
        try:
            for f in os.listdir(minidump):
                fpath = os.path.join(minidump, f)
                try:
                    if os.path.isfile(fpath):
                        os.unlink(fpath)
                        deleted += 1
                except:
                    pass
        except:
            pass
    memdump = os.path.join(os.getenv("WINDIR"), "MEMORY.DMP")
    if os.path.isfile(memdump):
        try:
            os.unlink(memdump)
            deleted += 1
        except:
            pass
    results["dumps_deleted"] = deleted

def clear_windows_old(progress, results):
    folder = os.path.normpath(os.path.join(os.getenv('WINDIR'), '..', 'Windows.old'))
    deleted = 0
    if os.path.isdir(folder):
        try:
            shutil.rmtree(folder, ignore_errors=True)
            deleted = 1
        except:
            pass
    results['windows_old_deleted'] = deleted

def create_flat_progressbar(parent, width=420, height=18, bg=BG_SECONDARY, fg=ACCENT_COLOR, pad=16):
    c = tk.Canvas(parent, width=width+pad*2, height=height+pad*2, bg=BG_MAIN, bd=0, highlightthickness=0)
    c.create_rectangle(pad, pad, pad+width, pad+height, fill=bg, outline=bg)
    fg_rect = c.create_rectangle(pad, pad, pad, pad+height, fill=fg, outline=fg)
    c._fg_rect = fg_rect; c._width = width; c._height = height; c._pad = pad; c._fg = fg
    c.pack(pady=(12,10))
    return c, fg_rect

def update_progress(canvas, rect, value, max_value):
    pad, height, width, fg = canvas._pad, canvas._height, canvas._width, canvas._fg
    prog_w = int(width * value / max_value)
    canvas.coords(canvas._fg_rect, pad, pad, pad+prog_w, pad+height)
    canvas.itemconfig(canvas._fg_rect, fill=fg)
    canvas.update_idletasks()

def custom_warning(parent, text, accent_color=ACCENT_COLOR):
    warn = tk.Toplevel(parent); warn.title("Attention")
    warn.geometry("370x150"); warn.configure(bg=BG_MAIN)
    warn.resizable(False, False); warn.attributes('-topmost', True); warn.grab_set()
    tk.Label(warn, text="⚠️", font=("Segoe UI", 28, "bold"), fg=accent_color, bg=BG_MAIN).pack(pady=(12,0))
    tk.Label(warn, text=text, font=("Segoe UI", 13, "bold"), fg=FG_MAIN, bg=BG_MAIN, wraplength=340, justify="center").pack(pady=(4,14), padx=16)
    tk.Button(
        warn, text="OK", font=("Segoe UI", 12, "bold"),
        bg=ACCENT_COLOR, fg=FG_MAIN,
        activebackground="#1976D2", activeforeground=FG_MAIN,
        relief="flat", border=0, highlightthickness=0, command=warn.destroy
    ).pack(pady=(0,12), ipadx=35, ipady=6)
    warn.protocol("WM_DELETE_WINDOW", warn.destroy)
    parent.wait_window(warn)

def wait_and_progress(target, step=0.2, sleep=0.007):
    while progress.value < target:
        progress.value += step
        if progress.value > target: progress.value = target
        app.update(); time.sleep(sleep)

def multitool():
    results = {}
    try:
        progress.value = 0
        status.config(text="Nettoyage des éléments système temporaires…", fg=ACCENT_COLOR)
        wait_and_progress(10)
        clear_temp(progress, results)
        wait_and_progress(20)
        status.config(text="Optimisation du préchargement Windows…", fg=ACCENT_COLOR)
        clear_prefetch(progress, results)
        wait_and_progress(30)
        status.config(text="Purge des historiques techniques…", fg=ACCENT_COLOR)
        clear_recent(progress, results)
        wait_and_progress(40)
        status.config(text="Rafraîchissement du cache des miniatures…", fg=ACCENT_COLOR)
        clear_thumbnail_cache(progress, results)
        wait_and_progress(50)
        status.config(text="Nettoyage des journaux techniques…", fg=ACCENT_COLOR)
        clear_crash_dumps(progress, results)
        wait_and_progress(65)
        status.config(text="Nettoyage installation précédente…", fg=ACCENT_COLOR)
        clear_windows_old(progress, results)
        wait_and_progress(75)
        status.config(text="Nettoyage du cache Windows Update…", fg=ACCENT_COLOR)
        clear_windows_update_cache(progress, results)
        wait_and_progress(85)
        status.config(text="Vidage de la corbeille…", fg=ACCENT_COLOR)
        empty_recycle_bin(progress, results)
        wait_and_progress(95)
        status.config(text="Arrêt de modules système optionnels…", fg=ACCENT_COLOR)
        stop_services(SERVICES_TO_STOP, progress, results)
        wait_and_progress(100)
        status.config(text="Opération terminée !", fg=ACCENT_COLOR)
        time.sleep(0.38)
        show_summary(results)
    except Exception as e:
        messagebox.showerror("Erreur 5Gh'z Cleaner", str(e))

def show_summary(results):
    bilan_win = tk.Toplevel(app)
    bilan_win.title("Bilan du nettoyage"); bilan_win.configure(bg=BG_MAIN)
    bilan_win.geometry("480x370"); bilan_win.resizable(False, False); bilan_win.grab_set(); bilan_win.focus_set()
    main_frame = tk.Frame(bilan_win, bg=BG_MAIN); main_frame.pack(fill="both", expand=True, pady=(10,0))
    tk.Label(main_frame, text="Bilan du nettoyage", font=("Segoe UI", 19, "bold"),
             bg=BG_MAIN, fg=ACCENT_COLOR).pack(pady=(10,20))
    details = [
        ("Éléments système temporaires supprimés", results.get('temp_deleted', 0)),
        ("Préchargements Windows optimisés", results.get('prefetch_cleared', 0)),
        ("Historique technique purgé", results.get('recent_cleared', 0)),
        ("Cache de miniatures rafraîchi", results.get('thumbs_cleared', 0)),
        ("Journaux techniques allégés", results.get('dumps_deleted', 0)),
        ("Installation précédente nettoyée", "Oui" if results.get('windows_old_deleted', 0) else "Non"),
        ("Cache Windows Update nettoyé", results.get('update_deleted', 0)),
        ("Corbeille vidée", results.get('recycle_bin_deleted', 0)),
        ("Modules optionnels arrêtés", len(results.get('services_stopped', [])))
    ]
    details_frame = tk.Frame(main_frame, bg=BG_MAIN); details_frame.pack(pady=(0,15), padx=20, fill="x")
    for label, value in details:
        line = tk.Frame(details_frame, bg=BG_MAIN); line.pack(fill="x", pady=4)
        tk.Label(line, text=label + " :", font=("Segoe UI", 12), bg=BG_MAIN, fg=FG_MAIN,
                 anchor="w", justify="left").pack(side="left")
        tk.Label(line, text=f"{value}", font=("Segoe UI", 12, "bold"), bg=BG_MAIN, fg=ACCENT_COLOR,
                 anchor="e").pack(side="right")
    servs = results.get('services_stopped',[])
    if servs:
        services_frame = tk.Frame(main_frame, bg=BG_MAIN); services_frame.pack(pady=(10,0), padx=20, fill="x")
        tk.Label(services_frame, text="Détail des modules arrêtés :", font=("Segoe UI", 11, "bold"),
                bg=BG_MAIN, fg=FG_SECONDARY).pack(anchor="w", pady=(0,5))
        for s in servs:
            tk.Label(services_frame, text=f"→ {s}", font=("Segoe UI", 10), bg=BG_MAIN, fg=FG_SECONDARY).pack(anchor="w", padx=20, pady=1)
    tk.Button(main_frame, text="Fermer", font=("Segoe UI", 13, "bold"),
              bg=ACCENT_COLOR, fg=FG_MAIN, activebackground="#1976D2", activeforeground=FG_MAIN,
              relief="flat", border=0, highlightthickness=0, command=bilan_win.destroy
    ).pack(pady=(20,15), ipadx=30, ipady=8)
    credit_frame = tk.Frame(bilan_win, bg=BG_MAIN)
    credit_frame.pack(side="bottom", pady=(0, 8))
    tk.Label(
        credit_frame,
        text="Tous droits réservés par ",
        font=("Segoe UI", 9), fg=FG_SECONDARY, bg=BG_MAIN
    ).pack(side="left")
    pseudo_link = tk.Label(
        credit_frame,
        text="UndKiMi",
        font=("Segoe UI", 9, "underline"),
        fg=ACCENT_COLOR,
        bg=BG_MAIN,
        cursor="hand2"
    )
    pseudo_link.pack(side="left")
    pseudo_link.bind("<Button-1>", open_github)

def launch_clean():
    threading.Thread(target=multitool, daemon=True).start()

def start_main_window():
    global app
    app = tk.Tk()
    app.title("5Gh'z_Cleaner")
    app.geometry("520x300")
    app.configure(bg=BG_MAIN)
    app.resizable(False, False)
    def redraw_progress(*args):
        update_progress(progress_canvas, getattr(progress_canvas, '_fg_rect', progress_fg), progress.get(), 100)
    avatar_size = 54
    avatar_path = "image.jpg"
    try:
        base_image = Image.open(avatar_path).resize((avatar_size, avatar_size), Image.LANCZOS)
        avatar = ImageTk.PhotoImage(base_image)
    except Exception:
        avatar = None
    title_frame = tk.Frame(app, bg=BG_MAIN); title_frame.pack(pady=(17, 3))
    if avatar:
        tk.Label(title_frame, image=avatar, bg=BG_MAIN).pack(side="left", padx=(0, 12))
    tk.Label(title_frame, text="5Gh'z_Cleaner", font=("Segoe UI", 21, "bold"), bg=BG_MAIN, fg=ACCENT_COLOR).pack(side="left", anchor="n")
    tk.Label(app, text="Windows Cleaning & Optimisation LITE", font=("Segoe UI", 12, "bold"), bg=BG_MAIN, fg=FG_SECONDARY).pack(pady=(0, 8))
    global progress_canvas, progress_fg, progress
    progress_canvas, progress_fg = create_flat_progressbar(app, width=400, height=16, bg=BG_SECONDARY, fg=ACCENT_COLOR)
    progress = tk.DoubleVar(); progress.set(0)
    progress.trace_add("write", redraw_progress)
    global status
    status = tk.Label(app, text="Prêt à nettoyer !", font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=FG_MAIN); status.pack(pady=(7,8))
    tk.Button(app, text="🚀 Lancer le nettoyage", font=("Segoe UI", 12, "bold"),
              bg=ACCENT_COLOR, fg=FG_MAIN, activebackground="#1976D2", activeforeground=FG_MAIN,
              relief="flat", border=0, highlightthickness=0, command=launch_clean
    ).pack(pady=(12,0), ipadx=18, ipady=6)

    credit_frame = tk.Frame(app, bg=BG_MAIN)
    credit_frame.pack(side="bottom", pady=(0, 8))
    tk.Label(
        credit_frame,
        text="Ce script élève les droits automatiquement (UAC) • Tous droits réservés par ",
        font=("Segoe UI", 9), fg=FG_SECONDARY, bg=BG_MAIN
    ).pack(side="left")
    pseudo_link = tk.Label(
        credit_frame,
        text="UndKiMi",
        font=("Segoe UI", 9, "underline"),
        fg=ACCENT_COLOR,
        bg=BG_MAIN,
        cursor="hand2"
    )
    pseudo_link.pack(side="left")
    pseudo_link.bind("<Button-1>", open_github)

    class ProgressProxy:
        def __init__(self, var): self.var = var
        @property
        def value(self): return self.var.get()
        @value.setter
        def value(self, v): self.var.set(v)
        def get(self): return self.var.get()
    globals()['progress'] = ProgressProxy(progress)
    app.mainloop()

def disclaimer_window():
    root = tk.Tk()
    root.title("Disclaimer 5Gh'z_Cleaner")
    root.geometry("370x170")
    root.config(bg=BG_MAIN)
    root.resizable(False, False)

    def open_disclaimer_web():
        webbrowser.open_new("https://github.com/UndKiMi/5Ghz_Cleaner/tree/main")
    disclaimer_link = tk.Label(root, text="Lire le disclaimer en ligne", font=("Segoe UI", 12, "underline"),
                              fg=ACCENT_COLOR, bg=BG_MAIN, cursor="hand2")
    disclaimer_link.pack(pady=(26,16))
    disclaimer_link.bind("<Button-1>", lambda e: open_disclaimer_web())

    v = tk.IntVar()
    tk.Checkbutton(root, text="J’ai lu et compris les conditions d’utilisation.", variable=v,
                   font=("Segoe UI", 11, "bold"), bg=BG_MAIN, fg=ACCENT_COLOR,
                   selectcolor=BG_MAIN, activebackground=BG_MAIN, activeforeground=ACCENT_COLOR
                  ).pack(pady=(0,18))

    def ok():
        if v.get() == 1:
            root.destroy()
            start_main_window()
        else:
            custom_warning(root, "Veuillez accepter les conditions pour utiliser le logiciel.", accent_color=ACCENT_COLOR)
    tk.Button(root, text="J'accepte", font=("Segoe UI", 12, "bold"), bg=ACCENT_COLOR, fg=FG_MAIN,
              activebackground="#1976D2", activeforeground=FG_MAIN, relief="flat", border=0,
              highlightthickness=0, command=ok).pack(pady=(0,6), ipadx=20, ipady=5)

    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

if __name__ == "__main__":
    disclaimer_window()
