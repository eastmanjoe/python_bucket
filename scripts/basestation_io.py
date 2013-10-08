#!/usr/bin/env Python

import mmap
import os

# This is for the TS-8100:
#   BAT10_ADDR = 0x110
#   DIO_IN_REG = 0xC
#   DIO_OUT_REG = 0x4
#   DIO_DIR_REG = 0x8
#   BOARD_ID = 0x0
#   syscon offset = 0xb0010000);
#   muxbuss offset = 0xb0017000

# static volatile uint16_t *mwin;
# static volatile uint16_t *syscon;


# StatusFlags = {"SW1":1 << 7}
# typedef enum
# {
#     "SW1": 1 << 7,
#     "BELOW33V": = 1 << 6,
#     "NOVDC5 = 1 << 5,
#     "BACKUPDISABLED = 1 << 4,
#     "BAT1CHARGING = 1 << 3,
#     "BAT1CHARGED = 1 << 2,
#     "BAT2CHARGING = 1 << 1,
#     "BAT2CHARGED = 1 << 0
# } StatusFlags;

# typedef enum
# {
#     REDLED = 1 << 14,
#     GREENLED = 1 << 15,
#     DIO_1 = 1 << 0,
#     DIO_3 = 1 << 1
# } IOBits;

# typedef enum
# {
#     RESERVED = 1 << 7,
#     BAT2NOFASTCHARGE = 1 << 6,
#     BAT1NOFASTCHARGE = 1 << 5,
#     BAT2CHARGEEN = 1 << 4,
#     BAT1CHARGEEN = 1 << 3,
#     BAT2TIMERDISABLE = 1 << 2,
#     BAT1TIMERDISABLE = 1 << 1,
#     SOFTDISABLE = 1 << 0
# } ConfigurationFlags;

def mwinen():
    filename = '/dev/mem'
    mem = os.open(filename, os.O_RDWR| os.O_SYNC)
    size = os.path.getsize(filename)
    syscon = mmap.mmap(mem.fileno(), size, mmap.MAP_SHARED, mmap.PROT_READ| mmap.PROT_WRITE, mem, int('0xb0010000', 0)
    # mwin = mmap.mmap(0, getpagesize(), PROT_READ|PROT_WRITE, MAP_SHARED, mem, 0xb0017000);

    # assert(syscon != NULL);
    # assert(mwin != NULL);

    # #Set up muxbus timing register.
    # syscon[0x12/2] = 0x321;

    # #Turn Red LED OFF & GREEN LED ON
    # syscon[0x10/2] &= ~(REDLED);
    # syscon[0x10/2] |= (GREENLED);

    # close(mem);


# def mwinpeek16(uint32_t addr):
#     mwin[0x0] = addr >> 11; // This register contains the upper bits of address
#     // Sets the remaining address bits, and requests a 16 bit bus cycle
#     mwin[0x2/2] = (addr & 0x7ff) | 0x8000;

#     return mwin[0x4/2];

# def mwinpoke16(uint32_t addr, uint16_t value)
#     mwin[0x0] = addr >> 11;
#     mwin[0x2/2] = (addr & 0x7ff) | 0x8000;

#     mwin[0x4/2] = value;

# def mwinpeek8(uint32_t addr):
#     // 8-bit addr starts 64k into the memory window
#     addr = 0x10000 | addr;

#     mwin[0x0] = addr >> 11;
#     // Similar to the 16 bit transactions, but requests 8 bit bus cycles
#     mwin[0x2/2] = (addr & 0x7ff) | 0xc000;

#     return mwin[0x4/2];

# def mwinpoke8(addr, value):
#     #8-bit addr starts 64k into the memory window
#     addr = 0x10000 | addr;

#     mwin[0x0] = addr >> 11;
#     mwin[0x2/2] = (addr & 0x7ff) | 0xc000;

#     mwin[0x4/2] = value;

# def get_status():
#     pass
# int main(int argc, char **argv)
# {
#     mwinen();

#     uint8_t bat10_status = mwinpeek8(BAT10_ADDR);
#     uint16_t dio_dir = mwinpeek16(DIO_DIR_REG);
#     uint8_t dio_in_status = mwinpeek8(DIO_IN_REG);

#     if(~(dio_dir & DIO_3))
#     {
#         // Set MUXBUS configuration
#         syscon[0x12/2] = 0x181;

#         // Set DIO 3 as output
#         mwinpoke16(DIO_DIR_REG, 0x2);
#     }

#     // Enable UPS
#     uint8_t get_dio_out = mwinpeek8(DIO_OUT_REG);
#     get_dio_out |= DIO_3;
#     mwinpoke8(DIO_OUT_REG, get_dio_out);

#     // Begin fast charging both batteries
#     mwinpoke8(BAT10_ADDR, BAT1CHARGEEN | BAT2CHARGEEN);

#     printf("======= INITIAL Status =======\n");
#     printf("Board ID: %x\n", mwinpeek16(BOARD_ID));

#     if (dio_in_status & DIO_1)
#         printf("System Mode: Run\n");
#     else
#         printf("System Mode: Test\n");

#     print_settings(bat10_status);


#     printf("==============================\n");


#     while(1)
#     {

#         uint8_t get_ups_status = mwinpeek8(BAT10_ADDR);

#         uint8_t get_dio_in_status = mwinpeek8(DIO_IN_REG);
#         get_dio_out = mwinpeek8(DIO_OUT_REG);
#         uint16_t sysconstate = syscon[0x10/2];

#         if((get_ups_status != bat10_status) | (get_dio_in_status != dio_in_status))
#         {
#             bat10_status = get_ups_status;
#             dio_in_status = get_dio_in_status;
#             printf("======= UPS Status ========\n");
#             print_settings(bat10_status);

#             if (get_dio_in_status & DIO_1)
#                 printf("System Mode: Run\n");
#             else
#                 printf("System Mode: Test\n");

#             printf("==============================\n");


#         }

#         // If input power is lost and UPS enabled
#         if ((((get_ups_status & NOVDC5) >> 5) == 0) & (get_ups_status & BACKUPDISABLED))
#         {
#             // If battery voltage below 3.3VDC issue shutdown command
#             if (((get_ups_status & BELOW33V) >> 6) == 0)
#             {
#                 printf("Run Shutdown\n");
#                 // system("shutdown -h 1");
#             }
#             else
#             {

#                 printf("Test Shutdown\n");
#                 // system("shutdown -h 1");

#                 // usleep(59000000);

#                 // //disable UPS
#                 // get_dio_out &= ~DIO_3;
#                 // mwinpoke8(DIO_OUT_REG, get_dio_out);
#             }
#         }

#         // Toggle Red LED
#         if (sysconstate & REDLED)
#             syscon[0x10/2] &= ~REDLED;
#         else
#             syscon[0x10/2] |= REDLED;

#         usleep(500000);
#     }

#     return 0;
# }

if __name__ == "__main__":
    mwinen ()
