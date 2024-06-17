import requests
import csv
import re
import time

start_time = time.time()
# 定义请求URL
url = 'https://guba.eastmoney.com/api/getData'

# 定义请求载荷
payload = {
    'path': 'reply/api/Reply/ArticleNewReplyList',
    'plat': 'Web',
    'env': '2',
    'origin': '',
    'version': '2022',
    'product': 'Guba'
}

# 定义请求头
headers = {
    # cookie定期更换
    'Cookie': 'qgqp_b_id=9bd18148d5268b1ad604663111b25171; websitepoptg_api_time=1718433937510; mtp=1; ct=jRVvbf8C8eAUubLQdThpU-ROBuIB2bAGGJ8v7o7ovwvrakUqOcUSev704mfeCc6ps_pPNID9XTs4oeWCQCGpSKWWVAEiXdc-VO-GwrO5KoQikocxuFW8antNo5_bN-_LC00g4-PiPbSc8iSWbkMWUqBqz8fUHR6BALvemxRGi1E; ut=FobyicMgeV5FJnFT189SwCd727ut6we6RRtllPH-KJb9X6lWhAq5wCVdqitPguazjaX79vlt-3LtPZv0Gg-OIGMr_P-tE1RBZvzXAbmV4eEAFzA2jGwEI9zAYoQntfZV3s5eNwgBBL-68TjP-i_w85WeT6tOKi1sMa00VbqlVUJ0ZsOk5UDZrSrc_2Y2WhNFr_sauUxADZMoW1SoNhin2i3pEFLlwWUfbFUUsCCRFM8Y55VVNvDEgiRFTXp5i2mJenwiH2udoSbacRlT45e5v4xHuyEMJpC7AzRvpjXdrq4SAKn4ORQnmDwy5koQsM28HpCQRTLx8JuKL3jBccFSgaj7hij6jrE-; pi=1684047184343106%3Bj1684047184343106%3B%E8%82%A1%E5%8F%8B568312d77x%3Bm7AlIy3sL9qN4W0kx99BoGN9hKBUIF1Fbsq6bGgHfkQLKRAaH5ua4Qqc2oy3K65j0c5IaszLls%2BCse6hqaXztjc9g8lsMjceUEq6UPFxF9fMetST6eYIArjpeoDFM5TRODHlGVxyqUCSbM53pX0FL8Ic6f0j%2FyWfaiccAl5DgmH%2Bv61WY6pJOzytIbM7RWvacrQZDoO%2B%3B812kYt8QdSYs00plVokIB4HfxU5D8zKsLkHFOU0K2rDD82DQKrV500wt97U6vDL1U1M2HGnMnSn2WlSYe%2BuDFcvQCuDhHeHL2efdx047BFdfnoG6iD0YRJ99QRmarHVPgMQLMqtSfnTUFLlTtDWW5MMRqPn%2Fng%3D%3D; uidal=1684047184343106%e8%82%a1%e5%8f%8b568312d77x; sid=; vtpst=|; st_si=06762407280692; st_asi=delete; st_pvi=95297412281025; st_sp=2024-06-15%2014%3A45%3A37; st_inirUrl=https%3A%2F%2Fcn.bing.com%2F; st_sn=2; st_psi=20240617144309573-117001354293-1897263224',
    'Host': 'guba.eastmoney.com',
    'Origin': 'https://guba.eastmoney.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}


# 读取urls.txt文件中的所有URL
with open('guba_urls.txt', 'r', encoding='utf-8') as file:
    referer_urls = [line.strip() for line in file.readlines()]

# 定义一个递归函数，用于提取评论及其子评论
def extract_comments(comments):
    for comment in comments:
        comment_data = {
            '评论者ID': comment.get('user_id'),
            '评论者名称': comment.get('reply_user', {}).get('user_nickname'),
            '评论内容': comment.get('reply_text'),
            '点赞人数': comment.get('reply_like_count', 0),
            '发布日期': comment.get('reply_time'),
            '发布IP': comment.get('reply_ip_address', '')
        }
        yield comment_data
        # 如果存在子评论，则递归提取子评论
        yield from extract_comments(comment.get('child_replys', []))

# 准备CSV文件的列名
csv_columns = ['评论者ID', '评论者名称', '评论内容', '点赞人数', '发布日期', '发布IP']

# 打开一个新的CSV文件用于写入
with open('guba_comments.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()

    # 遍历所有URL
    for referer_url in referer_urls:
        # 从URL中提取股票代码和postid
        match = re.search(r'news,(\d+),(\d+).html', referer_url)
        if match:
            stock_code, post_id = match.groups()
            # 更新请求头中的Referer
            headers['Referer'] = referer_url
            # 更新payload中的股票代码和postid
            payload['code'] = stock_code
            payload['param'] = f'postid={post_id}&sort=1&sorttype=1&p=1&ps=30'
            
            # 发送POST请求
            response = requests.post(url, data=payload, headers=headers)
            # 解析JSON响应数据
            data = response.json()

            # 检查响应中是否有评论数据
            if 're' in data:
                # 从递归函数中获取所有评论数据并写入CSV
                for comment_data in extract_comments(data['re']):
                    writer.writerow(comment_data)

print("评论数据已保存到文件。")
end_time = time.time()
run_time = end_time - start_time
print(f"程序运行时间:{int(run_time)}s")