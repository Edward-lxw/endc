mrdc_amount = 0
mrdc_listall = []
combination_amount = 0
combination_listall = []
com_dlcc_amount = 0
com_dlcc_listall = []
com_ulcc_amount = 0
com_ulcc_listall = []
com_lte_dlcc_amount = 0
com_lte_dlcc_listall = []
com_lte_ulcc_amount = 0
com_lte_ulcc_listall = []
com_lte_dlcc_cfg_amount = 0
com_lte_dlcc_cfg_listall = []
has_lte_feature = 0
# for NR only : SA mode
NRONLY_mrdc_amount = 0
NRONLY_mrdc_listall = []
NRONLY_combination_amount = 0
NRONLY_combination_listall = []
NRONLY_has_nronly_cap = 0
NRONLY_has_nronly_bandlist = 0

MRDC_ue_log = []
NRONLY_ue_log = []

def my_test2():
    for lines in range(0, 2):
        print(lines)

def get_uecap(in_text):
    global mrdc_amount
    global mrdc_listall
    global combination_amount
    global combination_listall
    global com_dlcc_amount
    global com_dlcc_listall
    global com_ulcc_amount
    global com_ulcc_listall
    global com_lte_dlcc_amount
    global com_lte_dlcc_listall
    global com_lte_dlcc_cfg_amount
    global com_lte_dlcc_cfg_listall
    global has_lte_feature
    global MRDC_ue_log
    global NRONLY_ue_log



    endc_result = ""
    endc_result_list = []
    # log list clear
    MRDC_ue_log = []
    NRONLY_ue_log = []
    # 先把log拆分, 防止里面有SA模式的UE 能力
    split_ue_log(in_text)

    get_NR_mrdc(NRONLY_ue_log)
    get_NR_combination(NRONLY_ue_log)
    get_nrdl_com_cc(NRONLY_ue_log)
    get_nrul_com_cc(NRONLY_ue_log)

    get_mrdc(MRDC_ue_log)
    get_combination(MRDC_ue_log)
    get_ltedl_com_cc(MRDC_ue_log)
    get_ltedl_com_cfg(MRDC_ue_log)
    # format and print the result:
    m_i = 0 # mrdc index
    c_i = 0 # combination index
    nrdl_i = 0 # dl cc combination set index
    nrul_i = 0 # ul cc combination set index
    ltedl_i = 0
    ltedl_cfg_i = 0

    if NRONLY_has_nronly_bandlist:
        for nronly_bandlist in format_nr():
            endc_result_list.append(nronly_bandlist)
        print("NR only output done")

    for m_i in range(0, mrdc_amount):
        c_i = int(mrdc_listall[m_i][-1])
        nrul_i = int(combination_listall[c_i][-1].replace("NU-", "")) - 1
        nrdl_i = int(combination_listall[c_i][-2].replace("ND-", "")) - 1

        mrdc_ele_num = len(mrdc_listall[m_i])
        print(m_i + 1, ": DC_", end="")
        endc_result = ""
        endc_result += str(m_i + 1)
        endc_result += ": DC_"

        n = 0
        for i in range(0, mrdc_ele_num - 4):
            # 这行仅仅是把LTE的band和class输出, 需要添加mimo.
            print(mrdc_listall[m_i][i], end="")
            endc_result += str(mrdc_listall[m_i][i])
            # 这里是添加mimo的逻辑
            # 判断mrdc list里的数据, 如果是单个字母, 说明是一个下行的cc, 如果是第n个 就找lte cfg中的第2n-1 个.
            if len(mrdc_listall[m_i][i]) == 1: # 说明这里是a,b,c,d..等下行的class
                n += 1
                ltedl_i_temp = combination_listall[c_i][2 * n - 2]
                ltedl_i = int(ltedl_i_temp.replace("D-", ""))
                # print(">>>>>>", ltedl_i)
                if has_lte_feature != 0:
                    ltecfg_i = int(com_lte_dlcc_listall[ltedl_i - 1][0])
                    print("[" + com_lte_dlcc_cfg_listall[ltecfg_i] + "]", end="")
                    endc_result += "["
                    endc_result += str(com_lte_dlcc_cfg_listall[ltecfg_i])
                    endc_result += "]"

        # 这行是输出NR的band以及mimo
        print("_" + mrdc_listall[m_i][-4] + mrdc_listall[m_i][-3] + "[" + com_dlcc_listall[nrdl_i][0] + "]" + mrdc_listall[m_i][-2])
        endc_result += "_"
        endc_result += str(mrdc_listall[m_i][-4])
        endc_result += str(mrdc_listall[m_i][-3])
        endc_result += "["
        endc_result += str(com_dlcc_listall[nrdl_i][0])
        endc_result += "]"
        endc_result += str(mrdc_listall[m_i][-2])
        endc_result_list.append(endc_result)

        #print(m_i, c_i, u_i, d_i, mrdc_ele_num, i)
    return endc_result_list

