#!/bin/bash

# Проверка наличия аргумента
if [ $# -ne 1 ]; then
    echo "Использование: $0 <путь_к_архиву.tar>"
    exit 1
fi

TAR_PATH="$1"

# Проверка существования файла
if [ ! -f "$TAR_PATH" ]; then
    echo "Ошибка: файл '$TAR_PATH' не найден"
    exit 1
fi

# Создание временной директории
TEMP_DIR=$(mktemp -d)
ORIGINAL_DIR=$(pwd)
CURRENT_DIR="$TEMP_DIR"

# Распаковка tar-архива во временную директорию
tar -xf "$TAR_PATH" -C "$TEMP_DIR"

# Функция для очистки временной директории при выходе
function cleanup {
    rm -rf "$TEMP_DIR"
    exit
}

# Обработка Ctrl+C и команды exit
trap cleanup SIGINT

# Запуск эмулятора оболочки
while true; do
    # Вывод приглашения
    echo -n "$(basename "$CURRENT_DIR")$ "
    read -r CMD_LINE
    # Разбиение команды на массив
    IFS=' ' read -r -a CMD_ARRAY <<< "$CMD_LINE"
    CMD="${CMD_ARRAY[0]}"
    ARGS=("${CMD_ARRAY[@]:1}")

    case "$CMD" in
        ls)
            if [ "${#ARGS[@]}" -eq 0 ]; then
                ls -A "$CURRENT_DIR"
            else
        	TARGET="$CURRENT_DIR/${ARGS[0]}"
        	# Проверяем, что путь существует и находится внутри виртуальной ФС
        	if [ -e "$TARGET" ] && [[ "$(realpath "$TARGET")" == "$TEMP_DIR"* ]]; then
        	    ls -A "$TARGET"
        	else
        	    echo "ls: невозможно получить доступ к '${ARGS[0]}': Нет такого файла или каталога"
        	fi
	    fi
            ;;
        cd)
            if [ "${#ARGS[@]}" -eq 0 ]; then
                CURRENT_DIR="$TEMP_DIR"
            else
                NEW_DIR="$CURRENT_DIR/${ARGS[0]}"
                # Получаем реальный путь
                NEW_DIR="$(realpath "$NEW_DIR" 2>/dev/null)"
                if [ -d "$NEW_DIR" ] && [[ "$NEW_DIR" == "$TEMP_DIR"* ]]; then
                    CURRENT_DIR="$NEW_DIR"
                else
                    echo "cd: ${ARGS[0]}: Нет такого каталога"
                fi
            fi
            ;;
        exit)
            cleanup
            ;;
        cal)
            cal
            ;;
        chmod)
    	    if [ "${#ARGS[@]}" -ne 2 ]; then
                echo "chmod: неправильное количество аргументов"
    	    else
        	MODE="${ARGS[0]}"
        	TARGET="$CURRENT_DIR/${ARGS[1]}"
       		# Проверяем, что режим состоит из 3 или 4 цифр от 0 до 7
       		if [[ ! "$MODE" =~ ^[0-7]{3,4}$ ]]; then
        	    echo "chmod: недопустимый режим: '$MODE'"
       		elif [ -e "$TARGET" ] && [[ "$(realpath "$TARGET")" == "$TEMP_DIR"* ]]; then
            	    chmod "$MODE" "$TARGET" 2>/dev/null
            	    if [ $? -ne 0 ]; then
                	echo "chmod: не удалось изменить права доступа к '${ARGS[1]}'"
            	    fi
        	else
            	    echo "chmod: невозможно получить доступ к '${ARGS[1]}': Нет такого файла или каталога"
        	fi
    	    fi
    	    ;;
        cat)
            if [ "${#ARGS[@]}" -eq 0 ]; then
                echo "cat: отсутствует файл для чтения"
            else
                TARGET="$CURRENT_DIR/${ARGS[0]}"
                if [ -f "$TARGET" ] && [[ "$(realpath "$TARGET")" == "$TEMP_DIR"* ]]; then
                    cat "$TARGET"
                else
                    echo "cat: ${ARGS[0]}: Нет такого файла"
                fi
            fi
            ;;
        *)
            if [ -n "$CMD" ]; then
                echo "$CMD: команда не найдена"
            fi
            ;;
    esac
done
