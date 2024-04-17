#include <Arduino.h>
#include <Wire.h>

#define PRINTBIN(Num)                                           
#ifdef DEBUG                                                   \
  for (uint32_t t = (1UL << (sizeof(Num) * 8) - 1); t; t >>= 1) \
  Serial.write(Num &t ? '1' : '0') 
#endif

#define DEBUG_PRINTLN(x) 
#ifdef DEBUG              \
  Serial.println(x);     
#endif

#define DEBUG_PRINT(x) 
#ifdef DEBUG              \
  Serial.print(x);     
#endif


// Pins assigned to addMT8808_RESETs lines MT8808_AX0-MT8808_AX2 and MT8808_AY0-MT8808_AY2
const int MT8808_AX0 = 10;
const int MT8808_AX1 = 16;
const int MT8808_AX2 = 14;
const int MT8808_AY0 = 15;
const int MT8808_AY1 = A0;
const int MT8808_AY2 = A1;

const int MT8808_ADDRESS_LINES[6] = {
    MT8808_AX0, MT8808_AX1, MT8808_AX2,
    MT8808_AY0, MT8808_AY1, MT8808_AY2};

const int MT8808_DAT = A3;   // MT8808 Data
const int MT8808_STR = 6;    // MT8808 Strobe
const int MT8808_RESET = A2; // MT8808 Reset

const int RESTORE = 4;   // Restore key in
const int C64_RESET = 2; // C64 Reset
const int C64_EXROM = 3; // C64 Exrom

const int C64_POWER = 9; // Check if the c64 is powerd on

const int C64_LED = 5; // C64 Power led

const int reset_time_warm = 2000; // time in milliseconds before a warm reset is initiated
const int reset_time_cold = 4000; // time in milliseconds before a cold reset is initiated

unsigned long restore_start_time = 0;
int restore_first_press = 1;
int can_reset = 0;

int power_led_state = 1;
unsigned long power_led_delay = 0;
unsigned long matrix_delay = 0;

bool text_mode = false;

byte key_buffer[128];

void setup()
{
  for (int pos = 0; pos < 6; pos++)
  {
    pinMode(MT8808_ADDRESS_LINES[pos], OUTPUT);
    digitalWrite(MT8808_ADDRESS_LINES[pos], LOW);
  }

  pinMode(MT8808_DAT, OUTPUT);
  pinMode(MT8808_STR, OUTPUT);
  pinMode(MT8808_RESET, OUTPUT);

  pinMode(RESTORE, INPUT_PULLUP);

  pinMode(C64_RESET, INPUT);
  pinMode(C64_EXROM, INPUT);

  pinMode(C64_POWER, INPUT);

  pinMode(C64_LED, OUTPUT);
  digitalWrite(C64_LED, power_led_state == 0);

  Serial.begin(MONITOR_SPEED); // Initialize serial port

  resetMatrix(true);
}

void strobeMatrix(bool state)
{
  digitalWrite(MT8808_DAT, state);
  digitalWrite(MT8808_STR, HIGH);
  digitalWrite(MT8808_STR, LOW);
}

void resetMatrix(bool resetTextMode)
{
  digitalWrite(MT8808_RESET, HIGH);
  digitalWrite(MT8808_RESET, LOW);
  pinMode(RESTORE, INPUT_PULLUP);
  if(resetTextMode){
    DEBUG_PRINTLN("Reset matrix");
    text_mode = false;
  }
}

void pressRestore(bool state)
{
  DEBUG_PRINT("Restore: ");
  DEBUG_PRINTLN(!state);
  pinMode(RESTORE, OUTPUT);
  digitalWrite(RESTORE, !state);
}

void textMode(bool start)
{
  DEBUG_PRINT("Text mode: ");
  DEBUG_PRINTLN(start ? "ON" : "OFF");
  text_mode = start;
  if(start) {
    resetMatrix(false);
  }
}

#ifdef DEBUG
void debugMatrix(uint8_t addr)
{
  PRINTBIN(addr);
  DEBUG_PRINTLN();
}
#endif

void setSpecial(uint8_t addr, bool state)
{
#ifdef DEBUG
  DEBUG_PRINTLN();
  DEBUG_PRINT("Special address: ");
  debugMatrix(addr);
#endif
  switch (addr & 0x3F)
  {
  case 0:
    pressRestore(state);
    break;
  case 1:
    warmReset();
    break;
  case 2:
    coldReset();
    break;
  case 3:
    resetMatrix(true);
    break;
  case 4:
    textMode(state);
    break;
  }
}

