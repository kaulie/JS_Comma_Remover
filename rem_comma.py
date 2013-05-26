#-*- coding: utf8 -*-
import random

#去掉js文件中的逗号

import os, sys
import re

js_file_pattern = re.compile('(.)*.jsp$')

js_pattern = re.compile('(,\s*})|(,\s*])')

#是否保留原文件
keep_raw = True
#是否保留日志
log2file = True


def repl(m):
    r = m.group(0)[1:]
    return r


js_file_list = []

#===============================遍历项目文件===========================================

def main():
    if(len(sys.argv))==0:
        scan_path = sys.argv[1]
        tranverse(scan_path)

def tranverse(root_path):
    for dirname, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            _filename = os.path.abspath(os.path.join(dirname, filename))
            if js_file_pattern.match(_filename):
                js_file_list.append(_filename)
    match_num = 0
    rewrite_num = 0
    for f in js_file_list:
        scan_result = scan(f)
        if scan_result[0] == 0:
            match_num += 1
            if keep_raw:
                rewrite(f+'.bak',scan_result[1])
            if not rewrite(f,scan_result[2]):
                rewrite_num += 1
    print '================扫描结果================='
    print("扫描文件%s个" % len(js_file_list))
    print("匹配文件%s个" % match_num)
    print("成功重写文件%s个" % rewrite_num)      
          
sample_file = '/home/gl/workspace/xyspcs/WebRoot/system/user.jsp'


    
def scan(fname):
    f = open(fname, 'r')
    raw_content = None
    new_content = None
    return_code = 1 
    try:
        raw_content = f.read()
        new_content = re.sub(js_pattern, repl, raw_content)
    except Exception,e:
        print '操作文件时发生异常 > %s,%s' % (fname,e)
    else:
        if(raw_content and new_content and new_content != raw_content):
            return_code = 0
            print("文件 %s 找到匹配项" % fname)
    finally:
        f.close()
    return return_code,raw_content,new_content
        
def rewrite(_filename,content):        
    f = open(_filename, 'w')
    ret_code = 0
    try:
        f.write(content)
    except Exception,e:
        print '覆写文件时发生异常 > %s,%s' % (_filename,e)
        ret_code = 1
    finally:
        f.close()            
    return ret_code



if __name__ == '__main__':
    main()
