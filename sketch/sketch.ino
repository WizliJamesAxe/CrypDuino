#include <AESLib.h>
int i=0, crypt_mode;
char data[] = "this16bytestring";
uint8_t key[] = {0xa7, 0x52, 0xa5, 0x87, 0x6b, 0x6b, 0xec, 0x93, 
                 0x98, 0x3e, 0xc7, 0x7f, 0x9c, 0x43, 0x92, 0x4a, 
                 0xf5, 0x2c, 0xec, 0x81, 0xe4, 0xc8, 0x28, 0x25, 
                 0x52, 0x5b, 0x2a, 0x76, 0xbc, 0xf1, 0xa1, 0x54};

void setup() {
  Serial.begin(57600); 
}

void loop() {
  while (Serial.available()) {
    if (i != 0){
      data[i-1] = (char)Serial.read();    
    } else{
      crypt_mode = (char)Serial.read();
    }
    
    i=i+1;
    
    if (i == 17){
      if (crypt_mode == (char)0xaa) {
        aes256_enc_single(key, data);   
      } else if (crypt_mode == (char)0xbb){
        aes256_dec_single(key, data);
      }
      Serial.write(data);
      i = 0;
    }
  }    
}
