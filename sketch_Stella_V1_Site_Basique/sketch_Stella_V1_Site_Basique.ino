#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <SPIFFS.h>

// Remplacez par vos informations WiFi
const char* ssid = "ESP32-Stella";
const char* password = "12345678";

// Création du serveur web
AsyncWebServer server(80);

void listSPIFFSFiles() {
  File root = SPIFFS.open("/");
  File file = root.openNextFile();
  while (file) {
    Serial.print("FILE: ");
    Serial.println(file.name());
    file = root.openNextFile();
  }
}

void setup() {
  // Initialiser la communication série
  Serial.begin(115200);

  // Initialiser SPIFFS
  if (!SPIFFS.begin(true)) {
    Serial.println("Erreur de montage SPIFFS");
    return;
  } else {
    Serial.println("Montage SPIFFS réussi");
  }

  // Lister les fichiers SPIFFS
  listSPIFFSFiles();

  // Démarrer le point d'accès Wi-Fi
  WiFi.softAP(ssid, password);

  // Vérifiez si le point d'accès Wi-Fi a démarré
  Serial.print("Adresse IP : ");
  Serial.println(WiFi.softAPIP());

  // Servir les fichiers statiques
  server.serveStatic("/", SPIFFS, "/").setDefaultFile("index.html");

  // Ajout des points de débogage pour les requêtes HTTP
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.println("Requête reçue pour /");
    request->send(SPIFFS, "/index.html", "text/html");
  });

  server.on("/style.css", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.println("Requête reçue pour /style.css");
    request->send(SPIFFS, "/style.css", "text/css");
  });

  server.on("/scripts.js", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.println("Requête reçue pour /scripts.js");
    request->send(SPIFFS, "/scripts.js", "application/javascript");
  });

  server.on("/images/Logo.ico", HTTP_GET, [](AsyncWebServerRequest *request){
    Serial.println("Requête reçue pour /images/Logo.ico");
    request->send(SPIFFS, "/images/Logo.ico", "image/x-icon");
  });

  server.onNotFound([](AsyncWebServerRequest *request){
    Serial.printf("Requête non trouvée: %s\n", request->url().c_str());
    request->send(404, "text/plain", "Not found");
  });

  // Démarrer le serveur
  server.begin();
}

void loop() {
  // Pas besoin de boucle pour cette vérification
}
