# **Linux CLI Cheatsheet for AQA Full Stack**

# 🟩 **1. SSH — Server Connection**

### Connection via key

ssh -i ~/.ssh/id_rsa user@server

Creating key pair

ssh-keygen -t rsa -b 4096 -C "aleks@exante"

Execute remote command

ssh user@server "tail -n 100 /var/log/app.log"

Port tunneling

ssh -L 8080:localhost:8000 user@server
🟩 2. Logs: tail, grep, less

2.1. tail — live log viewing

tail -f app.log

Live stream + filter

tail -f app.log | grep -E "ERROR|500|502|timeout"

Last N lines

tail -n 200 app.log

2.2. grep — quick search

Basic search

grep "ERROR" app.log

Multiple patterns

grep -E "ERROR|500|502|404" app.log

Case insensitive

grep -i "timeout" app.log

With line numbers

grep -n "Exception" app.log

Exclude lines

grep -v "healthcheck" app.log

Context around line

grep -C 3 "ERROR" app.log

Recursive search in directory

grep -R "jdbc.url" /etc/myapp

File names only

grep -Rl "database" /opt/project/

2.3. less — convenient viewing of large files

less app.log

Navigation:

/text — search

PgUp / PgDn — pages

G — end of file

g — beginning

q — exit

🟩 3. Performance: top, ps

View system load

top
Find java processes

ps aux | grep java
View memory and CPU
CPU% — whether service uses cores

RES — real memory

SWAP — whether swapping started (bad)

🟩 4. Network: curl, ss, iptables

Check healthcheck

curl -v <http://localhost:8080/health>

Check listening port

ss -tulpn | grep 8080

View firewall rules

sudo iptables -L -n -v

🟩 5. Typical QA Cases

Find errors for today

grep "2025-11-15" app.log | grep -E "ERROR|500|502"

Find chain of one request

grep -R "requestId=abc-123" /var/log/

Database crashes

grep -E "Connection refused|timeout|could not connect" app.log

Slow requests

grep -E "took=[0-9]+ms" app.log

NullPointer / Exception

grep -E "Exception|NullPointer" app.log

404/500/502 errors

grep -E " 404 | 500 | 502 " nginx-access.log
