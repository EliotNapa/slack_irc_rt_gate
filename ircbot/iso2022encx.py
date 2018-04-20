# -*- coding: utf-8 -*-

class Iso2022jpEncX:
    
    @staticmethod
    def encode(str_str):
        bin1 = str_str.encode('CP932', errors="replace")
        bin_str1 = bin1.decode('shift_jis', errors="replace")
        target_bin = bin_str1.encode('iso2022_jp_ext', errors="replace")
        return target_bin

    @staticmethod
    def regularize(str_str):
        bin1 = str_str.encode('CP932', errors="replace")
        bin_str1 = bin1.decode('shift_jis', errors="replace")
        return bin_str1
