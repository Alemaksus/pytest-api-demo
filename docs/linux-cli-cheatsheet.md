# **Linux CLI Cheatsheet for AQA Full Stack**

# 🟩 **1. SSH — подключение к серверам**

### Подключение по ключу

ssh -i ~/.ssh/id_rsa user@server

Создание пары ключей

ssh-keygen -t rsa -b 4096 -C "aleks@exante"

Выполнить удалённую команду

ssh user@server "tail -n 100 /var/log/app.log"

Туннелирование порта

ssh -L 8080:localhost:8000 user@server
🟩 2. Логи: tail, grep, less

2.1. tail — живой просмотр логов

tail -f app.log

Живой поток + фильтр

tail -f app.log | grep -E "ERROR|500|502|timeout"

Последние N строк

tail -n 200 app.log

2.2. grep — быстрый поиск

Базовый поиск

grep "ERROR" app.log

Несколько шаблонов

grep -E "ERROR|500|502|404" app.log

Без учета регистра

grep -i "timeout" app.log

С номерами строк

grep -n "Exception" app.log

Исключить строки

grep -v "healthcheck" app.log

Контекст вокруг строки

grep -C 3 "ERROR" app.log

Поиск рекурсивно по каталогу

grep -R "jdbc.url" /etc/myapp

Только имена файлов

grep -Rl "database" /opt/project/

2.3. less — удобный просмотр больших файлов

less app.log

Навигация:

/text — поиск

PgUp / PgDn — страницы

G — конец файла

g — начало

q — выход

🟩 3. Производительность: top, ps

Смотреть загрузку системы

top
Найти java-процессы

ps aux | grep java
Посмотреть память и CPU
CPU% — использует ли сервис ядра

RES — реальная память

SWAP — начался ли свопинг (плохо)

🟩 4. Сеть: curl, ss, iptables

Посмотреть healthcheck

curl -v <http://localhost:8080/health>

Проверить слушающий порт

ss -tulpn | grep 8080

Посмотреть firewall-правила

sudo iptables -L -n -v

🟩 5. Типовые QA-кейсы

Найти ошибки за сегодня

grep "2025-11-15" app.log | grep -E "ERROR|500|502"

Найти цепочку одного запроса

grep -R "requestId=abc-123" /var/log/

Падения БД

grep -E "Connection refused|timeout|could not connect" app.log

Долгие запросы

grep -E "took=[0-9]+ms" app.log

NullPointer / Exception

grep -E "Exception|NullPointer" app.log

Ошибки 404/500/502

grep -E " 404 | 500 | 502 " nginx-access.log
