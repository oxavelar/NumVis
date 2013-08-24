#!/usr/bin/env python
"""
    Author: Omar Avelar
    
    DESCRIPTION
    ===========
    Simple class extension of number to add hex and binary chunk representations
    that allow for faster debugging and data analysis, tested in Python 2.6.
    
    EXAMPLE
    =======
    >>> from numvis import NumVis
    >>> # Can be regular integer, long, hex number or binary number
    >>> number = NumVis(0xf5fa)
    >>> number
    0xf5faL
    
    >>> number.hex()
     (9B per line):
     00 00000000 00000000                                              [0575:0504]
     00 00000000 00000000                                              [0503:0432]
     00 00000000 00000000                                              [0431:0360]
     00 00000000 00000000                                              [0359:0288]
     00 00000000 00000000                                              [0287:0216]
     00 00000000 00000000                                              [0215:0144]
     00 00000000 00000000                                              [0143:0072]
     00 00000000 0000F5FA                                              [0071:0000]
    
    
    >>> number.bin()
     (16b per line)
     0000 0000 0000 0000                                               [0127:0112]
     0000 0000 0000 0000                                               [0111:0096]
     0000 0000 0000 0000                                               [0095:0080]
     0000 0000 0000 0000                                               [0079:0064]
     0000 0000 0000 0000                                               [0063:0048]
     0000 0000 0000 0000                                               [0047:0032]
     0000 0000 0000 0000                                               [0031:0016]
     1111 0101 1111 1010                                               [0015:0000]
    
    
    Both "bin()" and "hex()" methods provide more flexible ways of organizing the
    data to print, for example:
    
    >>> number.hex(line_width=128, full_size = 256, hgroup=2, vgroup=2)
     (16B per line):
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0255:0128]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 F5 FA                   [0127:0000]
    
    
    >>> number.hex(line_width=128, full_size = 1024, hgroup=2, vgroup=4)
     (16B per line):
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [1023:0896]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0895:0768]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0767:0640]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0639:0512]

     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0511:0384]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0383:0256]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00                   [0255:0128]
     00 00 00 00 00 00 00 00 00 00 00 00 00 00 F5 FA                   [0127:0000]
"""
import __builtin__

class NumVis(long):
    
    def hex(self, line_width=72, full_size=576, hgroup=8, vgroup=8):
        """
        Organizes numeric data hex chunks for data visualization.
        
        Notes: "line_width" and "full_size" are in bit sizes.
               hgroup and vgroup are symbol sizes.
        """
        # If data is bigger than size, override manually to fit.
        while (self.numerator >> full_size): full_size = full_size + line_width
        
        if line_width % full_size != line_width:
            raise(ValueError, 'The choosen "line_width" parameter is not evenly divisible by the specified size')
        
        print(' (%dB per line):' % (line_width / 8))
        str_cl_hex = eval("'%%0%dX' %% self.numerator" % (full_size / 4))
        # Separates size in chunks of width bits.
        tmp = self._reversesplit(str_cl_hex, line_width / 4)
        
        c = full_size / line_width
        for chunk in tmp:
            # Splits according to horizontal group, left to right.
            chunk = ' '.join(self._reversesplit(chunk, hgroup))
            print(' %-65s [%04d:%04d]' % (chunk, c * line_width - 1, c * line_width - line_width))
            if ((c-1) % vgroup == 0): print('')
            c -= 1
            
    def bin(self, line_width=16, full_size=128, hgroup=4, vgroup=8):
        """
        Organizes numeric data in chunks of binary for data visualization.
        
        Notes: "line_width" and "full_size" are in bit sizes.
               "hgroup" and "vgroup" are symbol sizes.
               Default "hgroup" is 4 to see them as nibbles.
        """
        # If data is bigger than size, override manually to fit.
        while (self.numerator >> full_size): full_size = full_size + line_width
        
        if line_width % full_size != line_width:
            raise(ValueError, 'The choosen "line_width" parameter is not evenly divisible by the specified size')
        
        str_cl_bin = self._rawbin(self.numerator, padding=full_size)
        # Separates size in chunks of width bits.
        print(' (%db per line)' % line_width)
        tmp = self._reversesplit(str_cl_bin, line_width)

        c = full_size / line_width
        for chunk in tmp:
            # Splits according to horizontal group, left to right.
            chunk = ' '.join(self._reversesplit(chunk, hgroup))
            print(' %-65s [%04d:%04d]' % (chunk, c * line_width - 1, c * line_width - line_width))
            if ((c-1) % vgroup == 0): print('')
            c -= 1    
        
    def _reversesplit(self, binstring, size):
        """
        Will split the binary string in chunks of desire size. Starts
        from the LSB as desired.
        """
        results = list()
        
        l = list(binstring)
        l.reverse()
        for i in xrange(0, len(l), size):
            tmp = l[i:i+size]
            tmp.reverse()
            results.append(tmp)
        
        results.reverse()
        
        # Concatenates and places a separator.
        tmp = list()
        for e in results:
            tmp.append(''.join( [str(x) for x in e]))
        return tmp
    
    def _rawbin(self, number, padding=0):
        """
        Returns the string representation in binary of the number with left padding.
        """
        tmp = bin(number)[2:]
        # Padding happens here...
        if padding < len(tmp):
            return tmp
        else:
            num_zeros = padding - len(tmp)
            return (num_zeros * '0') + tmp

