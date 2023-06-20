/*
Aplicação para ESP 32 com:
- Ponto de Acesso Wi-Fi (AP)
- servidor TCP
- bridge de serial para segmentos TCP
- chat simples
*/

#include <WiFi.h>

//credenciais/configurações do AP e servidor
String hostname = "REDES AP ESP32 Node";
const char* ssid     = "REDES-ESP32-AP";

//sem senha, para colocar adicionar: const char* password = "123456789";
IPAddress IP(192, 168, 1, 1);
IPAddress NMask(255, 255, 255, 0);
int TCP_server_port = 55555;

//Configurando servidor TCP na porta (bind)
WiFiServer server(TCP_server_port);

//gerenciador para cliente(s)
WiFiClient client;

//variável para armazenar clienes conectados
byte clients_connected = 0;

//flag para modo chat
boolean chat_on = false;

//variável para máquina de estados
byte estado = 0;

//buffers de recebimento TCP
String TCPinputString = "";

//buffers de recebimento Serial
String SerialInputString = "";
boolean SerialStringComplete = false;

// procedimento de leitura da serial
void Serial_read();

// procedimento de leitura do buffer de recebimento do TCP
void TCPbuffer_read();

// teste ainda nao funciona
byte ack_clients = 0;
IPAddress clients[4];

void setup(){
  Serial.begin(115200);

  Serial.println("Aplicacao Bridge Serial-2-Wi-Fi-TCP-socket");
  Serial.println("Configurando ESP como ponto de acesso (AP - Access Point).");
  
  WiFi.mode(WIFI_AP);	//access point mode: stations can connect to the ESP32
  
  WiFi.softAP(ssid, NULL, 1, 0, 4);
  /* WiFi.softAPIP parameters
    ssid: name for the access point – maximum of 63 characters;
    password: minimum of 8 characters; set to NULL if you want the access point to be open;
    channel: Wi-Fi channel number (1-13)
    ssid_hidden: (0 = broadcast SSID, 1 = hide SSID)
    max_connection: maximum simultaneous connected clients (1-4)
  */
  WiFi.onEvent(WiFiStationConnected, SYSTEM_EVENT_AP_STACONNECTED);
  WiFi.onEvent(WiFiStationDisconnected, SYSTEM_EVENT_AP_STADISCONNECTED);
  Serial.println("Esperando 100 ms para AP_START...");
  delay(100);

  Serial.println("Configurando AP com softAPConfig");
  WiFi.setHostname(hostname.c_str()); //define hostname
  WiFi.softAPConfig(IP, IP, NMask);

  server.begin();
  Serial.println("##### Informações do AP #####");
  Serial.print("IP: [");
  Serial.print(WiFi.softAPIP());
  Serial.print("] - Mascara de Subrede: [");
  Serial.print(NMask);
  Serial.print("] - MAC: [");
  Serial.print(WiFi.softAPmacAddress());
  Serial.print("] - servidor TCP na porta: [");
  Serial.print(TCP_server_port);
  Serial.println("]");
  /*
  ver endereço de broadcast -> softAPBroadcastIP
  */
}

void loop(){
  //máquina de estados
  switch (estado){
    case 0: //Disponabiliza o servidor para o cliente se conectar.
      client = server.available();//Disponabiliza o servidor para o cliente se conectar.
      delay(100);
      //cliente solicita/estabelece conexao TCP
      if (client && client.connected()) 
        estado = 1;
      break;
    case 1: //reconhece cliente
      if (clients_connected > ack_clients){
        Serial.print("Novo cliente! ");
        Serial.print( clients_connected);
        Serial.println(" clientes conectados.");
        Serial.print("IP do cliente: ");
        Serial.println(client.remoteIP());
        clients[ack_clients] = client.remoteIP();
        Serial.println("Conexao TCP estabelecida com o cliente!");
        ack_clients++;
      }
      estado = 2;
      break;
    case 2: //configura fluxos de dados
      //envia Chat ON ao cliente
      client.print("Chat ON");
      client.flush();
      delay(500);

      TCPbuffer_read();

      if (TCPinputString == "Chat ON ACK"){
        Serial.println("Chat iniciado - escreva uma mensagem para o cliente na serial.");
        Serial.println("##############################################################");
        chat_on = true;
        TCPinputString = "";
        estado = 3;
      }
      break;
    case 3: //chat bidirecional
      TCPbuffer_read();

      if (TCPinputString != ""){
        Serial.print("Cliente: " + TCPinputString);
        TCPinputString = "";        
      }

      Serial_read();
      
      if (SerialInputString != "" && SerialStringComplete){
        Serial.print("Servidor: " + SerialInputString);
        client.print(SerialInputString);
        SerialStringComplete = false;
        SerialInputString = "";
      }
      break;
  }      
}

//procedimento de leitura de caracteres da serial
void Serial_read(){
  if (Serial.available()){
    //Serial.println("Bytes disponiveis na serial");
    while (Serial.available()){
      //ler caracter
      char inChar = (char)Serial.read();
      SerialInputString += inChar;
      // if the incoming character is a newline, set a flag
      // so the main loop can do something about it:
      if (inChar == '\n'){ //10d/0Ah - LF (\n) ; 13d/0Dh - CR (\r)
        SerialStringComplete = true;
        //Serial.print("mensagem: ");
        //Serial.print(SerialinputString);
      }        
    }
  }
}

//procedimento de leitura do segmento de dados
void TCPbuffer_read(){
  if (client.available() > 0){
    TCPinputString = "";
    byte recv_bytes = 0;
        
    // Armazena cada Byte (letra/char) na String para formar a mensagem recebida.
    while (client.available() > 0){
      char z = client.read();
      //Serial.write(z);
      TCPinputString += z;
      recv_bytes++;
    }
    
    //Mostra a mensagem recebida do cliente no Serial Monitor.
    //Serial.print("Segmento recebido com ");
    //Serial.print(recv_bytes );
    //Serial.println(" bytes");
    //Serial.println("Mensagem do cliente: " + TCPinputString );
    client.flush();
  }
}

//interrupção configurada para detectar conexão ao AP
void WiFiStationConnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Host conectado ao AP!");
  Serial.print("Numero de host(s) conectados: ");
  Serial.println(WiFi.softAPgetStationNum());
  delay(500);
  clients_connected++;
}

//interrupção configurada para detectar desconexão do AP
void WiFiStationDisconnected(WiFiEvent_t event, WiFiEventInfo_t info){
  Serial.println("Host desconectado do AP!");
  Serial.print("Numero de host(s) conectados: ");
  Serial.println(WiFi.softAPgetStationNum());
  delay(500);
  clients_connected--;
}
