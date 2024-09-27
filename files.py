#Задание 1
f = open('khvorostov.ru-log-Apr-2022.log')
ips = []
browsers = {}
all_requests = 0
first_request_time = ''
last_request_time = ''
for line in f:
    data = line.split()
    ip = data[0]
    if ip not in ips:
        ips.append(ip)
    if all_requests == 0:
        first_request_time = data[3] + data[4]
    else:
        last_request_time = data[3] + data[4]
    browser = data[-1]
    if browser in browsers.keys():
        browsers[browser] += 1
    else:
         browsers[browser] = 1
    all_requests += 1
f.close()
popular_browsers = sorted(browsers, key=browsers.get, reverse=True)
print("All requests: ", all_requests)
print("First request time: ", first_request_time)
print("Last request time: ", last_request_time)
print("Unique users: ", len(ips))
print("The most popular brawsers: ")
for i in range(0, 10):
    print(i + 1, ": ", popular_browsers[i])
print('-------------------------------------------')
#Задание2
f2 = open('khvorostov.ru-log-Apr-2022.log')
output_file = open('without_bots.log', "w")
bad_words = ["krowler", "crawler", "Bot", "bot", "python"]
for line in f2:
    check = True
    for word in bad_words:
        if word in line:
            check = False
            break
    if check:
        output_file.write(line)
f2.close()
output_file.close()

new_file = open('without_bots.log')
ips = []
browsers = {}
all_requests = 0
first_request_time = ''
last_request_time = ''

for line in new_file:
    data = line.split()
    ip = data[0]
    if ip not in ips:
        ips.append(ip)

    if all_requests == 0:
        first_request_time = data[3] + data[4]
    else:
        last_request_time = data[3] + data[4]

    browser = data[-1]
    if browser in browsers.keys():
        browsers[browser] += 1
    else:
         browsers[browser] = 1
    all_requests += 1

new_file.close()
popular_browsers = sorted(browsers, key=browsers.get, reverse=True)
print("All requests: ", all_requests)
print("First request time: ", first_request_time)
print("Last request time: ", last_request_time)
print("Unique users: ", len(ips))
print("The most popular brawsers: ")
for i in range(0, 10):
    print(i + 1, ": ", popular_browsers[i])
