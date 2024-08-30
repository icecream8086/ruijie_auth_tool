import requests
import os

# 如果输入失败，可能是字符编码问题
# 使用浏览器开发者工具观察http://10.10.10.52/eportal/InterFace.do?method=login的表单信息
# eportal_server为网络服务提供商，名称编码格式必须为URL编码

user = ""
password = ""
user_group = "%E5%AD%A6%E7%94%9F%E7%BB%84"
eportal_server = "%e7%a7%bb%e5%8a%a8%e4%ba%92%e8%81%94%e7%bd%91%e6%9c%8d%e5%8a%a1"


# # 检查登录后的ip 无法确认是否登录成功
# info = str(os.popen(
#     'ipconfig | find "IPv4 Address. . . . . . . . . . . : 10."').readlines())
# if 'IPv4 Address. . . . . . . . . . . : 10.' in info:
#     print("已连接到网络")
# else:
#     print("未连接至网络,尝试连接至目标网络")


# 检测是否有网，如果有，则不执行后续操作，如果没有，则执行校园网连接
# # win32_cmd
putout = str(os.popen('ping baidu.com | find "timed out."').readline())

# pwsh_7
# putout = str(os.popen('ping baidu.com | Select-String "time out"').readlines())

if 'timed out.' not in putout and 'Ping request could not find' not in putout:
    print("已连接到网络")
# elif 'Ping request could not find' not in putout:
#     print("尝试解析域名baidu.com失败,此网络可能无法联网，需要进一步进行调试")
else:
    geturl1 = "http://172.168.100.21/"
    session = requests.session()
    session.get(geturl1)
    html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
    send_cookie = session.cookies['JSESSIONID']

# 这里应该是跳转到认证服务器上，表明自己的学生身份
    geturl2 = "http://172.168.100.21/eportal/redirectortosuccess.jsp"
    get2_header = {
        "EPORTAL_USER_GROUP": user_group,
        "JSESSIONID": send_cookie
    }
    responseRes = requests.get(geturl2,  headers=get2_header)

# 然后就会被重定向到[url=http://123.123.123.123/]http://123.123.123.123/[/url],并且获取当前的AP的各种消息（query_string）

    geturl3 = "http://123.123.123.123/"
    back = requests.get(geturl3)
    query_string = back.text
    st = query_string.find("index.jsp?") + 10
    end = query_string.find("'</script>")
    query_string = query_string[st:end]

# 接下来就是post登录请求了
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36 Edg/89.0.774.54"
    posturl = "http://172.168.100.21/eportal/InterFace.do?method=login"

    post_header = {
        "Host": "172.168.100.21",
        "Connection": "keep-alive",
        "Content-Length": "926",
        "Origin": "172.168.100.21",
        'User-Agent': userAgent,
        "EPORTAL_COOKIE_USERNAME": user,
        "EPORTAL_COOKIE_PASSWORD": password,
        "EPORTAL_COOKIE_SERVER": eportal_server,
        "EPORTAL_COOKIE_SERVER_NAME": eportal_server,
        "JSESSIONID": send_cookie,
        "EPORTAL_USER_GROUP": user_group
    }

    post_data = {
        "userId": user,
        "password": password,
        "service": eportal_server,
        "queryString": query_string,
        "operatorPwd": "",
        "operatorUserId": "",
        "validcode": "",
        "passwordEncrypt": "false"

    }

    responseRes = requests.post(posturl, data=post_data, headers=post_header)
    responseRes.encoding = "utf-8"
    Thankyou = responseRes.json()
    if Thankyou["result"] == "success":
        print("理论上登录成功了")
    else:
        print("没有登录成功，可能存在某些异常,请手动排查")



# 用于检测是否登录成功

# Used to detect whether the login is successful

