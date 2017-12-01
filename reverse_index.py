# -*- coding: utf-8 -*-
import sys
default_encoding="utf-8"
import os
import jieba as jb
#### 取得文档路径

def getFilePathList(path):
    file_path_list = []
    for root, dirs, files in os.walk(path):
        for filespath in files:
            file_path_list.append(os.path.join(root,filespath))
    return file_path_list

####读取一个文档的内容，保持原文档格式
def getTextContext(file_path):
    content=""
    fp =  open(file_path,mode='r')
    for line  in fp.readlines():
        content+=line
    fp.close()
    print("finish read : "+ file_path)
    return content

####切割一个文档，返回一个list
def cut_content(content):
    cut_content_list=[]
    cut_content_list = list(jb.cut(content, cut_all=False))  ###使用jieba 分词
    return cut_content_list

####获取所有文本
def getAllContents(path):
    all_content_dir={}
    err_file_path=[]
    file_path_list= getFilePathList(path)
    for file_path in file_path_list:
        try:
            all_content_dir[file_path]=getTextContext(file_path)
        except Exception as e:
            err_file_path.append(path)
            print(e)
            continue  ###'gbk' codec can't decode byte 0xfd in position 1545: illegal multibyte sequence,暂时无法解决此问题
    return all_content_dir,err_file_path

####对所有文本切割
def getAllCutContent(all_content_dir):
    cut_content_dir={}
    for key in all_content_dir:
        print("current cut:"+ key)
        cut_content_dir[key]=cut_content(all_content_dir[key])
    return cut_content_dir


#####获取所有关键词
def getAllKeyWords(cut_content_dir):
    key_words_list=[]
    key_words_set=set()
    for key in cut_content_dir:
        for word in cut_content_dir[key]:
            key_words_set.add(word)
    key_words_list=list(key_words_set)
    return key_words_list

###计算倒排表
def getInverseIndex(key_words_list,all_content_dir):
    inverse_index_dir={}
    for word in key_words_list:
        print(word)
        indx_dir={}
        for text_name in all_content_dir:
            indx_list=getIndex(word,all_content_dir[text_name])
            if len(indx_list)!=0:
                indx_dir[text_name]=indx_list ####将此关键词在当前文档的索引列表组成dict
            inverse_index_dir[word]=indx_dir  ####对此关键词，组成{keyword:{txt_name1:[1,3,8],txt_name2:[5,6,9],...}}
    return inverse_index_dir
#####获取每个关键词在文本中的位置list
def getIndex(keyword,content):
    # multiple searches of a string for a substring
    # using s.find(sub[ ,start[, end]])
    indx_list=[]
    search = keyword
    start = 0
    while True:
        index = content.find(search, start)
        # if search string not found, find() returns -1
        # search is complete, break out of the while loop
        if index == -1:
            break
        indx_list.append(index)
        # move to next possible start position
        start = index + 1
    return indx_list

if __name__ == '__main__':
    all_content_dir,err_path_list=getAllContents(r"d:\nlp1")
    print(len(all_content_dir))
    print(len(err_path_list))
    cut_content_dir = getAllCutContent(all_content_dir)
    key_words_list=getAllKeyWords(cut_content_dir)
    print(len(key_words_list))
    inverse_indx_dir=getInverseIndex(key_words_list,all_content_dir)
    print(key_words_list[0]+":::"+str(inverse_indx_dir[key_words_list[0]]))

    txt_name_indx_dir=inverse_indx_dir[key_words_list[0]] ###获取文档名和关键词索引dict
    print(txt_name_indx_dir)

    # for txt_name in txt_name_indx_dir:
    #     content=getTextContext(txt_name)
    #     print(content)
    #     print(content.index(key_words_list[0]))

    # file_path_list = getFilePathList()
    # for file_path in file_path_list:
    #     print(file_path)
    # content=  getTextContext(r'd:\nlp\train\C7-History\C7-History879.txt')
    # print(content)
    # cut_content_list=cut_content(content)
    # print(cut_content_list)
