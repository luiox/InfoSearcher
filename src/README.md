# wechat_subscription

微信公众号模拟登陆
目标网址: https://mp.weixin.qq.com/

## 声明此代码仅供技术交流学习，擅自用于其他，一切后果与本人无关

```
# 简单环境 由于我这个直接用的本地环境，导致很多依赖,所以requirements.txt太多了
Python3.6+ 
Flask==1.0.2  
Pillow==6.1.0
qiniu   # 七牛云上传sdk
```

如果对你有帮助的话，可以点击star 🌈
对应博客

简单的说一下运行逻辑。

- 1 首先是模拟表单发送一个post请求， 注意密码是md5之后的值
- 2 模拟请求后可能出现验证码，如果有就请求验证码，(验证码url会携带登陆cookie)，然后手动输入重新post
- 3 跳转到扫描二维码界面，这会就有两个逻辑，第一个是账号持有人扫码，第二个是非账号持有人。
    - 3.1账号持有人扫码，扫完就直接登陆确认。
    - 3.2 非账号持有人，扫完后，会继续跳转到账号本人扫码界面(貌似账号本人微信会直接提示，直接确认就行)
- 4 直接访问主页，获取token，然后把现在自身的cookie保存，模拟登陆到此就完成了。

--------------------- 

# Run

> 我省时间就直接写在一个.py文件里面，flask项目工程文件结构可参考我另一个项目：https://github.com/wgPython/Fantastic

```

> python3 app.py

```

# idea:

- [x] 封装成API接口，可以管理多个公众号，避免每天重复登陆。
- [x] 获取当前公众号的历史文章，点赞阅读，粉丝信息，账户信息等等。

#### 封装成api接口

- 1 登陆接口

```
POST  /login

params:
    username  {str}  
    password  {str}
    
return:
    {"code": 0, "msg": "请尽快扫描验证码!有效时间5分钟", "QrCode": "二维码链接", "source_name": source_name}

``` 

- 2 获取邮箱信息

```
POST /get/history/email
params:
    username {str}
return:
    微信原始接口信息    
```

- 3 获取历史文章，以及在看阅读数

```
POST /get/history/article
params:
    username {str}
return:
    article_data = {
        "code": 0,
        "history_article": 微信文章信息,
        "article_other_info": 微信在看阅读,
    }
```

- 4 获取关注用户男女比例

```
POST /get/fans/sex/ratio
params:
    username {str}
return:
    {"code": 0, "msg": "OK", "male": "数量", "female": "数量"}

```

- 5 获取账号信息

```
POST /get/public/account/info
params:
    username {str}
return:
       {"code": 0, 
       "msg": "OK", 
       "account_info":
        "public_account_image": 头像链接,
        "public_account_name": 名称,
        "wechat_account": 微信号,
        "public_account_type": 类型,
        "public_account_desc": 描述,
        "public_account_auth": 认证情况,
        "public_account_address": 所在地址,
        "public_account_body": 主体信息,
        "login_email": 登陆邮箱,
        "source_id": 原始ID,
       }
```



