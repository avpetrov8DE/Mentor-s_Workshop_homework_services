#!/bin/bash

greet() {
    echo "Hello, $1"
}

add() {
    echo $(($1 + $2))
}

echo '1. Функция префикса Hello'
greet "World"
echo '2. Функция сложения 2 чисел'
result=$(add 5 3)
echo "5 + 3 = $result"
