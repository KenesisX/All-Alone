// ALLALONE — ESP32 host. Serves the app over its own Wi-Fi access point so a
// phone/laptop can open the UI with no internet. The sensors still come from
// the device running the browser; the ESP32 provides the UI + can be your
// LoRa/SDR bridge endpoint.
#include <WiFi.h>
#include <WebServer.h>
#include <LittleFS.h>

const char* AP_SSID = "ALLALONE";
const char* AP_PASS = "allalone123";   // >= 8 chars

WebServer server(80);

void serveApp() {
  File f = LittleFS.open("/index.html", "r");
  if (!f) { server.send(500, "text/plain", "index.html missing — run `pio run -t uploadfs`"); return; }
  server.streamFile(f, "text/html");
  f.close();
}

void setup() {
  Serial.begin(115200);
  if (!LittleFS.begin(true)) Serial.println("LittleFS mount failed");
  WiFi.mode(WIFI_AP);
  WiFi.softAP(AP_SSID, AP_PASS);
  Serial.print("AP up. Open  http://");
  Serial.println(WiFi.softAPIP());   // 192.168.4.1

  server.on("/", serveApp);
  server.on("/index.html", serveApp);
  // simple captive-portal redirect for any other path
  server.onNotFound([]() {
    server.sendHeader("Location", String("http://") + WiFi.softAPIP().toString(), true);
    server.send(302, "text/plain", "");
  });
  server.begin();
}

void loop() { server.handleClient(); }
