import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from lxml import etree
import time

start_time = time.time()

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 启动Chrome浏览器
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义CSV文件字段
fieldnames = [
    "title", "用户id","评论者", "评论者IP", "评论时间", "评论内容", "评论点赞数", "评论者链接"
]

# 打开CSV文件以保存提取的数据
with open('caifuhao_comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # 读取urls.txt文件中的所有URL
    with open('caifuhao_urls.txt', 'r', encoding='utf-8') as file:
        referer_urls = [line.strip() for line in file.readlines()]

    # 遍历每个URL并提取评论数据
    for url in referer_urls:
        # 打开目标网页
        driver.get(url)

        # 等待页面加载
        time.sleep(3)

        # 点击“加载更多”按钮，直到按钮不存在为止
        while True:
            try:
                load_more_button = driver.find_element(By.XPATH, '//div[@class="loadMbtn bottombtn fl"]')
                load_more_button.click()
                time.sleep(3)  # 等待加载更多评论
            except:
                break

        # 获取页面HTML内容
        page_source = driver.page_source
        tree = etree.HTML(page_source)

        # 提取文章标题
        title = tree.xpath('//div[@class="grid_wrapper"]//h1[@class="article-title"]/text()')
        title = title[0].strip() if title else 'error'

        # 提取评论项
        items = tree.xpath('//div[@class="list_cont"]')
        for item in items:
            # 提取评论字段
            commenter_id = item.xpath('.//a[@class="replyer_name"]/@data-popper')
            commenter_id = commenter[0].strip() if commenter_id else 'error'
            
            commenter = item.xpath('.//a[@class="replyer_name"]/text()')
            commenter = commenter[0].strip() if commenter else 'error'

            comment_time = item.xpath('.//div[@class="publish_time fr"]/span[1]/text()')
            comment_time = comment_time[0].strip() if comment_time else 'error'

            ip = item.xpath('.//div[@class="publish_time fr"]/span[2]/text()')
            ip = ip[0].strip() if ip else 'error'

            comment_content = item.xpath('.//div[@class="short_text"]/text()')
            comment_content = comment_content[0].strip() if comment_content else 'error'

            comment_likes = item.xpath('.//div[@class="level1_btns"]//span[@class="z_num"]/text()')
            comment_likes = comment_likes[0].strip() if comment_likes else 'error'
            if comment_likes == '点赞':
                comment_likes = 0

            commenter_link = item.xpath('.//a[@class="replyer_name"]/@href')
            commenter_link = "https:" + commenter_link[0].strip() if commenter_link else 'error'

            # 写入评论数据到CSV文件
            data = {
                "title": title,
                "用户id": commenter_id,
                "评论者": commenter,
                "评论者IP": ip,
                "评论时间": comment_time,
                "评论内容": comment_content,
                "评论点赞数": comment_likes,
                "评论者链接": commenter_link
            }
            writer.writerow(data)

            # 提取并写入回复评论
            replies = item.xpath('.//div[@class="level2_item"]')
            for reply in replies:
                replier_id = reply.xpath('.//a[@class="replyer_name"]/@data-popper')
                replier_id = replier_id[0].strip() if replier_id else 'error'
                
                replier = reply.xpath('.//a[@class="replyer_name"]/text()')
                replier = replier[0].strip() if replier else 'error'

                reply_time = reply.xpath('.//div[@class="time fl"]/span[1]/text()')
                reply_time = reply_time[0].strip() if reply_time else 'error'

                reply_content = reply.xpath('.//span[@class="l2_short_text"]/text()')
                reply_content = reply_content[0].strip() if reply_content else 'error'

                reply_likes = reply.xpath('.//span[@class="z_num"]/text()')
                reply_likes = reply_likes[0].strip() if reply_likes else 'error'
                if reply_likes == '点赞':
                    reply_likes = 0

                reply_ip = reply.xpath('.//span[@class="reply_ip"]/text()')
                reply_ip = reply_ip[0].strip() if reply_ip else 'error'

                replier_link = reply.xpath('.//a[@class="replyer_name"]/@href')
                replier_link = "https:" + replier_link[0].strip() if replier_link else 'error'

                reply_data = {
                    "title": title,
                    "用户id": replier_id,
                    "评论者": replier,
                    "评论者IP": reply_ip,
                    "评论时间": reply_time,
                    "评论内容": reply_content,
                    "评论点赞数": reply_likes,
                    "评论者链接": replier_link
                }
                writer.writerow(reply_data)

print("所有数据已保存到文件中!")

# 关闭浏览器
driver.quit()
end_time = time.time()
run_time = end_time - start_time
print(f"程序运行时间:{int(run_time)}s")
