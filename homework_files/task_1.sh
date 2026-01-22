#!/bin/bash

echo "1. Список всех файлов в текущей директории с указанием типа:"
for item in *
do
    if [ -f "$item" ]; then
        echo "Обычный файл: $item"
    elif [ -d "$item" ]; then
        echo "Каталог: $item"
    elif [ -L "$item" ]; then
        echo "Ссылка: $item"
    elif [ -c "$item" ]; then
        echo "Символьное устройство: $item"
    elif [ -b "$item" ]; then
        echo "Блочное устройство: $item"
    elif [ -p "$item" ]; then
        echo "FIFO: $item"
    elif [ -S "$item" ]; then
        echo "Сокет: $item"
    fi
done

echo ""

echo "2. Проверка наличия файла из аргумента:"
if [ $# -eq 0 ]; then
    echo "Файл для проверки не указан"
else
    filename="$1"
    if [ -e "$filename" ]; then
        echo "Файл '$filename' существует"
    else
        echo "Файл '$filename' не существует"
    fi
fi

echo ""

echo "3. Информация о каждом файле (имя и права доступа):"
for file in *
do
    if [ -e "$file" ]; then
        permissions=$(ls -ld "$file" | awk '{print $1}')
        echo "Имя: $file, Права доступа: $permissions"
    fi
done
