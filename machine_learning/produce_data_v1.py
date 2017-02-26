# -*- coding: UTF-8 -*-
import json
import sys
import jieba
import time
import att_dic
import traceback

reload(sys)
sys.setdefaultencoding("utf-8")

filename = sys.argv[1]
tmp_org_file = "/export/App/data/" + filename
print tmp_org_file
org_file = tmp_org_file.strip('\r\n')
out_put_att = org_file + '_' + 'out_put_att.txt'
print out_put_att
out_put_title = org_file + '_' + 'out_put_title.txt'
out_put_colour = org_file + '_' + 'out_put_colour.txt'
out_put_size = org_file + '_' + 'out_put_size.txt'
out_put_title_and_colour = org_file + '_' + 'out_put_title_and_colour.txt'
out_put_pic_att = org_file + '_' + 'out_put_pic_att.txt'
jieba_out_put_title = org_file + '_' + 'jieba_out_put_title.txt'
jieba_out_put_colour = org_file + '_' + 'jieba_out_put_colour.txt'
jieba_out_put_size = org_file + '_' + 'jieba_out_put_size.txt'
final_output_result = org_file + '_' + 'output_result.txt'
spec_put_data = org_file + '_' + 'spec_put_data.txt'
spec_extend_attr = org_file+ '_' + 'spec_extend_attr.txt'
spec_size_attr = org_file+ '_' + 'spec_size_attr.txt'


user_dict = "/export/App/jieba-0.38/jieba/ps_dic.txt"
pic_file = "/export/App/gl_pic.csv"


title_dict = {}
colour_dict = {}
extend_dict = {}
size_dict = {}
pic_att_dict = {}


match_dict_list = []
match_dict_list.append({"sub":att_dic.sub_sty_att_dic,"parent":att_dic.sty_att_dic})
match_dict_list.append({"sub":att_dic.sub_people_att_dic,"parent":att_dic.people_att_dic})
match_dict_list.append({"sub":att_dic.sub_colour_dic,"parent":att_dic.colour_dic})
match_dict_list.append({"sub":att_dic.sub_fansion_dic,"parent":att_dic.fansion_dic})
match_dict_list.append({"sub":att_dic.sub_main_material_dic,"parent":att_dic.main_material_dic})
match_dict_list.append({"sub":att_dic.sub_online_time_dic,"parent":att_dic.online_time_dic})
match_dict_list.append({"sub":att_dic.sub_scene_dic,"parent":att_dic.scene_dic})
match_dict_list.append({"sub":att_dic.sub_type_of_cloth_dic,"parent":att_dic.type_of_cloth_dic})
match_dict_list.append({"sub":att_dic.sub_pattern_dic,"parent":att_dic.pattern_dic})
match_dict_list.append({"sub":att_dic.sub_size_dic,"parent":att_dic.size_dic})
match_dict_list.append({"sub":att_dic.sub_type_of_colllar_dic,"parent":att_dic.type_of_colllar_dic})
match_dict_list.append({"sub":att_dic.sub_type_of_sleeve_dic,"parent":att_dic.type_of_sleeve_dic})
match_dict_list.append({"sub":att_dic.sub_ver_sty_att_dic,"parent":att_dic.ver_sty_att_dic})


def read_origin_cut():
    file = open(org_file)
    file_out_title = open(out_put_title, 'w')
    file_out_colour = open(out_put_colour, 'w')
    file_out_att = open(out_put_att, 'w')
    file_out_size = open(out_put_size, 'w')
    file_spec_data = open(spec_put_data, 'w')
    text = []

    while 1:
        line = file.readline()
        text.append(line)
        if not line:
            break
    line_num = len(text)
    for i in range(1, line_num - 1, 1):
        out_title_str_tmp = []
        out_colour_str_tmp = []
        out_size_str_tmp = []
        out_att_dict = {}
        temp = text[i].split('^')
        if len(temp) != 6:
            file_spec_data.write(text[i])
            continue

        out_title_str_tmp.append(temp[0])
        out_title_str_tmp.append(temp[1])
        out_colour_str_tmp.append(temp[0])
        out_colour_str_tmp.append(temp[3])

        temp[5] = temp[5].strip('\n')
        out_att_dict[temp[0]] = temp[5]
        # out_size_dict[temp[0]] = temp[4]
        out_size_str_tmp.append(temp[0])
        out_size_str_tmp.append(temp[4])
        out_title_str = json.dumps(out_title_str_tmp, encoding='utf-8', ensure_ascii=False) + '\n'
        out_colour_str = json.dumps(out_colour_str_tmp, encoding='utf-8', ensure_ascii=False) + '\n'
        out_att_str = json.dumps(out_att_dict, encoding='gbk', ensure_ascii=False) + '\n'
        out_att_str_p = out_att_str.decode("string_escape")
        out_size_str = json.dumps(out_size_str_tmp, encoding='utf-8', ensure_ascii=False) + '\n'

        # out_size_str = json.dumps(out_size_dict, encoding='utf-8', ensure_ascii=False) + '\n'

        file_out_title.write(out_title_str)
        file_out_colour.write(out_colour_str)
        file_out_att.write(out_att_str_p)
        file_out_size.write(out_size_str)
    file_out_title.close()
    file_out_colour.close()
    file_out_att.close()
    file_out_size.close()


