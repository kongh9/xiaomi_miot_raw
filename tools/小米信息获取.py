try:
    import aiohttp
except ModuleNotFoundError:
    input("需要安装 aiohttp，请运行: pip install aiohttp")
from aiohttp import ClientSession
import getpass
try:
    from xiaomi_cloud import *
except ImportError:
    input("需要“xiaomi_cloud.py”文件，请确保文件夹内容完整！")
    
async def login(username: str, password: str):
    async with aiohttp.ClientSession() as cs:
        mc = MiCloud(cs)
        if await mc.login(username, password):
            print("以下是登录信息，请保存下来\n注意！拥有此信息即拥有小米账号的所有权限，请勿泄露！")
            # print (mc.auth)
            print(f"userId: '{mc.auth['user_id']}'")
            print(f"ssecurity: '{mc.auth['ssecurity']}'")
            print(f"serviceToken: '{mc.auth['service_token']}'")
            input("按回车键读取名下所有设备")
            devices_list = await mc.get_devices("cn")
            # print(devices_list)
            parse_device_list(devices_list)
        else:
            print("登录失败")
            # return None
        
    
def parse_device_list(devices_list: list):
    SHOW_LIST=[('did','did'),
               ('model','model'),
               ('IP','localip'),
               ('token','token'),
              ]
    for idx, d in enumerate(devices_list):
        desc = f"({d['desc']})" if d['desc'] else ""
        print(f"{idx}. {d['name']} {desc}")
        for key, value in SHOW_LIST:
            print(f"   {key}: {d[value]}")
if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    user = input("请输入小米账号: ")
    pwd = getpass.getpass("请输入密码(输入时不显示): ")
    tasks = [login(user, pwd)]
    results = event_loop.run_until_complete(asyncio.gather(*tasks))
    # print(results)
    input("按回车键退出...")