def format_nr():
    # for NR only UE capability
    global NRONLY_has_nronly_cap
    global NRONLY_has_nronly_bandlist
    global NRONLY_mrdc_amount
    global NRONLY_mrdc_listall
    global NRONLY_combination_amount
    global NRONLY_combination_listall
    global com_dlcc_amount
    global com_dlcc_listall
    global com_ulcc_amount
    global com_ulcc_listall

    nronly_result_list = []

    for m_i in range(0, NRONLY_mrdc_amount):
        # m_i mrdc index; c_i combination index
        c_i = int(NRONLY_mrdc_listall[m_i][-1])
        nrul_i = int(NRONLY_combination_listall[c_i][-1].replace("NU-", "")) - 1
        nrdl_i = int(NRONLY_combination_listall[c_i][-2].replace("ND-", "")) - 1

        endc_result = ""

        # 这行是输出NR的band以及mimo, 注意这里只解析了下行. 因为目前看到的NR上行都是1 mimo
        print("NR_ONLY_" + NRONLY_mrdc_listall[m_i][-4] + NRONLY_mrdc_listall[m_i][-3] + "[" + com_dlcc_listall[nrdl_i][0] + "]" + NRONLY_mrdc_listall[m_i][-2])
        endc_result += "NR_ONLY "
        endc_result += str(m_i + 1)
        endc_result += ": "
        endc_result += str(NRONLY_mrdc_listall[m_i][-4])
        endc_result += str(NRONLY_mrdc_listall[m_i][-3])
        endc_result += "["
        endc_result += str(com_dlcc_listall[nrdl_i][0])
        endc_result += "]"
        endc_result += str(NRONLY_mrdc_listall[m_i][-2])
        nronly_result_list.append(endc_result)

        #print(m_i, c_i, u_i, d_i, mrdc_ele_num, i)
    return nronly_result_list
    print("todo")

def split_ue_log(in_text):
    # 该函数把整段的ue log文本, 按照关键字 Further decoding UE Cap NR 拆分为两部分
    # 一部分为只含有NR only的能力, 一部分为e-utra - NR, 或者 e-utra - NR 和 eutra
    # 前一部分交给NR解析, 后一部分交给mrdc解析.
    global MRDC_ue_log
    global NRONLY_ue_log
    global NRONLY_has_nronly_cap
    # clean the lists
    MRDC_ue_log = []
    NRONLY_ue_log = []
    NRONLY_has_nronly_cap = 0
    in_nr_log = 0

    # because it may not have NR only log, so default is mrdc log
    in_text_temp = in_text.splitlines()
    for cur_line in in_text_temp:
        if cur_line.find("Further decoding UE Cap NR") != -1 or cur_line.find("ue-Capability ContainertList -RAT NR") != -1:
            NRONLY_has_nronly_cap = 1
            in_nr_log = 1
            NRONLY_ue_log.append(cur_line)
            continue
        if cur_line.find("Further decoding EUTRA NR") != -1:
            in_nr_log = 0
            MRDC_ue_log.append(cur_line)
            continue
        if cur_line.find("Further decoding EUTRA NR") != -1:
            in_nr_log = 0
            MRDC_ue_log.append(cur_line)
            continue
        if in_nr_log == 1:
            NRONLY_ue_log.append(cur_line)
        else:
            MRDC_ue_log.append(cur_line)

    # print(NRONLY_ue_log)
    # print("##################################")
    # print(MRDC_ue_log)
    return

