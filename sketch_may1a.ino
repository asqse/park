#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN_1   8     // 第一个 RC522 模块的复位引脚
#define SS_PIN_1    7    // 第一个 RC522 模块的 SPI Slave Select 引脚

#define RST_PIN_2   8     // 第二个 RC522 模块的复位引脚
#define SS_PIN_2    9     // 第二个 RC522 模块的 SPI Slave Select 引脚

MFRC522 mfrc522_1(SS_PIN_1, RST_PIN_1); // 创建第一个 MFRC522 实例
MFRC522 mfrc522_2(SS_PIN_2, RST_PIN_2); // 创建第二个 MFRC522 实例

void setup() {
  Serial.begin(9600); // 初始化串口通信
  SPI.begin(); // 初始化 SPI 总线
  mfrc522_1.PCD_Init(); // 初始化第一个 MFRC522 模块
  mfrc522_2.PCD_Init(); // 初始化第二个 MFRC522 模块
  Serial.println("Scan RFID cards...");
}

void loop() {
  // 检查第一个 RC522 模块是否有新的 RFID 卡
  if (mfrc522_1.PICC_IsNewCardPresent() && mfrc522_1.PICC_ReadCardSerial()) {
    // 获取卡的 UID
    String uid = "";
    for (byte i = 0; i < mfrc522_1.uid.size; i++) {
      uid.concat(String(mfrc522_1.uid.uidByte[i] < 0x10 ? "0" : ""));
      uid.concat(String(mfrc522_1.uid.uidByte[i], HEX));
    }
    uid.toUpperCase(); // 转换为大写字母
    Serial.print("1,"); // 第一个读卡器编号
    Serial.println(uid);
    mfrc522_1.PICC_HaltA(); // 暂停读取卡
  }

  // 检查第二个 RC522 模块是否有新的 RFID 卡
  if (mfrc522_2.PICC_IsNewCardPresent() && mfrc522_2.PICC_ReadCardSerial()) {
    // 获取卡的 UID
    String uid = "";
    for (byte i = 0; i < mfrc522_2.uid.size; i++) {
      uid.concat(String(mfrc522_2.uid.uidByte[i] < 0x10 ? "0" : ""));
      uid.concat(String(mfrc522_2.uid.uidByte[i], HEX));
    }
    uid.toUpperCase(); // 转换为大写字母
    Serial.print("2,"); // 第二个读卡器编号
    Serial.println(uid);
    mfrc522_2.PICC_HaltA(); // 暂停读取卡
  }
}
