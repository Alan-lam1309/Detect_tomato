#include "StepperMotor.h"// thư viện cung cấp chức năng để điều khiển steeper
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>
#include <NTPClient.h>

#define DIR0_PIN D3   //D3
#define PUL0_PIN D4   //D4
#define HOME0_PIN D5  //D2
#define MAN_PIN D6    //D6
#define AUTO_PIN D7   // D7

StepperMotor stepper(PUL0_PIN, DIR0_PIN);
#include <Firebase_ESP_Client.h>

// Provide the RTDB payload printing info and other helper functions.
#include <addons/RTDBHelper.h>

/* 1. Define the WiFi credentials */
#define WIFI_SSID "Huy Huynh"
#define WIFI_PASSWORD "12345@abcd"

/* 2. If work with RTDB, define the RTDB URL and database secret */
#define DATABASE_URL "detect-tomato-default-rtdb.firebaseio.com"  //<databaseName>.firebaseio.com or <databaseName>.<region>.firebasedatabase.app
#define DATABASE_SECRET "kdo64W2UAuoXBhDp4uBFtqoAki4SXX2uuj66qYLD"

WiFiUDP ntpUDP;
NTPClient timeClient(ntpUDP, "pool.ntp.org");

/* 3. Define the Firebase Data object */
FirebaseData fbdo;

/* 4, Define the FirebaseAuth data for authentication data */
FirebaseAuth auth;

/* Define the FirebaseConfig data for config data */
FirebaseConfig config;
long stepsPerUnit = 40;  //pulse/mm //số xung cần thiết để di chuyển động cơ 1 mm
long target = 0;// vị trí mục tiêu của động cơ steepper tính bằng số bước(steps)

//motor run//giá trị ban đầu cho các cờ chạy động cơ(M1, M2, M3, M4)
bool M1 = 0;  //ZRN - go home
bool M2 = 0;  //Go to position MAN
bool M3 = 0;  //Go as auto
bool M4 = 0;  //Go to 0 from auto
//motor pulse value// Giá trị xung động cơ P
long P = 100;
//motor frequency// tần số động cơ(F1)
long F1 = 5000;
//motor creep frequency// Tần số di chuyển chậm(F2)
long F2 = 100;
//circle
long N = 5;  //so lan chay auto
//delay motor// Thời gian trễ động cơ
long T = 1000;
//position to go  //chay den vi tri pos
long distance = 100;  //chay auto theo tung khoang


void setup() {
  Serial.begin(9600);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(300);
  }
  Serial.println();
  Serial.print("Connected with IP: ");
  Serial.println(WiFi.localIP());
  Serial.println();

  Serial.printf("Firebase Client v%s\n\n", FIREBASE_CLIENT_VERSION);

  /* Assign the certificate file (optional) */
  // config.cert.file = "/cert.cer";
  // config.cert.file_storage = StorageType::FLASH;

  /* Assign the database URL and database secret(required) */
  config.database_url = DATABASE_URL;
  config.signer.tokens.legacy_token = DATABASE_SECRET;

  Firebase.reconnectWiFi(true);

  /* Initialize the library with the Firebase authen and config */
  Firebase.begin(&config, &auth);
  timeClient.begin();
  timeClient.setTimeOffset(25200);

  pinMode(MAN_PIN, INPUT_PULLUP);
  pinMode(AUTO_PIN, INPUT_PULLUP);
  delay(2000);
  //set chay theo vi tri xac dinh
  // M2 = true;
  // target = position * stepsPerUnit;
  //set chay theo auto tung buoc
  // M3 = true;
  // target = 0;
}

void runAndTakePhoto(position,F1,){
  stepper.DRVA(position, F1);
  Serial.printf("Set addPic values... %s\n", Firebase.RTDB.setString(&fbdo, F("/device/addPic"), "YES") ? "ok" : fbdo.errorReason().c_str());
  while(true){
    Firebase.RTDB.getString(&fbdo, F("/device/addPic"));
    String addPic = fbdo.to<String>()
    if(addPic == 'NO'){
      break;
    }
  }
  if (stepper.getExeCompleteFlag()) {// Kiểm tra xem quá trình thực thi đã hoàn thành hay chưa
    stepper.DRVA(0, F1);
    Serial.printf("Set run values... %s\n", Firebase.RTDB.setInt(&fbdo, F("/device/run"), 0) ? "ok" : fbdo.errorReason().c_str());
  }
}