def get_mrdc(in_list):
    print("enter get mrdc")
    global mrdc_amount
    global mrdc_listall

    mrdc_amount = 0
    mrdc_listall = []

    in_mrdc_list = 0
    in_curly = 0
    left_curly_brackets = 0
    right_curly_brackets = 0
    mrdc_list = []
    lte_band = -1
    nr_band = -1
    lte_cc_amount = 0
    nr_cc_amount = 0
    mrdc = []
    for curline in in_list:
        # print(curline)
        if curline.find("        bandList ") != -1:
            mrdc_amount += 1
            in_mrdc_list = 1
            mrdc_list = []
            # print(curline)
        if in_mrdc_list == 1:
            # print("get_mrdc] 0:",curline)
            #print("get_mrdc] {= ", left_curly_brackets, " }= ", right_curly_brackets, " in_curly= ", in_curly)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                in_curly = 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                right_curly_brackets += 1
                if left_curly_brackets != right_curly_brackets:
                    continue
                else: #如果左右大括号的数量相等, 说明这个mrdc已经结束了.
                    in_curly = 0
                    left_curly_brackets = 0
                    right_curly_brackets = 0
                    continue
            if in_curly != 0: #如果在括号里 说实话, python这种没大括号的代码块设计要么很垃圾,要么我没领悟到精髓
                # 这里解析eutra的cc
                print("get_mrdc] 1:", curline)
                if curline.find("eutra") != -1:
                    lte_cc_amount += 1
                    lte_band = 0
                # 这里解析eutra band
                if curline.find("bandEUTRA") != -1:
                    temp_lte = curline.replace(',', '')
                    for lte_temp_line in temp_lte.split():
                        if lte_temp_line.isdigit():
                            lte_band = lte_temp_line
                            mrdc_list.append("B"+lte_band)
                            print("B", lte_band)
                            continue

                #这里解析LTE DL band cc个数及等级
                if curline.find("BandwidthClassDL-EUTRA") != -1:
                    temp_lte = curline.replace(',', '')
                    temp_lte = temp_lte.lstrip()
                    lte_cc = temp_lte.split(' ')[1]
                    lte_cc = lte_cc.replace('\n', '')
                    mrdc_list.append(lte_cc)
                    print("get_mrdc] LTE DL class: ", lte_cc)
                    continue

                # 这里解析LTE UL band cc个数及等级
                if curline.find("BandwidthClassUL-EUTRA") != -1:
                    temp_lte = curline.replace(',', '')
                    temp_lte = temp_lte.lstrip()
                    lte_cc = temp_lte.split(' ')[1]
                    lte_cc = lte_cc.replace('\n', '')
                    mrdc_list.append("U"+lte_cc)
                    print("get_mrdc] LTE UL class: ", lte_cc)
                    continue

                # 这里解析NR的cc
                # 这里解析nr band
                if curline.find("bandNR") != -1:
                    temp_nr = curline.replace(',', '')
                    for nr_band in temp_nr.split():
                        if nr_band.isdigit():
                            mrdc_list.append("N" + nr_band)
                            print("N", nr_band)
                            continue

                # 这里解析NR band DL cc个数及等级
                if curline.find("BandwidthClassDL-NR") != -1:
                    temp_nr = curline.replace(',', '')
                    temp_nr_line = temp_nr.lstrip()
                    nr_cc = temp_nr_line.split(' ')[1]
                    nr_cc = nr_cc.replace('\n', '')
                    mrdc_list.append(nr_cc)
                    print("get_mrdc] NR DL class: ", nr_cc)
                    continue

                # 这里解析NR band UL cc个数及等级
                if curline.find("BandwidthClassUL-NR") != -1:
                    temp_nr = curline.replace(',', '')
                    temp_nr_line = temp_nr.lstrip()
                    nr_cc = temp_nr_line.split(' ')[1]
                    nr_cc = nr_cc.replace('\n', '')
                    mrdc_list.append("U" + nr_cc)
                    print("get_mrdc] NR UL class: ", nr_cc)
                    continue

            # 这里已经在mrdc的大括号外面了
            if curline.find("featureSetCombination") != -1:
                temp_line = curline.replace(',', '')
                for set_combination in temp_line.split():
                    if set_combination.isdigit():
                        #print("set_combination", set_combination)
                        print("         ")
                        mrdc_list.append(set_combination)
                mrdc_listall.append(mrdc_list)
                in_mrdc_list = 0
                continue


    print("get_mrdc] MRDC amount = ", mrdc_amount)
    print(mrdc_listall)
    print("over!")
    # finfile.close()
    return

