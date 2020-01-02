# _*_ coding: utf8 _*_
import re


def get_name(txt):
    if txt:
        name_list = re.findall(r'(.*?)（统一', txt)
        if name_list:
            name = name_list[0]
            # print(name)
        else:
            name_list = re.findall(r'(.*?)\(统一', txt)
            if name_list:
                name = name_list[0]
                # print( name)
            else:
                name = ''
        code_list = re.findall(r'注册号：(.*?)）', txt)
        if code_list:
            code = code_list[0]
        else:
            code_list = re.findall(r'号：(.*?)\)', txt)
            if code_list:
                code = code_list[0]
            else:
                code = ''
    else:
        name = ''
        code = ''
    return name, code


def content_split(txt):
    if txt:
        txt_list = txt.split('，')
        cf_sy = txt_list[1]
        cf_yj = txt_list[2]
        cf_jg = txt_list[3]
    else:
        cf_sy = ''
        cf_yj = ''
        cf_jg = ''
    return cf_sy, cf_yj, cf_jg


def get_result(string):
    if string:
        str_list = string.split('。')
        cf_sy = str_list[0]
        cf_jg = str_list[1]
    else:
        cf_sy = ''
        cf_jg = ''
    return cf_sy, cf_jg


if __name__ == '__main__':
    txt = '纳雍县以角泰旺种植农民专业合作社(统一社会信用代码/注册号：93520525MA6EGN9K19）'
    txt2 = '经查，你单位在补报未报年份的年度报告并公示后申请移出，根据《农民专业合作社年度报告公示暂行办法》第 十三 条的规定，决定将你单位移出经营异常名录。'
    txt3 = """经查，你单位因被列入经营异常名录届满3年仍未履行相关义务，违反了《企业信息公示暂行条例》的有关规定且情节严重。依据《严重违法失信企业名单管理暂行办法》第五条第一款第（一）项的规定，现决定将你单位列入严重违法失信企业名单，并通过企业信用信息公示系统向社会公示。你单位应主动纠正相关违法行为，并于2024年10月29日后申请移出严重违法失信企业名单。"""
    # name, code = get_name(txt)  # print(code)
    # sy, yj, jg = content_split(txt2)
    sy, jg = get_result(txt3)
    print(sy)
    print(jg)

