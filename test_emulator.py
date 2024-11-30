import unittest
import os
import sys
import io
from emulator import ShellEmulator
from unittest.mock import patch
import calendar
from datetime import datetime
from contextlib import redirect_stdout


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Используем существующий архив vfs.tar
        cls.tar_path = 'vfs.tar'
        if not os.path.exists(cls.tar_path):
            raise FileNotFoundError(f"Тестовый архив {cls.tar_path} не найден.")
        cls.emulator = ShellEmulator(cls.tar_path)

    def setUp(self):
        # Сбрасываем текущий путь эмулятора перед каждым тестом
        self.emulator.current_path = []

    # Тесты для команды ls
    def test_ls_root(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.ls([])
            output = buf.getvalue().splitlines()
        expected_entries = ['dir1', 'dir2', 'file1.txt', 'file2.txt']
        self.assertCountEqual(output, expected_entries)

    def test_ls_dir1(self):
        self.emulator.current_path = ['dir1']
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.ls([])
            output = buf.getvalue().splitlines()
        expected_entries = ['file3.txt']
        self.assertEqual(output, expected_entries)

    def test_ls_nonexistent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.ls(['nonexistent'])
            output = buf.getvalue().strip()
        self.assertIn('Path not found: nonexistent', output)

    # Тесты для команды cd
    def test_cd_root(self):
        self.emulator.current_path = ['dir1']
        self.emulator.cd(['/'])
        self.assertEqual(self.emulator.current_path, [])

    def test_cd_parent(self):
        self.emulator.current_path = ['dir1']
        self.emulator.cd(['..'])
        self.assertEqual(self.emulator.current_path, [])

    def test_cd_nonexistent(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.cd(['nonexistent'])
            output = buf.getvalue().strip()
        self.assertIn('Path not found: nonexistent', output)

    # Тесты для команды cal
    def test_cal(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.cal()
            output = buf.getvalue()
        now = datetime.now()
        self.assertIn(calendar.month_name[now.month], output)

    def test_cal_output(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.cal()
            output = buf.getvalue()
        self.assertTrue(len(output) > 0)

    def test_cal_format(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.cal()
            output = buf.getvalue()
        self.assertIn(str(datetime.now().year), output)

    # Тесты для команды chmod
    def test_chmod_valid(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.chmod(['755', 'file1.txt'])
            output = buf.getvalue().strip()
        self.assertIn("chmod: permissions of 'file1.txt' changed to 755", output)

    def test_chmod_invalid_mode(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.chmod(['999', 'file1.txt'])
            output = buf.getvalue().strip()
        self.assertIn("chmod: invalid mode: '999'", output)

    def test_chmod_nonexistent_file(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator.chmod(['755', 'nonexistent.txt'])
            output = buf.getvalue().strip()
        self.assertIn("chmod: cannot access 'nonexistent.txt': No such file or directory", output)

    # Тесты для команды exit
    def test_exit_command(self):
        with patch('builtins.input', side_effect=['exit']):
            with self.assertRaises(SystemExit):
                self.emulator.run()

    def test_exit_message(self):
        with patch('builtins.input', side_effect=['exit']):
            with patch('sys.stdout', new=io.StringIO()) as fake_out:
                try:
                    self.emulator.run()
                except SystemExit:
                    pass
                output = fake_out.getvalue()
                self.assertIn("Shell Emulator started. Type 'exit' to quit.", output)

    def test_exit_in_handle_command(self):
        with self.assertRaises(SystemExit):
            self.emulator._handle_command('exit')

    # Дополнительные тесты
    def test_handle_command_unknown(self):
        with io.StringIO() as buf, redirect_stdout(buf):
            self.emulator._handle_command('unknowncommand')
            output = buf.getvalue().strip()
        self.assertIn("Command 'unknowncommand' not found.", output)

    def test_navigate_to_path(self):
        path = ['dir1']
        dir_dict = self.emulator._navigate_to_path(path)
        self.assertIsInstance(dir_dict, dict)
        self.assertIn('file3.txt', dir_dict)

    def test_navigate_to_nonexistent_path(self):
        path = ['nonexistent']
        with self.assertRaises(FileNotFoundError):
            self.emulator._navigate_to_path(path)


if __name__ == '__main__':
    unittest.main()