def get_combination(in_list):
    print("enter get combination")
    global combination_amount
    global combination_listall

    combination_amount = 0
    combination_listall = []

    in_curly = 0
    left_curly_brackets = 0
    current_rat = 0
    in_combination = 0
    combination_list = []

    for curline in in_list:
        if curline.find("  featureSetCombinations") != -1:
            in_combination = 1
            continue
            #print(curline)
        if in_combination == 1:
            # print(">>> {= ", curline, left_curly_brackets)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_combination = 0
                    continue
                # 如果左大括号个数不是0, 则继续往下走, 看是不是一个combination的结束.

            # 这里解析eutra set
            if curline.find("eutra :") != -1:
                current_rat = 1 # 1:lte
                continue
            # 这里解析eutra DL set
            if curline.find("downlinkSetEUTRA") != -1:
                temp_lte = curline.replace(',', '')
                for lte_temp_line in temp_lte.split():
                    if lte_temp_line.isdigit():
                        lte_set = lte_temp_line
                        combination_list.append("D-"+lte_set)
                        #print("set D", lte_set)
                        continue

            # 这里解析eutra UL set
            if curline.find("uplinkSetEUTRA") != -1:
                temp_lte = curline.replace(',', '')
                for lte_temp_line in temp_lte.split():
                    if lte_temp_line.isdigit():
                        lte_set = lte_temp_line
                        combination_list.append("U-" + lte_set)
                        #print("set U", lte_set)
                        continue

            # 这里解析NR的set
            if curline.find("nr :") != -1:
                current_rat = 2 # 1:lte  2:nr
                continue
            # 这里解析nr的DL set
            if curline.find("downlinkSetNR") != -1:
                temp_nr = curline.replace(',', '')
                for nr_temp_line in temp_nr.split():
                    if nr_temp_line.isdigit():
                        nr_set = nr_temp_line
                        combination_list.append("ND-" + nr_set)
                        #print("set ND", nr_set)
                        continue
            # 这里解析nr UL set
            if curline.find("uplinkSetNR") != -1:
                temp_nr = curline.replace(',', '')
                for nr_temp_line in temp_nr.split():
                    if nr_temp_line.isdigit():
                        nr_set = nr_temp_line
                        combination_list.append("NU-" + nr_set)
                        #print("set NU", nr_set)
                        continue
            # print(">>>>>", curline, left_curly_brackets, current_rat)
            # 这里已经在一组combination的大括号外面了
            if left_curly_brackets == 1 and current_rat == 2:
                combination_listall.append(combination_list)
                combination_amount += 1
                combination_list = []
                continue

    print("combination amount = ", combination_amount)
    print(combination_listall)
    print("over!")
    # finfile.close()
    return

