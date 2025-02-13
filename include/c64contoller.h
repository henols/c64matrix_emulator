#ifndef C64CONTROLLER_H
#define C64CONTROLLER_H 
#include <Arduino.h>

#ifdef DEBUG
void printBinanry(uint32_t *x);
void debugMatrix(uint8_t addr);
#define DEBUG_PRINTLN(x) Serial.println(x)

#define DEBUG_PRINT(x) Serial.print(x)

void printBinanry(uint32_t x)
{
  for (uint32_t t = (1UL << ((sizeof(x) * 8) - 1)); t; t >>= 1)
  {
    DEBUG_PRINT(((x & t) ? '1' : '0'));
  }
}
#define PRINTBIN(x) printBinanry(x)
void debugMatrix(uint8_t addr)
{
  PRINTBIN(addr);
  DEBUG_PRINTLN("");
}

#else
#define debugMatrix(addr)
#define PRINTBIN(x)
#define DEBUG_PRINTLN(x)
#define DEBUG_PRINT(x)
#endif

#endif // C64CONTROLLER_H