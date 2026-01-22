#!/bin/bash

echo "Демонстрация управления процессами"
echo ""

# Запуск sleep в фоне
sleep 60 &
sleep 40 &
sleep 20 &

echo "Запущены 3 процесса sleep:"
jobs -l
echo ""

