//
//  adc.h
//  CrumbTest
//
//  Created by Juan Pablo Civile on 06/05/14.
//
//

#ifndef common_adc_h
#define common_adc_h

#include <stdint.h>

void adc_init(void);

void adc_mode(uint8_t mux);

uint16_t adc_read(void);

#endif
