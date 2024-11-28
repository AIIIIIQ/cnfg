import os
import tarfile
import shutil
import datetime
import calendar
from pathlib import Path, PurePosixPath
import tarfile
import io
from datetime import datetime
import calendar

class ShellEmulator:
    def __init__(self, tar_path):
        self.tar_path = tar_path
        self.vfs = {}  # Виртуальная файловая система в памяти
        self.current_path = []
        self._load_tar_to_memory()

    def _load_tar_to_memory(self):
        with tarfile.open(self.tar_path, "r") as tar:
            for member in tar.getmembers():
                path_parts = member.name.split("/")
                current = self.vfs
                for part in path_parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                if member.isfile():
                    current[path_parts[-1]] = tar.extractfile(member).read()
                elif member.isdir():
                    current[path_parts[-1]] = {}

    def _navigate_to_path(self, path_parts):
        current = self.vfs
        for part in path_parts:
            if part not in current or not isinstance(current[part], dict):
                raise FileNotFoundError(f"Path not found: {'/'.join(path_parts)}")
            current = current[part]
        return current

    def run(self):
        print("Shell Emulator started. Type 'exit' to quit.")
        while True:
            try:
                prompt = "/" + "/".join(self.current_path) if self.current_path else "/"
                command = input(f"{prompt}> ").strip()
                if command == "exit":
                    break
                self._handle_command(command)
            except Exception as e:
                print(f"Error: {e}")

    def _handle_command(self, command):
        parts = command.split()
        if not parts:
            return
        cmd, *args = parts

        if cmd == "ls":
            self.ls(args)
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "cal":
            self.cal()
        elif cmd == "chmod":
            self.chmod(args)
        else:
            print(f"Command '{cmd}' not found.")

    def ls(self, args):
        target_path = args[0].split("/") if args else []
        try:
            target_dir = self._navigate_to_path(self.current_path + target_path)
            if isinstance(target_dir, dict):
                for entry in target_dir:
                    print(entry)
            else:
                print("ls: Not a directory")
        except FileNotFoundError as e:
            print(e)

    def cd(self, args):
        if not args:
            # Переход в корневой каталог
            self.current_path = []
            return

        target_path = args[0]
        if target_path == "/":
            # Переход в корень
            self.current_path = []
        elif target_path == "..":
            # Переход в родительский каталог
            if self.current_path:
                self.current_path.pop()
        else:
            # Разбиваем путь и проверяем, является ли он относительным или абсолютным
            target_parts = target_path.split("/")
            if target_path.startswith("/"):
                # Абсолютный путь
                new_path = target_parts
            else:
                # Относительный путь
                new_path = self.current_path + target_parts

            try:
                # Проверяем, существует ли указанный путь
                self._navigate_to_path(new_path)
                self.current_path = new_path
            except FileNotFoundError as e:
                print(e)

    def chmod(self):
        mode, file_name = args

        # Проверяем, что mode состоит из 3 цифр, каждая из которых от 0 до 7
        if not mode.isdigit() or len(mode) != 3 or any(int(digit) > 7 for digit in mode):
            print(f"chmod: invalid mode: '{mode}'")
            return

        target_path = file_name.split("/")
        try:
            parent_dir = self._navigate_to_path(self.current_path + target_path[:-1])
            file_name = target_path[-1]
            if file_name in parent_dir:
                print(f"chmod: permissions of '{file_name}' changed to {mode}")
            else:
                print(f"chmod: cannot access '{file_name}': No such file or directory")
        except FileNotFoundError as e:
            print(e)

    def cal(self):
        now = datetime.now()
        print(calendar.TextCalendar().formatmonth(now.year, now.month))


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python emulator.py <path_to_tar>")
        sys.exit(1)

    tar_path = sys.argv[1]

    # Проверяем, существует ли указанный tar-архив
    if not os.path.exists(tar_path):
        print(f"Error: File '{tar_path}' not found.")
        sys.exit(1)

    # Запускаем эмулятор
    emulator = ShellEmulator(tar_path)
    try:
        emulator.run()
    except KeyboardInterrupt:
        print("\nExiting...")
