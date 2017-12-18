# DS1302 Real Time Clock
# Author: David Boyd
# The MIT License (MIT)
#
# Copyright (c) 2016 Philip R. Moyer and Radomir Dopieralski for Adafruit Industries.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
DS1302 Real Time Clock module
=================================================

CircuitPython library to support DS1302 Real Time Clock (RTC).

This library supports the use of the DS1302-based RTC in CircuitPython.

Beware that most CircuitPython compatible hardware are 3.3v logic level! Make
sure that the input pin is 5v tolerant.

* Author: David Boyd

"""
import time
import array
import digitalio

# Register names.
DS1302_ENABLE            = const(0x8E)
DS1302_TRICKLE           = const(0x90)
DS1302_CLOCK_BURST_WRITE = const(0xBE)
DS1302_CLOCK_BURST_READ  = const(0xBF)
DS1302_RAM_BURST_WRITE   = const(0xFE)
DS1302_RAM_BURST_READ    = const(0xFF)

class DS1302RTC:
    # 5us
    CLK_DELAY = .005

    def __init__(self, ce_pin, data_pin, sclk_pin):
        """
        Driver for a DS 1302 RTC
        """
        self._IO_PIN = digitalio.DigitalInOut(data_pin)
        
        self._SCLK_PIN = digitalio.DigitalInOut(sclk_pin)
        self._SCLK_PIN.direction = digitalio.Direction.OUTPUT

        self._CE_PIN = digitalio.DigitalInOut(ce_pin)
        self._CE_PIN.direction = digitalio.Direction.OUTPUT

        # turn off WP (write protect)
        self._start_tx()
        self._write_byte(DS1302_ENABLE)
        self._write_byte(0x00)
        self._end_tx()

        # charge mode is disabled
        self._start_tx()
        self._write_byte(DS1302_TRICKLE)
        self._write_byte(0x00)
        self._end_tx()

    def _to_time_struct(self, Year, Month, Day, Hour, Minute, Second, Wday, Yday = -1, isDst = -1):
        """
        create a struct_time obejct
        time.struct_time((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))
        """
        return time.struct_time((Year, Month, Day, Hour, Minute, Second, Wday, Yday, isDst))

    # def _from_time_struct(self, ts):
    #     """
    #         TODO:
    #         class time.struct_time((tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst))
    #     """
    #     pass 

    def _start_tx(self):
        """
        Start of transaction.
        """
        self._SCLK_PIN.value = False
        self._CE_PIN.value = True

        time.sleep(.004)

    def _end_tx(self):
        """
        End of transaction.
        """
        self._IO_PIN.switch_to_input()
        self._SCLK_PIN.value = False
        self._CE_PIN.value = False

        time.sleep(.004)

    def _write_byte(self, byte):
        """
        Write byte to the chip.
        """
        # data pin is now output
        self._IO_PIN.switch_to_output()

        # clock the byte to chip
        for _ in range(8):
            self._SCLK_PIN.value = False
            time.sleep(self.CLK_DELAY)

            # chip read data on clk rising edge
            self._IO_PIN.value = (byte & 0x01)
            byte >>= 1
            self._SCLK_PIN.value = True

            time.sleep(self.CLK_DELAY)

    def _read_byte(self):
        """
        Read byte from the chip.
        """
        # data pin is now input (pull-down resistor embedded in chip)
        self._IO_PIN.switch_to_input()
        # clock the byte from chip
        byte = 0
        for i in range(8):
            # make a high pulse on CLK pin
            self._SCLK_PIN.value = True
            
            time.sleep(self.CLK_DELAY)
            self._SCLK_PIN.value = False
            
            time.sleep(self.CLK_DELAY)
            # chip out data on clk falling edge: store current bit into byte
            bit = 1 if self._IO_PIN.value == True else 0 
            # Debug print 
            # print(self._IO_PIN.value, bit)
            byte |= ((2 ** i) * bit)


        return byte  
           
    def read_ram(self):
        """
        Read RAM as bytes
        """
        # start of message
        self._start_tx()
        # read ram burst
        self._write_byte(DS1302_RAM_BURST_READ)

        # read data bytes
        byte_a = bytearray()
        for _ in range(31):
            byte_a.append(self._read_byte())

        # end of message
        self._end_tx()

        return byte_a

    def write_ram(self, byte_a):
        """
        Write RAM with bytes
        """
        # start message
        self._start_tx()
        # write ram burst
        self._write_byte(DS1302_RAM_BURST_WRITE)

        # write data bytes
        for i in range(min(len(byte_a), 31)):
            self._write_byte(ord(byte_a[i:i + 1]))

        # end of message
        self._end_tx()

    def read_dt_bytes(self):
        """
        Read current date and time from RTC chip.
        """
        # start message
        self._start_tx()
        # read clock burst
        self._write_byte(DS1302_CLOCK_BURST_READ)

        byte_l = []
        for _ in range(7):
            byte_l.append(self._read_byte())
        
        # end of message
        self._end_tx()

        return byte_l

    def read_datetime(self):
        """
        Read current date and time from RTC chip.
        """
        # start message
        self._start_tx()
        # read clock burst
        self._write_byte(DS1302_CLOCK_BURST_READ)

        byte_l = []
        for _ in range(7):
            byte_l.append(self._read_byte())
        
        # end of message
        self._end_tx()
        
        # decode bytes
        second = ((byte_l[0] & 0x70) >> 4) * 10 + (byte_l[0] & 0x0f)
        minute = ((byte_l[1] & 0x70) >> 4) * 10 + (byte_l[1] & 0x0f)
        hour = ((byte_l[2] & 0x30) >> 4) * 10 + (byte_l[2] & 0x0f)
        day = ((byte_l[3] & 0x30) >> 4) * 10 + (byte_l[3] & 0x0f)
        month = ((byte_l[4] & 0x10) >> 4) * 10 + (byte_l[4] & 0x0f)
        year = ((byte_l[6] & 0xf0) >> 4) * 10 + (byte_l[6] & 0x0f) + 2000
        wday = (byte_l[5] & 0x70)

        # return datetime value
        return self._to_time_struct(year, month, day, hour, minute, second, wday)

    def write_datetime(self, dt):
        """
        Write a python datetime to RTC chip.
        """
        # format message
        byte_l = [0] * 9
        byte_l[0] = (dt.tm_sec // 10) << 4 | dt.tm_sec % 10
        byte_l[1] = (dt.tm_min // 10) << 4 | dt.tm_min % 10
        byte_l[2] = (dt.tm_hour // 10) << 4 | dt.tm_hour % 10
        byte_l[3] = (dt.tm_mday // 10) << 4 | dt.tm_mday % 10
        byte_l[4] = (dt.tm_mon // 10) << 4 | dt.tm_mon % 10
        # byte_l[5] = (dt.tm_wday // 10) << 4 | dt.tm_wday % 10
        byte_l[6] = ((dt.tm_year-2000) // 10) << 4 | (dt.tm_year-2000) % 10

        # start message
        self._start_tx()

        # write clock burst
        self._write_byte(DS1302_CLOCK_BURST_WRITE)

        # write all data
        for byte in byte_l:
            self._write_byte(byte)

        # end of message
        self._end_tx()
