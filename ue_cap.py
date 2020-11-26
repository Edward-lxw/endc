# *-* coding=utf-8
import logging
import os
import parse_uecap

if __name__ == '__main__':
    print("enter main")
    ue_txt_path = r"D:\08_py\uecap_lte_nr.txt"
    parse_uecap.get_uecap(ue_txt_path)
    # parse_uecap.get_ltedl_com_cc(ue_txt_path)
    # parse_uecap.get_mrdc(ue_txt_path)
    # parse_uecap.get_combination(ue_txt_path)





