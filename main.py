from app.crawler import Crawler      #引用爬虫工具包
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == "__main__":
    ## 地址统计页面
    url = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2020/"
    
    
    province = [["provincetr","</tr>"],["href='","'",">","<"]]
    city = [["citytr","</tr>"],["href='","'",">","<","href='","'",">","<"]]
    county = [["countytr","</tr>"],["href='","'",">","<","href='","'",">","<"],["<td>","</td>","<td>","</td>"]]
    town = [["towntr","</tr>"],["href='","'",">","<","href='","'",">","<"]]
    village = [["villagetr","</tr>"],["<td>","</td>","<td>","</td>","<td>","</td>"]]
    keys = [province,city,county,town,village] 

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
    x.traverse(data, keys)