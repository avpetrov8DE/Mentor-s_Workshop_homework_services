#!/bin/bash

read -p "Введите число: " number

# Проверяем, что введено число
if ! [[ "$number" =~ ^-?[0-9]+$ ]]; then
    echo "Ошибка: Введите целое число!"
    exit 1
fi

echo ""
echo "1. Проверка числа:"
echo "-------------------------------"

# Проверяем положительное, отрицательное или ноль
if [ "$number" -gt 0 ]; then
    echo "Число $number - ПОЛОЖИТЕЛЬНОЕ"
elif [ "$number" -lt 0 ]; then
    echo "Число $number - ОТРИЦАТЕЛЬНОЕ"
else
    echo "Число $number - НОЛЬ"
fi

echo ""
echo "2. Подсчет с помощью while"
echo "---------------------------------------------------------"

if [ "$number" -gt 0 ]; then
    count=1
    while [ "$count" -le "$number" ]; do
        echo "  $count"
        count=$((count + 1))
    done
elif [ "$number" -eq 0 ]; then
    echo "Введен ноль"
else
    echo "Введено отрицательное число"
fi