void loop(){
  Firebase.RTDB.getString(&fbdo, F("/device/status"));
  String status = fbdo.to<String>()
  if( status == 'manual'){
    Firebase.RTDB.getInt(&fbdo, F("/device/run"));
    int run = fbdo.to<int>();
    if(run == 1){
      Firebase.RTDB.getInt(&fbdo, F("/device/location"));
      int fbpostion = fbdo.to<int>();
      int position = fbpostion * stepsPerUnit;
      runAndTakePhoto(position,F1)
    }
  }
  if( status == 'auto'){
    int currentHour = timeClient.getHours();
    int currentMinute = timeClient.getMinutes();
    if(currentHour == 9 && currentMinute == 0){
      int i = 0;
      while(i<N){
        position = position + distance * stepsPerUnit
        runAndTakePhoto(position,F1)
      }
    }
    if(currentHour == 13 && currentMinute == 0){
      int i = 0;
      while(i<N){
        position = position + distance * stepsPerUnit
        runAndTakePhoto(position,F1)
      }
    }
    if(currentHour == 17 && currentMinute == 0){
      int i = 0;
      while(i<N){
        position = position + distance * stepsPerUnit
        runAndTakePhoto(position,F1)
      }
    }
  }
}

// void loop() {
//   // Serial.println(digitalRead(HOME0_PIN));
//   // kiểm tra trạng thái hoạt động của MAN_PIN và AUTO_PIN
//   if (digitalRead(MAN_PIN) == 0) {
//     M2 = true;
//     target = position * stepsPerUnit;// đặt vị trí mục tiêu
//   }
//   if (digitalRead(AUTO_PIN) == 0) {
//     M3 = true;
//     target = 0;// đặt ví trí mục tiêu là 0
//   }
//   // if (M1) {
//   //   stepper.ZRN(F1, F2, HOME0_PIN);
//   //   if (stepper.getExeCompleteFlag()) {
//   //     M1 = false;
//   //     delay(1000);
//   //     Serial.println("go home");
//   //   }
//   // } else
//   if (M2) {// nếu M2 true
//     stepper.DRVA(target, F1);// thực hiện hàm DRVA của động cơ stepper để di chuyển đến vị trí mục tiêu với tần số F1
//     if (stepper.getExeCompleteFlag()) {// Kiểm tra xem quá trình thực thi đã hoàn thành hay chưa
//       M2 = false;
//       Serial.println("go to set position");
//     }
//   } else if (M3) {// Nếu M3 true
//     stepper.DRVA(target, F1);//hực thi hàm DRVA của động cơ stepper để di chuyển đến vị trí mục tiêu với tần số F1. Kiểm tra xem quá trình thực thi đã hoàn thành hay chưa.
//     if (stepper.getExeCompleteFlag()) {
//       Serial.println(stepper.getCurrentPosition());
//       if (!M4 && stepper.getCurrentPosition() == N * distance * stepsPerUnit) {//Nếu cờ M4 không được đặt và vị trí hiện tại của động cơ bằng N * distance * stepsPerUnit
//         Serial.println("auto go to 0");//đặt cờ M4 thành true, đặt vị trí mục tiêu là 0 và in một thông báo cho biết đang thực hiện di chuyển tự động về vị trí 0.
//         target = 0;
//         M4 = true;
//       } else if (stepper.getCurrentPosition() == 0 && M4) {//Nếu vị trí hiện tại của động cơ là 0 và cờ M4 được đặt
//         M3 = false;//đặt cờ M3 thành false
//         Serial.println("auto go finish");// in một thông báo cho biết di chuyển tự động đã hoàn thành
//         M4 = false;//đặt lại cờ M4
//       } else {//Trong trường hợp khác, tăng vị trí mục tiêu lên distance * stepsPerUnit và trì hoãn trong T mili giây
//         target = target + distance * stepsPerUnit;
//       }
//       delay(T);
//     }
//   }
// }