# 这个函数只提取NR only的 nr band
def get_NR_mrdc(in_list):
    print("enter get NR mrdc")
    global NRONLY_mrdc_amount
    global NRONLY_mrdc_listall
    global NRONLY_has_nronly_bandlist

    NRONLY_mrdc_amount = 0
    NRONLY_mrdc_listall = []
    NRONLY_has_nronly_bandlist = 0

    in_mrdc_list = 0
    in_curly = 0
    left_curly_brackets = 0
    right_curly_brackets = 0
    mrdc_list = []
    nr_band = -1
    nr_cc_amount = 0
    for curline in in_list:
        # print(curline)
        if curline.find("        bandList ") != -1:
            NRONLY_has_nronly_bandlist = 1
            NRONLY_mrdc_amount += 1
            in_mrdc_list = 1
            NRONLY_mrdc_list = []
            # print(curline)
        if in_mrdc_list == 1:
            # print("get_mrdc] 0:",curline)
            #print("get_mrdc] {= ", left_curly_brackets, " }= ", right_curly_brackets, " in_curly= ", in_curly)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                in_curly = 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                right_curly_brackets += 1
                if left_curly_brackets != right_curly_brackets:
                    continue
                else: #如果左右大括号的数量相等, 说明这个mrdc已经结束了.
                    in_curly = 0
                    left_curly_brackets = 0
                    right_curly_brackets = 0
                    continue
            if in_curly != 0: #如果在括号里 说实话, python这种没大括号的代码块设计要么很垃圾,要么我没领悟到精髓
                # 这里解析eutra的cc
                print("get_NR_mrdc] 1:", curline)
                # 这里解析NR的cc
                # 这里解析nr band
                if curline.find("bandNR") != -1:
                    temp_nr = curline.replace(',', '')
                    for nr_band in temp_nr.split():
                        if nr_band.isdigit():
                            NRONLY_mrdc_list.append("N" + nr_band)
                            print("N", nr_band)
                            continue

                # 这里解析NR band DL cc个数及等级
                if curline.find("BandwidthClassDL-NR") != -1:
                    temp_nr = curline.replace(',', '')
                    temp_nr_line = temp_nr.lstrip()
                    nr_cc = temp_nr_line.split(' ')[1]
                    nr_cc = nr_cc.replace('\n', '')
                    NRONLY_mrdc_list.append(nr_cc)
                    # print("get_NR_mrdc] NR DL class: ", nr_cc)
                    continue

                # 这里解析NR band UL cc个数及等级
                if curline.find("BandwidthClassUL-NR") != -1:
                    temp_nr = curline.replace(',', '')
                    temp_nr_line = temp_nr.lstrip()
                    nr_cc = temp_nr_line.split(' ')[1]
                    nr_cc = nr_cc.replace('\n', '')
                    NRONLY_mrdc_list.append("U" + nr_cc)
                    # print("get_NR_mrdc] NR UL class: ", nr_cc)
                    continue

            # 这里已经在mrdc的大括号外面了
            if curline.find("featureSetCombination") != -1:
                temp_line = curline.replace(',', '')
                for set_combination in temp_line.split():
                    if set_combination.isdigit():
                        #print("set_combination", set_combination)
                        print("         ")
                        NRONLY_mrdc_list.append(set_combination)
                NRONLY_mrdc_listall.append(NRONLY_mrdc_list)
                in_mrdc_list = 0
                continue


    print("get_NR_mrdc] MRDC amount = ", NRONLY_mrdc_amount)
    print(NRONLY_mrdc_listall)
    print("over!")
    # finfile.close()
    return # zhe

