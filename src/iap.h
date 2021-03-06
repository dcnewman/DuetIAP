/* In-Application Programming application for RepRap Duet (Atmel SAM3X8E)
 *
 * This application is first written by RepRapFirmware to the end of the second
 * Flash bank and then started by RepRapFirmware.
 * 
 * Once this program is loaded, it performs in-application programming by
 * reading the new firmware binary from the SD card and replaces the corresponding
 * Flash content sector by sector.
 *
 * This application was written by Christian Hammacher (2016) and is
 * licensed under the terms of the GPL v2.
 */

#include "Core.h"

#if SAM3XA
#define IFLASH_ADDR			(IFLASH0_ADDR)
#define IFLASH_PAGE_SIZE	(IFLASH1_PAGE_SIZE)
#endif

const size_t baudRate = 115200;						// For USB diagnostics

const uint32_t iapFirmwareSize = 0x10000;			// 64 KiB max

#if SAM3XA
const char *fwFile = "0:/sys/RepRapFirmware.bin";	// Which file shall be used for IAP?
#endif
#if SAM4E
const char *fwFile = "0:/sys/DuetWiFiFirmware.bin";	// Which file shall be used for IAP?
#endif

const uint32_t firmwareFlashEnd = IFLASH_ADDR + IFLASH_SIZE - iapFirmwareSize;

// Read and write only 2 KiB of data at once (must be multiple of IFLASH_PAGE_SIZE).
// Unfortunately we cannot increase this value further, because f_read() would mess up data
const size_t blockReadSize = 2048;

const size_t maxRetries = 5;						// Allow 5 retries max if anything goes wrong


enum ProcessState
{
	Initializing,
	UnlockingFlash,
#if SAM4E || SAM4S
	ErasingFlash,
#endif
	WritingUpgrade,
	FillingZeros,
	LockingFlash
};


void initFilesystem();
void openBinary();
void writeBinary();
void closeAndDeleteBinary();
void Reset(bool success);

void sendUSB(uint32_t ep, const void* d, uint32_t len);

// vim: ts=4:sw=4
