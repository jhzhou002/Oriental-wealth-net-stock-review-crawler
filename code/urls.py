import csv
import urllib.request
from lxml import etree

# 设置HTTP请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183'
}

# 设置需要爬取的股票代码
stock_code = int(input("请输入股票代码："))

# 设置要爬取的页数范围
start_page = int(input("请输入起始的页码："))
end_page = int(input("请输入结束的页码："))

stock_name = str(stock_code)
file_name = f'{stock_name}_stock_info.csv'
# 打开CSV文件准备写入
with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["标题", "阅读量", "评论", "作者", "最后更新时间", "URL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 如果CSV文件是新创建的，写入表头
    if csvfile.tell() == 0:
        writer.writeheader()

    for page in range(start_page, end_page + 1):
        
        url = f'https://guba.eastmoney.com/list,{stock_code}_{page}.html?returnCode=0'
        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read()
        tree = etree.HTML(content)

        # 解析数据
        items = tree.xpath('//tbody[@class="listbody"]/tr')
        for item in items:
            # 逐条提取数据，并处理缺失情况
            read = item.xpath('.//div[@class="read"]/text()')
            read = read[0].strip() if read else 'error'

            comment = item.xpath('.//div[@class="reply"]/text()')
            comment = comment[0].strip() if comment else 'error'

            title = item.xpath('.//div[@class="title"]//a/text()')
            title = title[0].strip() if title else 'error'

            author = item.xpath('.//div[@class="author"]/a/text()')
            author = author[0].strip() if author else 'error'

            update = item.xpath('.//div[@class="update"]/text()')
            update = update[0].strip() if update else 'error'

            link = item.xpath('.//div[@class="title"]//a/@href')
            if link:
                link = link[0].strip()
                if link.startswith('/news'):
                    link = "https://guba.eastmoney.com" + link
                elif link.startswith('//caifuhao.eastmoney.com'):
                    link = "https:" + link
                else:
                    link = 'error'
            else:
                link = 'error'

            # 创建字典存储单条数据
            data = {
                "标题": title,
                "阅读量": read,
                "评论": comment,
                "作者": author,
                "最后更新时间": update,
                "URL": link
            }

            # 写入单条数据到CSV
            writer.writerow(data)

print(f"所有数据已保存到{file_name}!")
