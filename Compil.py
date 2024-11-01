import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import subprocess
import threading
import sys

def check_pyinstaller_version(label_version, open_button):
    try:
        result = subprocess.run([sys.executable, '-m', 'PyInstaller', '--version'], capture_output=True, text=True, check=True)
        version = result.stdout.strip()
        label_version.config(text=f"Установлен PyInstaller версии: {version}")
        open_button.config(text="Открыть", command=lambda: open_build_window(main_window, label_version, open_button))
        open_button["state"] = "normal"
    except subprocess.CalledProcessError:
        label_version.config(text="PyInstaller не установлен.")
        open_button.config(text="Установить PyInstaller", command=install_pyinstaller)
        open_button["state"] = "normal"
        messagebox.showwarning("Внимание", "PyInstaller не установлен. Пожалуйста, установите его перед продолжением работы.")

def install_pyinstaller():
    threading.Thread(target=run_install_command).start()

def run_install_command():
    command = [sys.executable, '-m', 'pip', 'install', 'pyinstaller']
    progress_bar.start()
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Успех", "PyInstaller успешно установлен!")
        check_pyinstaller_version(label_version, open_button)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Ошибка при установке: {e}")
    finally:
        progress_bar.stop()
        progress_bar['value'] = 100

def open_build_window(main_window, label_version, open_button):
    main_window.withdraw()  
    build_window = tk.Toplevel(main_window)
    build_window.title("PyInstaller GUI")
    
    label = tk.Label(build_window, text="Введите имя файла (например, BBS.py):")
    label.pack(pady=10)
    
    entry = tk.Entry(build_window, width=30)
    entry.pack(pady=5)

    icon_label = tk.Label(build_window, text="Введите имя иконки (например, Icons.ico):")
    icon_label.pack(pady=10)

    icon_entry = tk.Entry(build_window, width=30)
    icon_entry.pack(pady=5)

    windowed_var = tk.BooleanVar(value=True)
    windowed_checkbox = tk.Checkbutton(build_window, text="Скрыть консоль", variable=windowed_var)
    windowed_checkbox.pack(pady=5)

    button = tk.Button(build_window, text="Поехали", command=lambda: build_executable(entry.get(), icon_entry.get(), windowed_var.get()))
    button.pack(pady=10)

    global progress_bar
    progress_bar = ttk.Progressbar(build_window, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
    progress_bar.pack(pady=20)

def build_executable(script_name, icon_name, windowed):
    if not script_name.endswith('.py'):
        script_name += '.py'
    if not icon_name.endswith('.ico'):
        icon_name += '.ico'
    
    command = [sys.executable, '-m', 'PyInstaller', '--onefile', f'--icon={icon_name}', script_name]
    
    if windowed:
        command.append('--windowed')
    
    open_button['state'] = 'disabled'  # Отключаем кнопку
    threading.Thread(target=run_command, args=(command,)).start()

def run_command(command):
    progress_bar.start()
    
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Успех", f"Скомпилировано: {command[-1]}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Ошибка", f"Ошибка: {e}")
    finally:
        progress_bar.stop()
        progress_bar['value'] = 100
        open_button['state'] = 'normal'

def main():
    global main_window, label_version, open_button
    main_window = tk.Tk()
    main_window.title("PyInstaller Установщик")
    
    label_version = tk.Label(main_window, text="")
    label_version.pack(pady=10)
    
    open_button = tk.Button(main_window, text="Проверка PyInstaller...", state="disabled")
    open_button.pack(pady=20)

    global progress_bar
    progress_bar = ttk.Progressbar(main_window, orient=tk.HORIZONTAL, length=300, mode='indeterminate')
    progress_bar.pack(pady=20)

    check_pyinstaller_version(label_version, open_button)
    
    main_window.mainloop()

if __name__ == "__main__":
    main()
