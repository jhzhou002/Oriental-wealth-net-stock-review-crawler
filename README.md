东方财富网股票评论获取说明

步骤：

- 执行urls.py文件，输出文件中的url列的url分为caifuhao和guba两类，筛选出每一类的url并分别复制到caifuhao_urls.txt和guba_urls.txt文件（已在文件夹中建好）中

  ![image-20240617163545982](https://cdn.jsdelivr.net/gh/jhzhou002/blogImage@main/image/image-20240617163545982.png)

- 分别执行caifuhao_comments.py和guba_comments.py（由于这个代码是直接向服务器发送请求获取数据，速度比较快，可以先执行这个文件，而且url大部分是这种类型的）文件，程序完成后会输出该支股票下所有话题的评论

- 想要获取不同股票的评论，只需在urls.py运行的时候指定即可

思路：获取每支股票下所有话题url——>通过循环遍历每个话题url来获取每个话题下的所有评论

![image-20240617163319006](https://cdn.jsdelivr.net/gh/jhzhou002/blogImage@main/image/image-20240617163319006.png)

**注意：运行之前先把谷歌驱动放到正确位置**，否则python文件运行报错，我在文件放了一个驱动，对应的谷歌浏览器version：126.xxx

![image-20240616202958674](https://cdn.jsdelivr.net/gh/jhzhou002/blogImage@main/image/image-20240616202958674.png)

演示视频：https://www.bilibili.com/video/BV1fJgje8E3E/?vd_source=6cebfb74eb1fc5510e18c96ef6974f6f

欢迎关注我的公众号，不定期更新一些爬虫案例，一起学习交流！
![image](https://github.com/jhzhou002/Oriental-wealth-net-stock-review-crawler/assets/117413703/caf58e5b-2188-473b-ae56-4fd70bd35d15)

