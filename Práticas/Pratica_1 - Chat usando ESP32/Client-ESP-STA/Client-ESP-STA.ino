/*
Aplicação para ESP 32 com:
- Conexão a Ponto de Acesso Wi-Fi (AP) existente
- cliente TCP
- bridge de serial para segmentos TCP
- chat simples
*/

#include <WiFi.h>

//credenciais do servidor
String hostname = "Fred ESP32 Client Node";
const char* ssid     = "Fred-ESP32-AP";
//sem senha, para colocar adicionar: const char* password = "123456789";
//Endereço IP e porta do servidor ao qual o cliente irá se conectar
IPAddress TCP_server_IP(192, 168, 1, 1);
int TCP_server_port = 55555;

//gerenciador para cliente(s)
WiFiClient client;

//flag para modo chat
boolean chat_on = false;

//variável para máquina de estados
byte estado = 0;

//buffer de recebimento TCP
String TCPinputString = "";

//buffer de recebimento Serial
String SerialInputString = "";         // a string to hold incoming data
boolean SerialStringComplete = false;  // whether the string is complete

//procedimento de leitura da serial
void Serial_read();

//procedimento de leitura do buffer de recebimento do TCP
void TCPbuffer_read();

void setup(){
  Serial.begin(115200);

  Serial.println("Aplicacao Bridge Serial-2-Wi-Fi-TCP-socket");
  // Connect to Wi-Fi network with SSID and password
  Serial.println("Configurando ESP como cliente (station).");
  // Remove the password parameter, if you want the AP (Access Point) to be open
  
  WiFi.mode(WIFI_STA);	//modo station

  WiFi.begin(ssid); // sem password

  Serial.print("Tentando conectar ao servidor.");
  //Conectando ao AP
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi conectado!");
  Serial.print("Endereco IP: ");
  Serial.println(WiFi.localIP());
}

void loop(){
  //máquina de estados
  switch (estado){
    case 0: //tentando conectar
      if (!client.connect(TCP_server_IP, TCP_server_port)){
        chat_on = false;
        Serial.println("Conexao falhou!");
        Serial.println("Esperando 2 segundos para nova tentativa...");
        delay(2000);
        return;
      }
      else
        estado = 1;
      break;
    case 1: //conexão com servidor TCP
      Serial.println("Conexao TCP estabelecida com o servidor!");
      estado = 2;
      break;
    case 2: //configuração inicial do chat - ambos os lados com chat ON
      TCPbuffer_read();
        
      if (TCPinputString == "Chat ON"){
        client.print("Chat ON ACK");
        client.flush();
        delay(500);
        Serial.println("Chat iniciado - escreva uma mensagem para o servidor na serial.");
        Serial.println("###############################################################");
        chat_on = true;
        TCPinputString = "";
        estado = 3;
      }
      break;
    case 3:
      TCPbuffer_read();

      if (TCPinputString != "" ){
        Serial.print("Servidor: " + TCPinputString);
        TCPinputString = "";
      }        

      Serial_read();
      
      if (SerialInputString != "" && SerialStringComplete){
        Serial.print("Cliente: " + SerialInputString);
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
      if (inChar == '\n') //10d/0Ah - LF (\n) ; 13d/0Dh - CR (\r)
      {
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
        
    //debug
    //Serial.print("Segmento com: [");
    while (client.available() > 0)//Armazena cada Byte (letra/char) na String para formar a mensagem recebida.
    {
      char z = client.read();
      //Serial.write(z);
      TCPinputString += z;
      recv_bytes++;
    }
    //Serial.println("]");
    
    //Mostra a mensagem recebida do cliente no Serial Monitor.
    //Serial.print("Segmento recebido com ");
    //Serial.print(recv_bytes );
    //Serial.println(" bytes");
    //Serial.println("Mensagem do servidor: " + TCPinputString );
    client.flush();
  }
}
