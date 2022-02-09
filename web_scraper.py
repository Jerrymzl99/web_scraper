import requests # 导入网页请求库
import urllib.request as urllib # 导入网页请求库
import re

from bs4 import BeautifulSoup # 导入网页解析库


# 发起请求
def start_requests(url):
    print(url) # 用这条命令知道当前在抓取哪个链接，如果发生错误便于调试
    r = requests.get(url)
    return r.content


# 解析一级网页，获取url列表
def get_page(text):
    with open("article_link.txt", "a") as f:
        soup = BeautifulSoup(text, 'html.parser')
        article_list = soup.find_all('a', href=re.compile(r'^/news/'))
        
        for article in article_list:
            href = article.get('href')
            temp = 'https://research.unt.edu'+href[:]+'\n'
            f.write(temp)
    f.close()

# 解析二级网页，获取信息
def parse_page(pageurls):
    count = 0
    with open("article_link.txt","r") as f:
        for line in f.readlines():
            line = line.strip()
            count+=1

            try:
                r = requests.get(line, timeout=30)
                r.raise_for_status()
                r.encoding = r.apparent_encoding
            except:
                print('Error')
                break    

            soup = BeautifulSoup(r.text, "html.parser")
            #搜索目标标签div
            s = soup.find_all('div',class_="field field-name-field-paragraph-text field-type-text-long field-label-hidden field-wrapper")
            with open("content.txt","a",encoding='utf-8') as c:          
                for i in s:
                    #写入文件
                    c.write(i.get_text())
            c.close()
            # print("第%d篇爬取成功！……loading……"%(count))
    f.close()
    
#爬取需要一定时间，完成后输出“DONE”
    print('DONE')
    
def main():
    for i in range(0, 10):
        url = 'https://research.unt.edu/news?page=' + str(i)
        text = start_requests(url)
        pageurls = get_page(text) # 解析一级页面
        content = parse_page(pageurls) # 获取二级页面

if __name__ == '__main__':
    main()