void setMatrix(uint8_t addr, int state)
{
#ifdef DEBUG
  DEBUG_PRINT("Matrix address: ");
  debugMatrix(addr);
#endif

  for (int pos = 0; pos < 6; pos++)
  {
    int val = (addr >> pos) & 0x01;
    digitalWrite(MT8808_ADDRESS_LINES[pos], val);
  }
  strobeMatrix(state);
}

void warmReset()
{
  DEBUG_PRINTLN("Warm reset");
  pinMode(C64_RESET, OUTPUT);
  digitalWrite(C64_RESET, LOW);
  delay(200);
  digitalWrite(C64_RESET, HIGH);
  pinMode(C64_RESET, INPUT);
}

void coldReset()
{
  DEBUG_PRINTLN("Cold reset");
  pinMode(C64_EXROM, OUTPUT);
  digitalWrite(C64_EXROM, LOW);
  warmReset();
  delay(300);
  digitalWrite(C64_EXROM, HIGH);
  pinMode(C64_EXROM, INPUT);
}

void setPowerLed(int led_state)
{
  power_led_state = led_state;
  digitalWrite(C64_LED, power_led_state == 0);
}

void togglePowerLed(int on_state_millis, int off_state_millis)
{
  unsigned long time = millis() - power_led_delay;
  if (time > on_state_millis && power_led_state || (time > off_state_millis && power_led_state == 0))
  {
    power_led_delay = millis();
    setPowerLed((power_led_state + 1) % 2);
  }
}

int checkResetScope()
{
  int warm_reset_scope = 0;
  int cold_reset_scope = 0;
  int restore_key = !digitalRead(RESTORE);
  if (restore_key == 1)
  {
    // initiate RESTORE push timer
    if (restore_first_press == 1)
    {
      DEBUG_PRINTLN("Restore key is pressed");
      restore_first_press = 0;
      restore_start_time = millis(); // first time stamp
      delay(2);
    }
    can_reset = 0;
  }
  else if (restore_first_press == 0)
  {
    DEBUG_PRINTLN("Restore key is released");
    restore_first_press = 1; // RESTORE button has been released
    can_reset = 1;
  }

  if (restore_key || can_reset)
  {

    int restore_press_time = millis() - restore_start_time; // variable holds total time RESTORE is pressed
    warm_reset_scope = restore_press_time > reset_time_warm && restore_press_time < reset_time_cold;
    cold_reset_scope = restore_press_time > reset_time_cold && restore_press_time < 10000; // cancel reset if RESTORE is pushed > 10 seconds

    if (warm_reset_scope)
    {
      togglePowerLed(400, 100);
      if (can_reset)
      {
        DEBUG_PRINTLN("Do warm reset");
        warmReset();
      }
    }
    else if (cold_reset_scope)
    {
      togglePowerLed(200, 200);
      if (can_reset)
      {
        DEBUG_PRINTLN("Do cold reset");
        coldReset();
      }
    }
    else
    {
      setPowerLed(1);
    }
    can_reset = 0;
    return 1;
  }
  return 0;
}

void loop()
{

  if (!digitalRead(C64_POWER))
  {
    setPowerLed(0);
    return;
  }

  if (checkResetScope())
  {
    return;
  }

  while (Serial.available() > 0)
  {
    int ava = Serial.available();
    uint8_t size = Serial.read();
    int len = Serial.readBytes(key_buffer, size);
#ifdef DEBUG
    DEBUG_PRINT("Available:");
    DEBUG_PRINT(ava);
    DEBUG_PRINT(", Size:");
    DEBUG_PRINTLN(size);
    DEBUG_PRINT("read: ");
    DEBUG_PRINTLN(len);
#endif
    if (size > 0)
    {
      int delayTime = 0;
      for (int pos = 0; pos < size; pos++)
      {
        uint8_t val = key_buffer[pos];
        bool state = (val & 0x80) == 0x80;
#ifdef DEBUG
        DEBUG_PRINT("buffer size: ");
        DEBUG_PRINT(size);
        DEBUG_PRINT(", pos: ");
        DEBUG_PRINT(pos);
        DEBUG_PRINT(", value: 0b");
        PRINTBIN((uint8_t)(val&0x3F));
        DEBUG_PRINT(", state: ");
        DEBUG_PRINT(state);
        DEBUG_PRINT(", special: ");
        DEBUG_PRINT((val & 0x40) == 0x40);
        DEBUG_PRINTLN();
#endif
        if ((val & 0x40) == 0)
        {
          setMatrix(val, state);
        }
        else if ((val & 0x40) == 0x40)
        {
          setSpecial(val, state);
        }
      }
        delay(15);
      if(text_mode) {
        delay(10);
        resetMatrix(false);
      }
    }
  }

  setPowerLed(1);
}