def read_pic_att():
    file = open(pic_file)
    pic_org_file = open(out_put_pic_att, 'w')
    text = []
    while True:
        line = file.readline()
        text.append(line)
        if not line:
            break
    for i in range(1, (len(text) - 1)):
        out_pic_dict = {}
        temp = text[i].split('^')
        temp[1] = temp[1].strip('\n')
        if temp[1] == "notshirt":
            continue
        else:
            out_pic_dict[temp[0]] = temp[1]
        if temp[1] == "long":
            out_pic_dict[temp[0]] = "长袖"
        else:
            out_pic_dict[temp[0]] = "短袖"

        out_pic_str = json.dumps(out_pic_dict, encoding='utf-8', ensure_ascii=False) + '\n'
        pic_org_file.write(out_pic_str)
    pic_org_file.close()


def pr_jieba_result(input_file_path, output_file):
    # jieba.enable_parallel()
    jieba.load_userdict(user_dict)
    content = open(input_file_path, "rb").read()
    t1 = time.time()

    words = ' '.join(jieba.cut(content))

    t2 = time.time()
    tm_cost = t2 - t1

    log_f = open(output_file, "wb")
    log_f.write(words.encode('utf-8'))

    print 'tm_cost:', tm_cost
    # print('speed %s bytes/second' % (len(content) / tm_cost))


def jieba_result_format(input_file, dict):
    with open(input_file, 'r') as f_title:
        for line in f_title.readlines():
            # print line
            # print type(line)
            line = line.replace("[", "").replace("]", "")
            # print line
            lines = line.split("\" ,")
            if len(lines) != 2:
                print "spec...", line
                continue

            sku = lines[0].replace("\"", "").replace(" ", "")
            # print 'sku:', sku
            title = lines[1].replace("\"", "").split(" ")
            attr_list = []
            for title_attr in title:
                if title_attr != '' and title_attr != '\n':
                    attr_list.append(title_attr.strip())
                    # print 'title attr:', title_attr

            title_to_dict(sku, attr_list, dict)
            # print "=============================="

def jieba_result_format(input_file, dict):
    with open(input_file, 'r') as f_title:
        for line in f_title.readlines():
            # print line
            # print type(line)
            line = line.replace("[", "").replace("]", "")
            # print line
            lines = line.split("\" ,")
            if len(lines) != 2:
                print "spec...", line
                continue

            sku = lines[0].replace("\"", "").replace(" ", "")
            # print 'sku:', sku
            title = lines[1].replace("\"", "").split(" ")
            attr_list = []
            for title_attr in title:
                if title_attr != '' and title_attr != '\n':
                    attr_list.append(title_attr.strip())
                    # print 'title attr:', title_attr

            title_to_dict(sku, attr_list, dict)
            # print "=============================="


def title_to_dict(sku, attr_list, dict):
    record_dict = {}
    for attr in attr_list:
        for item in match_dict_list:
            # category = None
            # attr_value = None
            attr_value = item.get("sub").get(attr,attr)
            if attr_value:
                category = item.get("parent").get(attr_value)
                if category:
                    attr_list = record_dict.get(category, [])
                    # #去除类别中相同的值
                    if attr_value not in attr_list:
                        attr_list.append(attr_value)
                    record_dict[category] = attr_list

            # else:
            #     continue
        # attr = sub_dict_merged.get(attr, attr)
        # category = dict_merged.get(attr, None)
        # if category:
        #     attr_list = record_dict.get(category, [])
        #     ##去除类别中相同的值
        #     if attr_value not in attr_list:
        #         attr_list.append(attr_value)
        #     record_dict[category] = attr_list

    dict[sku] = record_dict


def oper_title():
    # 标题分词
    pr_jieba_result(out_put_title, jieba_out_put_title)

    # 标题分词结果格式化以及匹￿
    jieba_result_format(jieba_out_put_title, title_dict)


