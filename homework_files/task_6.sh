#!/bin/bash

echo "1. Содержимое input.txt:"
cat input.txt
echo ""

echo "2. Подсчет строк (wc -l) -> output.txt"
wc -l input.txt > output.txt
echo "Результат сохранен в output.txt"
echo ""

echo "3. Ошибка ls -> error.log"
ls несуществующий_файл.txt 2> error.log
echo "Ошибка сохранена в error.log"
echo ""


echo "Созданные файлы:"
ls -l input.txt output.txt error.log 2>/dev/null || echo "Некоторые файлы не найдены"
echo ""