# 这个函数只提取NR only的 feature set combination
def get_NR_combination(in_list):
    print("enter get NR combination")
    global NRONLY_combination_amount
    global NRONLY_combination_listall

    NRONLY_combination_amount = 0
    NRONLY_combination_listall = []

    in_curly = 0
    left_curly_brackets = 0
    current_rat = 0
    in_combination = 0
    combination_list = []

    for curline in in_list:
        if curline.find("  featureSetCombinations") != -1:
            in_combination = 1
            continue
            # print(curline)
        if in_combination == 1:
            # print(">>> {= ", curline, left_curly_brackets)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_combination = 0
                    continue
                # 如果左大括号个数不是0, 则继续往下走, 看是不是一个combination的结束.

            # 这里解析NR的set
            if curline.find("nr :") != -1:
                current_rat = 2 # 1:lte  2:nr
                continue
            # 这里解析nr的DL set
            if curline.find("downlinkSetNR") != -1:
                temp_nr = curline.replace(',', '')
                for nr_temp_line in temp_nr.split():
                    if nr_temp_line.isdigit():
                        nr_set = nr_temp_line
                        combination_list.append("ND-" + nr_set)
                        #print("set ND", nr_set)
                        continue
            # 这里解析nr UL set
            if curline.find("uplinkSetNR") != -1:
                temp_nr = curline.replace(',', '')
                for nr_temp_line in temp_nr.split():
                    if nr_temp_line.isdigit():
                        nr_set = nr_temp_line
                        combination_list.append("NU-" + nr_set)
                        #print("set NU", nr_set)
                        continue
            # print(">>>>>", curline, left_curly_brackets, current_rat)
            # 这里已经在一组combination的大括号外面了
            if left_curly_brackets == 1 and current_rat == 2:
                NRONLY_combination_listall.append(combination_list)
                NRONLY_combination_amount += 1
                combination_list = []
                current_rat == 0
                continue

    print("NR combination amount = ", NRONLY_combination_amount)
    print(NRONLY_combination_listall)
    print("over!")
    return

# 这个函数是从NR only部分提取的可供MRDC以及NR only用的per cc下行能力
def get_nrdl_com_cc(in_list):
    print("enter get NR DL combination set")

    global com_dlcc_amount
    global com_dlcc_listall

    com_dlcc_amount = 0
    com_dlcc_listall = []

    left_curly_brackets = 0
    in_curly = 0
    com_dlcc_list = []

    for curline in in_list:
        if curline.find("    featureSetsDownlinkPerCC") != -1:
            in_curly = 1
            continue
            #print(curline)
        if in_curly == 1:
            # print(">>> {= ", curline, left_curly_brackets)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_curly = 0
                    continue
                # 如果左大括号个数不是0, 则继续往下走, 看是不是一个combination的结束.

            # 这里解析每一个set的配置, 这里只解mimo
            if curline.find("maxNumberMIMO-LayersPDSCH") != -1:
                com_dlcc_amount += 1
                temp_nr = curline.replace(',', '')
                if temp_nr.find("fourLayers") != -1:
                    nr_mimo = "4"
                if temp_nr.find("twoLayers") != -1:
                    nr_mimo = "2"

                com_dlcc_list.append(nr_mimo)
                #print("set D", lte_set)
                continue

            if left_curly_brackets == 1:
                com_dlcc_listall.append(com_dlcc_list)
                com_dlcc_list = []
                continue

    print("com_dlcc amount = ", com_dlcc_amount)
    print(com_dlcc_listall)
    print("over!")
    # finfile.close()
    return

# 这个函数是从NR only部分提取的可供MRDC以及NR only用的per cc上行能力
def get_nrul_com_cc(in_list):
    print("enter get NR UL combination set")
    global com_ulcc_amount
    global com_ulcc_listall

    com_ulcc_amount = 0
    com_ulcc_listall = []

    left_curly_brackets = 0
    in_curly = 0
    com_ulcc_list = []

    for curline in in_list:
        if curline.find("    featureSetsUplinkPerCC") != -1:
            in_curly = 1
            continue
            #print(curline)
        if in_curly == 1:
            # print(">>> {= ", curline, left_curly_brackets)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_curly = 0
                    continue
                # 如果左大括号个数不是0, 则继续往下走, 看是不是一个combination的结束.

            # 这里解析每一个set的配置, 这里只解mimo
            if curline.find("maxNumberMIMO-LayersCB-PUSCH") != -1:
                com_ulcc_amount += 1
                temp_nr = curline.replace(',', '')
                if temp_nr.find("oneLayer") != -1:
                    nr_mimo = "1"

                com_ulcc_list.append(nr_mimo)
                #print("set D", lte_set)
                continue

            if left_curly_brackets == 1:
                com_ulcc_listall.append(com_ulcc_list)
                com_ulcc_list = []
                continue

    print("com_ulcc amount = ", com_ulcc_amount)
    print(com_ulcc_listall)
    print("over!")
    # finfile.close()
    return