def oper_colour():
    # 颜色分词
    pr_jieba_result(out_put_colour, jieba_out_put_colour)

    # 颜色分词结果格式化以及匹￿
    jieba_result_format(jieba_out_put_colour, colour_dict)


def oper_size():

    # 颜色分词
    pr_jieba_result(out_put_size, jieba_out_put_size)

    # 颜色分词结果格式化以及匹￿
    jieba_result_format(jieba_out_put_size, size_dict)
    print "size jieba finish..."
    # spec_size_attr_file = open(spec_size_attr, 'w')
    #
    # with open(out_put_size, 'rb') as f_size:
    #     for line in f_size.readlines():
    #         line = line.strip("\r\n")
    #         line = line.replace(" ", "")
    #         record = line.split("\":")
    #         if len(record) != 2:
    #             spec_size_attr_file.write(line + "\n")
    #             continue
    #         sku = record[0].replace("{\"", "").replace(" ", "")
    #         size = record[1].replace("\"}", "").replace("\"", "").replace(" ", "")
    #         item_dict = {}
    #         size_tmp = json.dumps(size, encoding='utf-8', ensure_ascii=False)
    #         size_tmp = size_tmp.replace("\"", "")
    #         size_list = []
    #         size_list.append(size_tmp)
    #         item_dict['尺码'] = size_list
    #         size_dict[sku] = item_dict
    #
    # print 'finish size operation...'


def oper_extend():
    spec_extend_attr_file = open(spec_extend_attr, 'w')

    with open(out_put_att, 'rb') as f_title:
        for line in f_title.readlines():
            # line = line.replace("\"[", "[").replace("]\"", "]")
            line = line.strip("\r\n")
            record = line.split("\":")
            if len(record) != 2:
                spec_extend_attr_file.write(line + "\n")
                continue
            sku = record[0].replace("{\"", "").replace(" ", "")

            items = None

            if "[]" in record[1]:
                extend_dict[sku] = {}
                continue

            if "\t" in record[1]:
                items = record[1].split("\t")
            elif "," in record[1]:
                items = record[1].split(",")
            else:
                items = record[1].split("\"")

            item_dict = {}
            try:
                for item in items:
                    if not item:
                        print 'item is None,continue...'
                        continue
                    item = item.replace(" ", "").replace("[", "").replace("]", "").replace("\t", "").replace("\"",
                                                                                                             "").replace(
                        "}", "")
                    itemArray = item.split(":")
                    if len(itemArray) != 2:
                        continue
                    if itemArray[0] =="尺码":
                        size_list = item_dict.get(itemArray[0],[])
                        if itemArray[1] not in size_list:
                            size_list.append(itemArray[1])
                        item_dict[itemArray[0]] = size_list
                        continue
                    item_dict[itemArray[0]] = itemArray[1]
            except Exception:
                msg = "failed due to %s" % traceback.format_exc()
                print "error ...", msg, "sku:", sku

            extend_dict[sku] = item_dict

    print 'finish extend attr operation...'


def pic_att_to_dic(input_file, dict):
    with open(input_file, 'r') as f_title:
        for line in f_title.readlines():
            line = line.strip("\n")
            line = line.replace("{\"", "").replace("\"}", "").replace("\"", "").replace(" ", "")
            lines = line.split(':')
            sku = lines[0]
            lines[1] = lines[1].strip('\n')
            att_tmp_dic = {}
            tmp = json.dumps(lines[1], encoding='utf-8', ensure_ascii=False)
            att_tmp_dic["袖长"] = tmp
            dict[sku] = att_tmp_dic

#
# def oper_size():
#     spec_size_attr_file = open(spec_size_attr, 'w')
#
#     with open(out_put_size, 'rb') as f_size:
#         for line in f_size.readlines():
#             line = line.strip("\r\n")
#             line = line.replace(" ", "")
#             record = line.split("\":")
#             if len(record) != 2:
#                 spec_size_attr_file.write(line + "\n")
#                 continue
#             sku = record[0].replace("{\"", "").replace(" ", "")
#             size = record[1].replace("\"}", "").replace("\"", "").replace(" ", "")
#             item_dict = {}
#             size_tmp = json.dumps(size, encoding='utf-8', ensure_ascii=False)
#             size_tmp = size_tmp.replace("\"", "")
#             size_list = []
#             size_list.append(size_tmp)
#             item_dict['尺码'] = size_list
#             size_dict[sku] = item_dict
#
#     print 'finish size operation...'


