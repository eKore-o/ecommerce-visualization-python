import csv
import json
import os
from DrissionPage import ChromiumPage, ChromiumOptions

# 设置Edge浏览器路径
edge_path = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# 创建配置对象
co = ChromiumOptions()
co.set_browser_path(edge_path)

# 使用配置创建页面对象
dp = ChromiumPage(addr_or_opts=co)

# 设置监听
dp.listen.start('https://h5api.m.taobao.com/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/?')


def spider(k, v):
    url = v
    dp.get(url)

    dp.wait(3)

    csv_file = 'tb.csv'

    file_exist = os.path.isfile(csv_file)

    # 定义csv文件表头
    header = ['标题', '店铺', '价格', '付款人数', '发货地址', '详情页地址', '图片地址', '特点列表', '卖点', '商品']

    # 打开文件 数据
    with open(csv_file, mode='a+', encoding='utf-8-sig', newline='') as file:  # 使用utf-8-sig避免中文乱码
        writer = csv.writer(file)

        # 如果文件不存在，先写表头
        if not file_exist:
            writer.writerow(header)

        total_pages = 10

        for page_number in range(1, total_pages + 1):
            try:
                dp.wait(3)
                dp.scroll.to_bottom()

                # 检查是否有下一页按钮
                next_btn = dp.ele('css:.next-btn.next-medium.next-btn-normal.next-pagination-item.next-next')
                if next_btn:
                    next_btn.click()
                    dp.wait(5)
                    dp.scroll.to_bottom()

                # 等待数据响应
                resp = dp.listen.wait(timeout=10)

                if resp and resp.response and resp.response.body:
                    json_data = resp.response.body
                    # 去除没用的
                    json_str = json_data[json_data.index('(') + 1:json_data.rindex(')')]
                    data = json.loads(json_str)

                    feeds = data['data']['itemsArray']

                    print(f"第{page_number}页的数据解析成功！")
                    for feed in feeds:
                        title = feed.get('title', '')
                        ShopInfo = feed.get('shopInfo', {}).get('title', '无店铺')
                        price = feed.get('price', 0)
                        realSales = feed.get('realSales', '付款人数')
                        procity = feed.get('procity', '暂无地址')
                        auctionURL = feed.get('auctionURL', '暂无详情页地址')
                        img_url = feed.get('pic_path', '暂无图片地址')
                        propertyName_list = [tag.get('propertyName', '') for tag in feed.get('structuredUSPInfo', [])]
                        summaryTips = feed.get('summaryTips', '')

                        shop_type = k

                        # 写入一行数据
                        writer.writerow([
                            title, ShopInfo, price, realSales,
                            procity, auctionURL, img_url,
                            str(propertyName_list), summaryTips, shop_type  # 将列表转为字符串
                        ])
            except Exception as e:
                print(f"第{page_number}页处理出错: {e}")
                continue

    print('数据成功写入')


shop_dict = {
    '现代装饰画':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&channelSrp=bingSomama&clk1=30b229df4f7b1de9239509281c20deef&keyword=%E7%8E%B0%E4%BB%A3%E8%A3%85%E9%A5%B0%E7%94%BB&localImgKey=&msclkid=aca6dfb646831c9a172bb618c0f878b0&page=1&q=%E7%8E%B0%E4%BB%A3%E8%A3%85%E9%A5%B0%E7%94%BB&refpid=mm_2898300158_3078300397_115665800437&spm=tbpc.pc_sem_alimama%2Fa.201867-main.d5_15_1.f9c82a89Fyj7Qq&tab=all',
    '零食':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&channelSrp=bingSomama&clk1=30b229df4f7b1de9239509281c20deef&keyword=%E9%9B%B6%E9%A3%9F&localImgKey=&msclkid=aca6dfb646831c9a172bb618c0f878b0&page=1&q=%E9%9B%B6%E9%A3%9F&refpid=mm_2898300158_3078300397_115665800437&spm=tbpc.pc_sem_alimama%2Fa.201867-main.d5_15_1.f9c82a89Fyj7Qq&tab=all',
    '吉他':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&channelSrp=bingSomama&clk1=30b229df4f7b1de9239509281c20deef&keyword=%E5%90%89%E4%BB%96&localImgKey=&msclkid=aca6dfb646831c9a172bb618c0f878b0&page=1&q=%E5%90%89%E4%BB%96&refpid=mm_2898300158_3078300397_115665800437&spm=tbpc.pc_sem_alimama%2Fa.201867-main.d5_15_1.f9c82a89Fyj7Qq&tab=all',
    '玩具':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&channelSrp=bingSomama&clk1=30b229df4f7b1de9239509281c20deef&commend=all&ie=utf8&initiative_id=tbindexz_20170306&keyword=%E7%8E%A9%E5%85%B7&localImgKey=&msclkid=aca6dfb646831c9a172bb618c0f878b0&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E7%8E%A9%E5%85%B7&refpid=mm_2898300158_3078300397_115665800437&search_type=item&sourceId=tb.index&spm=tbpc.pc_sem_alimama%2Fa.search_manual.0&ssid=s5-e&tab=all',
    '白酒':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&channelSrp=bingSomama&clk1=30b229df4f7b1de9239509281c20deef&commend=all&ie=utf8&initiative_id=tbindexz_20170306&keyword=%E7%99%BD%E9%85%92&localImgKey=&msclkid=aca6dfb646831c9a172bb618c0f878b0&page=1&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E7%99%BD%E9%85%92&refpid=mm_2898300158_3078300397_115665800437&search_type=item&sourceId=tb.index&spm=tbpc.pc_sem_alimama%2Fa.search_manual.0&ssid=s5-e&tab=all',

    '手机':'https://uland.taobao.com/sem/tbsearch?bc_fl_src=tbsite_T9W2LtnM&boxFilterList=&channelSrp=bingSomama&clk1=7eb64056229833f816fd756e2a529148&commend=all&ie=utf8&initiative_id=tbindexz_20170306&keyword=%E6%89%8B%E6%9C%BA&localImgKey=&msclkid=257a1414b1211d0186477db36dbb526d&page=2&preLoadOrigin=https%3A%2F%2Fwww.taobao.com&q=%E6%89%8B%E6%9C%BA&recommend_iconTabData=%7B%22iconType%22%3A%22%22%7D&refpid=mm_2898300158_3078300397_115665800437&search_type=item&sourceId=tb.index&spm=tbpc.pc_sem_alimama%2Fa.search_hover.0&ssid=s5-e&tab=all'
}

for k, v in shop_dict.items():
    spider(k, v)

# 关闭浏览器
dp.quit()