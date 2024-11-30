# Shell Emulator

## 1. Общее описание

**Shell Emulator** — это консольное приложение, которое эмулирует работу командной оболочки (shell) в операционной системе. Приложение позволяет пользователю работать с виртуальной файловой системой, загруженной из архива `.tar`, и поддерживает базовые команды:

- `ls`
- `cd`
- `cal`
- `chmod`
- `exit`

Эмулятор работает полностью в оперативной памяти, не создавая временных файлов или папок на диске.

## 2. Описание функций и настроек

### Основные команды

- **ls [\<path\>]**

  Отображает содержимое текущей директории или указанного пути.

  **Пример:**

  ```bash
  /> ls
  dir1
  dir2
  file1.txt
  file2.txt
  ```

- **cd \<path\>**

  Изменяет текущую директорию.

  Поддерживает:

  - `/` для перехода в корень.
  - `..` для возврата в родительский каталог.

  **Пример:**

  ```bash
  /> cd dir1
  /dir1> ls
  file3.txt
  ```

- **chmod \<mode\> \<file\>**

  Эмулирует изменение прав доступа к файлу. Режим задаётся трёхзначным числом, где каждая цифра от 0 до 7. Команда проверяет, существует ли файл, и отображает сообщение об изменении прав.

  **Пример:**

  ```bash
  /> chmod 755 file1.txt
  chmod: permissions of 'file1.txt' changed to 755
  ```

- **cal**

  Выводит календарь текущего месяца. Команда не принимает аргументов.

  **Пример:**

  ```bash
  /> cal
       November 2023
  Mo Tu We Th Fr Sa Su
         1  2  3  4  5
   6  7  8  9 10 11 12
  13 14 15 16 17 18 19
  20 21 22 23 24 25 26
  27 28 29 30
  ```

- **exit**

  Завершает работу эмулятора.

  **Пример:**

  ```bash
  /> exit
  ```

## 3. Требования и установка

### Требования

- Python 3.7 или выше.
- Файл `.tar` с виртуальной файловой системой (например, `vfs.tar`).

### Установка и запуск

1. Убедитесь, что у вас установлен Python необходимой версии.

2. Клонируйте репозиторий или скачайте файлы проекта.

3. Убедитесь, что файл `vfs.tar` находится в корневой директории проекта или укажите путь к вашему архиву.

4. Запустите эмулятор командой:

   ```bash
   python emulator.py vfs.tar
   ```

   или

   ```bash
   python emulator.py <path_to_tar>
   ```

## 4. Результаты прогона тестов

Эмулятор снабжён автоматическими тестами, покрывающими все его функции. Для каждой поддерживаемой команды написано по 3 теста.

### Запуск тестов

Для запуска тестов выполните команду:

```bash
python test_emulator.py
```

### Пример вывода

```bash
..................
----------------------------------------------------------------------
Ran 18 tests in 0.025s

OK
```

Это означает, что все тесты прошли успешно.

## 5. Примеры использования

### Использование команды ls и cd

```bash
/> ls
dir1
dir2
file1.txt
file2.txt

/> cd dir1
/dir1> ls
file3.txt

/dir1> cd ..
/> ls dir2
file4.txt
subdir1

/> cd dir2/subdir1
/dir2/subdir1> ls
file5.txt
```

### Использование команды chmod

```bash
/> chmod 755 file1.txt
chmod: permissions of 'file1.txt' changed to 755

/> chmod 999 file1.txt
chmod: invalid mode: '999'

/> chmod 755 nonexistent.txt
chmod: cannot access 'nonexistent.txt': No such file or directory
```

### Использование команды cal

```bash
/> cal
     November 2023
Mo Tu We Th Fr Sa Su
       1  2  3  4  5
 6  7  8  9 10 11 12
13 14 15 16 17 18 19
20 21 22 23 24 25 26
27 28 29 30
```