def merge_result():
    # for k, v in     pic_att_dict.items():
    #     print k,v


    for k, v in title_dict.items():
        v.update(colour_dict.get(k, {}))
        v.update(size_dict.get(k, {}))

    for k, v in title_dict.items():
        # type(sleeve_type)= []
        title_sleeve_list = v.get("袖型")
        pic_sleeve = pic_att_dict.get(k)
        if pic_sleeve =="长袖" and "七分袖" in title_sleeve_list:
            v["袖型"] = "七分袖"
            continue
        if pic_sleeve =="长袖"  and "七分袖" not in title_sleeve_list:
            v["袖型"] = "长袖"
            continue
        if pic_sleeve =="短袖" :
            v["袖型"] = "短袖"
            continue


    with open(out_put_title_and_colour, 'w') as f:
        for k, v in title_dict.items():
            record = k + "^" + json.dumps(v, encoding='utf-8', ensure_ascii=False) + "\n"
            f.write(record)

    sku_list = []
    for sku, attrs in title_dict.items():
        for category, value in attrs.items():
            if extend_dict.get(sku) is not None:
                #特殊处理
                #风格
                if category == "风格":
                    if not extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + "" + "^" + "，".join(value[0:2])
                        sku_list.append(sku_info)
                        continue
                    if extend_dict.get(sku).get(category) =="商务休闲" or extend_dict.get(sku).get(category) =="商务正装":
                        if len(value) == 1 and value[0] == "商务":
                            continue

                    sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category) + "^" + "，".join(value[0:2])
                    sku_list.append(sku_info)
                    continue
                #袖型
                if category == "袖型":
                    sleeves = ["长袖","九分袖","七分袖"]
                    if not extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + "" + "^" + value[0]
                        sku_list.append(sku_info)
                        continue
                    if value[0] == "七分袖" and "七分袖" not in extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category) + "^" + value[0]
                        sku_list.append(sku_info)
                        continue
                    if value[0] == "长袖" and extend_dict.get(sku).get(category) not in sleeves:
                        sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category) + "^" + value[0]
                        sku_list.append(sku_info)
                        continue
                    if value[0] == "短袖" and "短袖" != extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category) + "^" + value[0]
                        sku_list.append(sku_info)
                        continue
                #尺码
                if category =="尺码":
                    size_value = size_dict.get(sku).get(category, title_dict.get(sku).get(category))
                    if not extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + "" + "^" + size_value[0]
                        sku_list.append(sku_info)
                        continue
                    if len(extend_dict.get(sku).get(category)) ==1 and extend_dict.get(sku).get(category)[0] != size_value[0]:
                        sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category)[0] + "^" + size_value[0]
                        sku_list.append(sku_info)
                        continue
                    if len(extend_dict.get(sku).get(category)) >1:
                        sku_info = sku + "^" + category + "^" + "，".join(extend_dict.get(sku).get(category)) + "^" + size_value[0]
                        sku_list.append(sku_info)
                        continue
                else:
                    sku_info = None
                    if not extend_dict.get(sku).get(category):
                        sku_info = sku + "^" + category + "^" + "" + "^" + value[0]
                    elif extend_dict.get(sku).get(category) not in value:
                        try:
                            sku_info = sku + "^" + category + "^" + extend_dict.get(sku).get(category) + "^" + value[0]
                        except Exception:
                            msg = "failed due to %s" % traceback.format_exc()
                            print "error ...", msg, "sku:", sku,"   ,category:",category

                    if sku_info:
                        sku_list.append(sku_info)

    loop_count = len(sku_list) / 1000 + 1
    print "length of sku_list", len(sku_list)
    file_output_result = open(final_output_result, 'w')

    file_output_result.write("sku_id^attr_name^old_value^new_value\n")
    for i in range(0, loop_count):
        # try:
        content = "\n".join(sku_list[1000 * i:1000 * (i + 1)]) + '\n'
        file_output_result.write(content)
        print "$$$$$$$$$$$$$$$$$$$$", i, "loop_count", loop_count
        # except Exception:

    #        msg = "failed due to %s" % traceback.format_exc()
    #        print "error ...",msg

    file_output_result.close()


def main():
    # 原始数据拆分
    t_start = time.time()
    read_origin_cut()
    read_pic_att()
    pic_att_to_dic(out_put_pic_att, pic_att_dict)
    t_stop = time.time()
    print t_stop - t_start

    oper_title()
    oper_colour()

    oper_extend()
    oper_size()
    merge_result()


if __name__ == "__main__":
    main()