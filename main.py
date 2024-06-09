import network
import socket
import machine
import time

# Configuration de l'ESP32 en mode AP
ssid = 'ESP32-AP'
password = '12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password, authmode=network.AUTH_WPA_WPA2_PSK)

print('Setting up AP...')
while not ap.active():
    time.sleep(1)
print('AP config:', ap.ifconfig())

# Configurer la photorésistance
ldr_pin = 36  # Broche où la photorésistance est connectée
ldr = machine.ADC(machine.Pin(ldr_pin))
ldr.atten(machine.ADC.ATTN_11DB)  # Pour lire toute la gamme de 0 à 3.3V

# Configurer le capteur de température LM35
lm35_pin = 34  # Broche où le LM35 est connecté
lm35 = machine.ADC(machine.Pin(lm35_pin))
lm35.atten(machine.ADC.ATTN_11DB)  # Pour lire toute la gamme de 0 à 3.3V

# Fonction pour lire les fichiers
def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()

# Fonction pour lire les fichiers binaires (images)
def read_binary_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

# Fonction pour lire la température en degrés Celsius à partir du LM35
def read_temperature():
    raw_value = lm35.read()
    voltage = raw_value / 4095.0 * 3.3  # Conversion de la valeur brute en tension
    temperature = voltage * 100  # Conversion de la tension en température
    return temperature

# Création du serveur web
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Content = {}'.format(request))

    if 'GET / ' in request or 'GET /index.html' in request:
        response = read_file('/index.html')
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/html\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /style.css' in request:
        response = read_file('/style.css')
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/css\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /script.js' in request:
        response = read_file('/script.js')
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: application/javascript\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /FondSite.jpg' in request:
        response = read_binary_file('/FondSite.jpg')
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: image/jpeg\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /Logo.ico' in request:
        response = read_binary_file('/Logo.ico')
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: image/x-icon\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /ldr' in request:
        ldr_value = ldr.read()
        if ldr_value < 2000:
            ldr_status = "CubeSat Exposé"
        else:
            ldr_status = "CubeSat en Zone d'ombre"
        response = "LDR Value: {}\nStatus: {}".format(ldr_value, ldr_status)
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/plain\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    elif 'GET /temperature' in request:
        temperature = read_temperature()
        response = "Temperature: {:.2f}°C".format(temperature)
        cl.send('HTTP/1.1 200 OK\n')
        cl.send('Content-Type: text/plain\n')
        cl.send('Connection: close\n\n')
        cl.sendall(response)
    else:
        cl.send('HTTP/1.1 404 Not Found\n')
        cl.send('Content-Type: text/html\n')
        cl.send('Connection: close\n\n')
        cl.sendall('<h1>404 Not Found</h1>')

    cl.close()

