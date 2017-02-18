# -*- coding:utf-8
import json
import sys
import jieba
import time
reload(sys)
sys.setdefaultencoding( "utf-8" )

org_file = "C:/Users/eric/Desktop/test.csv"
out_put_title = "C:/Users/eric/Desktop/out_put_title.txt"
out_put_colour = "C:/Users/eric/Desktop/out_put_colour.txt"
out_put_att = "C:/Users/eric/Desktop/out_put_att.txt"


def read_origin_cut():
    file = open(org_file)
    file_out_title = open(out_put_title, 'w')
    file_out_colour = open(out_put_colour, 'w')
    file_out_att = open(out_put_att, 'w')
    text = []
    t_start = time.time()
    while 1:
        line = file.readline()
        text.append(line)
        if not line:
            break
    line_num = len(text)
    for i in range(1, line_num-1, 1):
        out_title_str_tmp = []
        out_colour_str_tmp = []
        out_att_str_tmp = []
        temp = text[i].split('^')
        out_title_str_tmp.append(temp[0])
        out_title_str_tmp.append(temp[1])
        out_colour_str_tmp.append(temp[0])
        out_colour_str_tmp.append(temp[2])
        out_att_str_tmp.append(temp[0])
        temp[4] = temp[4].strip('\n')
        out_att_str_tmp.append(temp[4])
        out_title_str = json.dumps(out_title_str_tmp, encoding='gbk', ensure_ascii=False) + '\n'
        out_colour_str = json.dumps(out_colour_str_tmp, encoding='gbk', ensure_ascii=False) + '\n'
        out_att_str = json.dumps(out_att_str_tmp, encoding='gbk', ensure_ascii=False) + '\n'
        out_att_str_p = out_att_str.decode("string_escape")
        file_out_title.write(out_title_str)
        file_out_colour.write(out_colour_str)
        file_out_att.write(out_att_str_p)
    file_out_title.close()
    file_out_colour.close()
    file_out_att.close()
    t_stop = time.time()
    print t_stop-t_start


def test_jieba():
    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式


if __name__ == "__main__":
    read_origin_cut()