def get_ltedl_com_cc(in_list):
    print("enter get LTE DL combination set")

    global com_lte_dlcc_amount
    global com_lte_dlcc_listall
    global has_lte_feature

    com_lte_dlcc_amount = 0
    com_lte_dlcc_listall = []
    has_lte_feature = 0

    com_lte_dlcc_list = []
    left_curly_brackets = 0
    in_curly = 0
    in_lte_dlfeature = 0
    has_lte_feature = 0

    for curline in in_list:
        if curline.find("featureSetsDL-r15") != -1:
            in_lte_dlfeature = 1
            continue
            #print(curline)
        if in_lte_dlfeature == 1:
            # print(">>> {= ", curline, left_curly_brackets)
            if curline.find("{") != -1: #如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1: #如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_lte_dlfeature = 0
                    continue
                # 如果左大括号个数不是0, 则继续往下走, 看是不是一个combination的结束.
            # 当有3个左大括号的时候, 是lte dl cc的set:
            if left_curly_brackets == 3:
                temp_lte = curline.replace(',', '')
                temp_lte = temp_lte.lstrip()
                com_lte_dlcc_list.append(int(temp_lte))
                continue

            if left_curly_brackets == 1:
                com_lte_dlcc_listall.append(com_lte_dlcc_list)
                com_lte_dlcc_list = []
                com_lte_dlcc_amount += 1
                has_lte_feature = 1
                continue

    print("com_lte_dlcc amount = ", com_lte_dlcc_amount)
    print(com_lte_dlcc_listall)
    print("over!")
    # finfile.close()
    return

def get_ltedl_com_cfg(in_list):
    print("enter get LTE DL cfg combination set")
    global com_lte_dlcc_cfg_amount
    global com_lte_dlcc_cfg_listall
    com_lte_dlcc_cfg_amount = 0
    com_lte_dlcc_cfg_listall = []

    left_curly_brackets = 0
    in_cfg = 0

    for curline in in_list:
        # 这里解析每一个set的配置, 这里只解mimo
        if curline.find("featureSetsDL-PerCC-r15") != -1:
            in_cfg = 1
            continue
        if in_cfg == 1:
            if curline.find("{") != -1:  # 如果这行是左大括号
                left_curly_brackets += 1
                continue
            if curline.find("}") != -1:  # 如果这行是右大括号
                left_curly_brackets -= 1
                if left_curly_brackets == 0:
                    # 如果左大括号的数量为0, 说明这个combination set已经结束了.
                    in_cfg = 0
                    continue # 这里很重要, 如果这里写成return其实更好... 这样就不会再继续解析文件了, 记得return之前关闭文件.
            # print(curline)
            if curline.find("supportedMIMO-CapabilityDL-MRDC-r15 twoLayers") != -1:
                # print("enter 2 mimo")
                lte_mimo = "2"
                com_lte_dlcc_cfg_listall.append(lte_mimo)
                com_lte_dlcc_cfg_amount += 1
                continue
            if curline.find("supportedMIMO-CapabilityDL-MRDC-r15 fourLayers") != -1:
                # print("enter 4 mimo")
                lte_mimo = "4"
                com_lte_dlcc_cfg_listall.append(lte_mimo)
                com_lte_dlcc_cfg_amount += 1
                continue

    print("com_lte_dlcc_ cfg amount = ", com_lte_dlcc_cfg_amount)
    print(com_lte_dlcc_cfg_listall)
    print("over!")
    # finfile.close()
    return
