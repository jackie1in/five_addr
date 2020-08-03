import requests as r
import time
import re
 
#  crawler 类
#  国家统计局主页小爬虫类
 
#  get_http(url)  得到页面数据
#  方法， 参数url，为需要操作的页面地址
 
#  主要方法：
 
#  traverse(data, keys)  
#  遍历页面所有地址数据 合并了以下三个方法，只有调用这个方法就可以了
#  传递页面数据，和正确的keys参数就能得到正确的数据
#  参数data,通过get_http(url)方法得到对页面数据，参数keys为分割关键字符
 
#  keys参数例子：
 
#  省份 = [["provincetr","</tr>"],["href='","'",">","<"]]   
#  ["provincetr","</tr>"] 是提取provincetr和<tr>中的省列表 得到所有省数据列表，
#  ["href='","'",">","<"] 是提取省列表里的地址链接和地名
 
#  以下的参数原理都一样
#  城市 = [["citytr","</tr>"],["href='","'",">","<","href='","'",">","<"]]    
#  区县 = [["countytr","</tr>"],["href='","'",">","<","href='","'",">","<"]]  
#  街道 = [["towntr","</tr>"],["href='","'",">","<","href='","'",">","<"]]    
#  社区 = ["villagetr","<td>","<td>","<td>","</td>"]   
#  社区参数直接提取最终地名，不需要再取链接rul了     
#  keys = [省份,城市,区县,街道,社区] 
#  keys为合并所有提取的字符，作为参数传递过去 traverse(data, keys)  
 
 
class Crawler:
 
    url = ""
 
    def __init__(self, url):
        self.url = url
 
    # 获得页面数据
    def get_http(self, url):
        i = 0
        try:
            data_request = r.get(url, timeout = 5)   
            if data_request:
                i = 10
                data_request.encoding = "gb2312"
                text_request = data_request.text
                return text_request
            else:
                print("连接超时。。。")
        except:
            return False
        
 
    # 对页面数据提取主要内容 返回列表
    def str_slice(self, data, key_str): 
 
        index_strat = 0         # 开始下标
        index_end = 0           # 结束下标
        endword = key_str[-1]   # 结尾关键字符
        d_list = []             # 数据储存列表
 
        t = 1
        while t == 1:
            for i in key_str:
                # 判断是否为结尾关键字符
                if i in endword:
                    index_end =data.find(i, index_strat)
                    t = 1
                    # 判断是否找到关键字符
                    if index_end < 0:
                        t = 0
                else:
                    index_strat =data.find(i, index_strat)
                    # 判断是否找到关键字符
                    if index_strat > 0:
                        index_strat = index_strat + len(i)
                        t = 1
                    else:
                        t = 0
            if t == 1:
                # 数据切片 
                slice_data = data[index_strat : index_end]          
                d_list.append(slice_data)      
                # 让起始下标 变为 结尾下标                     
                index_strat = index_end
        # 列表中元素 遍历结束，重置起始下标
        index_strat = 0
        return d_list
 
    # 对主要内容列表再次提取最终的 链接地址和地名 转为字典
    def list_slice(self, list_data, key_str, data_type = "dict",range = 0):
        index_strat = 0     # 开始下标
        index_end = 0       # 结束下标
        dic = {}            # 数据储存字典
        # 遍历数据列表
        for a in list_data:
            t = 1
            while t == 1:
                numb = 0        # 定义查找次数
                ran = 0
                value = ""
                # 查找关键字符key_str列表，两个数据为一组转化为字典
                for i in key_str:
                    # 当第一次执行，或第四次执行，获取开始下标
                    if numb == 0 or numb == 3 :
                        index_strat = a.find(i,index_strat,)
                        if index_strat > 0:
                            index_strat = index_strat + len(i)
                            # 执行计数+1
                            numb += 1      
                            t = 1
                        else:
                            t = 0
                            continue
                    # 否则获取 结尾下标
                    else:
                        index_end = a.find(i, index_strat,)
                        if index_end > 0 :
                            # 执行计数+1
                            numb += 1
                            t = 1
                        else:
                            t = 0
                            continue
                    # 当第三次执行数据，获得开始和结尾下标，对数据进行切片，赋值给value
                    # 并把开始下标跳到结尾所在的下标
                    if numb == 2:
                        value = a[index_strat : index_end]
                        index_strat = index_end
                        # 执行计数+1
                        numb += 1
                    # 当第六次执行数据，对数据进行切片赋值给c
                    # c为键，value为值添加到字典
                    if numb == 5:
                        if ran >= range:
                            c = a[index_strat : index_end]
                            dic.update({value : c})
                            # 重置计数
                            ran = 0
                            numb = 0
                        else:
                            ran += 1
                            numb = 0                         
            # 重置开始下标
            index_strat = 0
        # 返回字典
        return dic
    
    # 遍历页面数据， 合并了str_slice方法和list_slice方法
    def data_slice(self, 页面数据, 关键字符, save = None,range = 0):
 
        ## 对页面数据进行 分割返回列表数据
        列表数据 = self.str_slice(页面数据, 关键字符[0])   
 
        ##  对列表数据进行 分割返回字典数据
        字典数据 = self.list_slice(列表数据, 关键字符[1], range)
 
        ## 返回字典数据
        return 字典数据
 
    ## 遍历所有地址， 需要传递data城市页面数据
    def traverse(self, data, keys):
 
        ## 调用遍历页面数据方法， 传递data参数，返回省份字典
        print("开始获取省份数据*********************************************************************************")
        省份字典 = self.data_slice(data, keys[0])
        cont = 0
 
        if 省份字典:
            ## 遍历省份
            for s1,s2 in 省份字典.items():
                while cont < 6:
                    ##time.sleep(2)
 
                    ## 获取s1省份下一级城市页面数据, 返回省份页面数据data                   
                    data = self.get_http(self.url+s1)
                    if data:
                        break
                    cont+=1
                    time.sleep(2)
                cont = 0
                s1 =  s1[0:s1.find(".")] + "/"
                print("开始获取城市数据*********************************************************************************")
                ## 调用遍历页面数据方法， 传递城市数据data参数，返回城市字典
                城市字典 = self.data_slice(data, keys[1],range=1)
                if 城市字典:
                    # 遍历城市
                    for c1,c2 in 城市字典.items():
                        while cont < 6:
                            ##time.sleep(2)
 
                            ## 获取c1城市下一级区县页面数据， 返回区县页面数据data
                            data = self.get_http(self.url+c1)
                            if data:
                                break
                            cont+=1
                            time.sleep(2)
                        cont = 0
                        print("开始获取区县数据*********************************************************************************")
                        ## 调用遍历页面数据方法， 传递区县数据data参数，返回城市字典
                        区县字典 = self.data_slice(data, keys[2],range=1)
                        if 区县字典:
                            # 遍历区县
                            for q1,q2 in 区县字典.items():
                                while cont < 6:
                                    ##time.sleep(2)
 
                                    ## 获取q1下一级街道页面数据， 返回街道页面数据data
                                    data = self.get_http(self.url+s1+q1)
                                    if data:
                                        break
                                    cont+=1
                                    time.sleep(2)
                                cont = 0
                                q1 = q1[0:q1.find("/")] + "/"
                                print("开始获取街道数据*********************************************************************************")
                                 ## 调用遍历页面数据方法， 传递街道数据data参数，返回街道字典
                                街道字典 = self.data_slice(data, keys[3],range=1)
                                if 街道字典:
                                    # 遍历街道
                                    for j1,j2 in 街道字典.items():
                                        while cont < 6:
                                            ##time.sleep(2)
                                            ## 获取j1下一级社区页面数据， 返回社区页面数据data
                                            data = self.get_http(self.url+s1+q1+j1)
                                            if data:
                                                break
                                            cont+=1
                                            time.sleep(2)
                                        cont = 0
                                        print("开始获取社区数据*********************************************************************************")
                                        ## 调用遍历页面数据方法， 传递社区数据data参数，返回社区列表
                                        社区列表 = self.str_slice(data, keys[4])
                                        for 社区 in 社区列表:
                                            最终地址 = s2+"-->"+c2+"-->"+q2+"-->"+j2+"-->"+社区
                                            print(最终地址)
                                else:
                                    print("街道遍历结束")
                        else:
                            print("区县遍历结束")
                else:
                    print("城市遍历结束")
        else:
            print("省份遍历结束")
