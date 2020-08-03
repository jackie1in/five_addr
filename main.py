from app.crawler import Crawler      #引用爬虫工具包
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == "__main__":
    ## 地址统计页面
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/"
    
    
    省份 = [["provincetr","</tr>"],["href='","'",">","<"]]
    城市 = [["citytr","</tr>"],["href='","'",">","<","href='","'",">","<"]]
    区县 = [["countytr","</tr>"],["href='","'",">","<","href='","'",">","<"]]
    街道 = [["towntr","</tr>"],["href='","'",">","<","href='","'",">","<"]]
    社区 = ["villagetr","<td>","<td>","<td>","</td>"]
    keys = [省份,城市,区县,街道,社区] 

    ## 创建crawler爬虫实例
    x = Crawler(url)
    
    ## 获得页面数据data
    data = x.get_http(url)
    while data == False:
        time.sleep(2)
        print("重新链接中。。。")
        data = x.get_http(url)
    
    ## 调用调用crawler的地址遍历方法， 传递data页面数据，和keys地址关键字符参数
    ## 返回所有地址列表
    地址列表 = x.traverse(data, keys)