#-*-coding:utf-8-*-
import asyncio
from pyppeteer import launch
import random

async def main():
    browser = await launch(
        #参数有很多,推举几个常用的
        {'headless': False, # 无头
         'dumpio':True, # stdout and stderr 是否放入pipe
         'autoClose': False,  # script 渲染完成后自动关系浏览器
         'args':['--no-sandbox', #浏览器无限制
                 '--disable-infobars', #隐藏正在受到自动软件的控制
                 # '--proxy-server={}'.format(proxy), #可放入代理!!!
                 ],
         }
    )
    page = await browser.newPage() #开启页面
    await page.setViewport({"width": 1366, 'height': 800}) #设置页码大小
    await page.setJavaScriptEnabled(enabled=True) #是否开启JS
    await page.setUserAgent('Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36') #自定义ua
    try:
        # res=await page.goto(url='https://ip.cn/', options={"timeout":10000})
        res=await page.goto('https://www.baidu.com', options={"timeout":10000}) #10秒超时
        await asyncio.sleep(2)  # 异步等待
        # 在搜索框中输入python
        await page.type('input#kw.s_ipt', 'Python成功之路', {'delay': random.randint(100, 151) - 50}) #随机输入延迟
        # 点击搜索按钮
        await page.click('input#su')
        await page.evaluate('window.scrollBy(0, window.innerHeight)')  # 滚动到页面底部

        # Pyppeteer 三种解析方式
        """
        Page.querySelector()  # 选择器
        Page.querySelectorAll()
        Page.xpath()  # xpath  表达式
        # 简写方式为：
        Page.J(), Page.JJ(), and Page.Jx()
        """

        #XPATH 使用
        '''
        title_elements = await page.xpath('//h3[contains(@class,"t")]/a')   #圈定元素
        for item in title_elements:
            title_str = await (await item.getProperty('textContent')).jsonValue()
            print(title_str)
        '''
        # slider = await page.Jeval('#nocaptcha', 'node => node.style')  # 判断是否有滑块


        print(res.status)  # 响应状态
        print(res.headers)  # 响应头
        print(await page.cookies()) #打印页面cookie
        print(await page.content()) #打印页面文本
        print(await page.title()) # 打印当前页标题
        await page.screenshot({'path': 'pic.png'})  # 截屏幕保存
        await page.pdf(path='test_pdf.pdf') #保存为pdf

        # 在网页上执行js 脚本
        # dimensions = await page.evaluate(pageFunction='''() => {
        #         return {
        #             width: document.documentElement.clientWidth,    // 页面宽度
        #             height: document.documentElement.clientHeight,  // 页面高度
        #             deviceScaleFactor: window.devicePixelRatio,     // 像素比 1.0000000149011612
        #         }
        #     }''', force_expr=False)  # force_expr=False  执行的是函数
        # print(dimensions)
        # content = await page.evaluate(pageFunction='document.body.textContent', force_expr=True) #  只获取文本  执行 js 脚本  force_expr  为 True 则执行的是表达式



        #iframe时
        '''
        await asyncio.sleep(1)
        frame = page.frames
        print(frame)  # 需要找到是哪一个 frame
        title = await frame[1].title()
        print(title)
        await asyncio.sleep(1)
        login = await frame[1].querySelector('#switcher_plogin')
        print(login)
        await login.click()
        '''
        await asyncio.sleep(2)  # 异步等待
        # return res
    except Exception as e:
        print(e)
    await page_close(browser)

async def page_close(browser): #关闭浏览器
    for _page in await browser.pages():
        await _page.close()
    await browser.close()


#执行任务:
if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())   #启动单个任务

#启动多个任务
'''
if __name__ == '__main__':
    url_list = [
        "http://www.baidu.com",
        "https://wap.huaqianapp.com/m/news/detail?id=17201398",
        "https://www.qq.com",
    ]
    task = [main(url) for url in url_list]

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(*task))
    for res in results:
        print(res)
'''
