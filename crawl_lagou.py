import requests  
import math  
import pandas as pd  
import time
import urllib
import urllib.request
from bs4 import BeautifulSoup as Bs
import random

def get_json(url,num,pos):  
    '''''从网页获取JSON,使用POST请求,加上头部信息'''  
    my_headers = {  
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',  
            'Host':'www.lagou.com',  
            'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',  
            'X-Anit-Forge-Code':'0',  
            'X-Anit-Forge-Token': 'None',  
            'X-Requested-With':'XMLHttpRequest'  
            }  

    my_data = {  
            'first': 'true',  
            'pn':num,  
            'kd':pos}  

    res = requests.post(url, headers = my_headers, data = my_data)  
    res.raise_for_status()  
    res.encoding = 'utf-8'  
    # 得到包含职位信息的字典  
    page = res.json()  
    return page


def get_page_num(count):  
    '''''计算要抓取的页数'''  
    # 每页15个职位,向上取整  
    res = math.ceil(count/15)  
    # 拉勾网最多显示30页结果  
    if res > 30:  
        return 30  
    else:  
        return res  

def get_page_info(jobs_list):  
    '''''对一个网页的职位信息进行解析,返回列表'''  
    page_info_list = []  
    for n, i in enumerate(jobs_list): 
        print('现在进行到第{}个；'.format(n))
        job_info = []  
        job_info.append(i['companyFullName'])  
        job_info.append(i['companyShortName'])  
        job_info.append(i['companySize'])  
        job_info.append(i['financeStage'])  
        job_info.append(i['district'])  
        job_info.append(i['positionName'])  
        job_info.append(i['workYear'])  
        job_info.append(i['education'])  
        job_info.append(i['salary'])  
        job_info.append(i['positionAdvantage'])  
        job_info.append(i['positionId'])
        
        url = 'https://www.lagou.com/jobs/'+ str(i['positionId']) +'.html'
        headers = {  
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',  
                'Host':'www.lagou.com',  
                'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?labelWords=&fromSearch=true&suginput=',  
                'X-Anit-Forge-Code':'0',  
                'X-Anit-Forge-Token': 'None',  
                'X-Requested-With':'XMLHttpRequest'  
                }  

        #data = urllib.parse.urlencode(dict).encode('utf-8')
        #data参数如果要传必须传bytes（字节流）类型的，如果是一个字典，先用urllib.parse.urlencode()编码。
        time_sleep = random.randint(10, 30)
        time.sleep(time_sleep)  
        request = urllib.request.Request(url = url, headers = headers,method = 'POST')
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        soup = Bs(html, 'html.parser')
        try:
            content = soup.find('dd', class_='job_bt').get_text()
            job_info.append(content)
        except:
            print(i['positionId'])
        finally:    
            page_info_list.append(job_info)  
    return page_info_list 

def main():  
    random.seed(36)

    url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&needAddtionalResult=false'
    #url = 'https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false'  
    # 先设定页数为1,获取总的职位数  
    pos = input('请输入你想查阅的职位名称：')
    page_1 = get_json(url,1,pos)  
    total_count = page_1['content']['positionResult']['totalCount']  
    num = get_page_num(total_count)  
    total_info = []  
    time_sleep = random.randint(10, 30)
    time.sleep(time_sleep)  
    print('职位总数:{},页数:{}'.format(total_count,num))  

    for n in range(1,num+1):  
        # 对每个网页读取JSON, 获取每页数据  
        page = get_json(url,n,pos)  
        jobs_list = page['content']['positionResult']['result']  
        page_info = get_page_info(jobs_list)  
        total_info += page_info  
        print('已经抓取第{}页, 职位总数:{}'.format(n, len(total_info)))  
        # 每次抓取完成后,暂停一会,防止被服务器拉黑  
        time_sleep = random.randint(10, 30)
        time.sleep(time_sleep)  
    #将总数据转化为data frame再输出  
    df = pd.DataFrame(data = total_info,columns = ['公司全名','公司简称','公司规模','融资阶段','区域','职位名称','工作经验','学历要求','工资','职位福利','职位描述'])   
    df.to_csv('lagou_jobs.csv',index = False)  
    print('已保存为csv文件.')  

if __name__== "__main__":   
    main()  