<div align="center">
<h1 align="center">NJU宿舍低电量提醒器</h1>
</div>

## 简介

每天定时自动查询宿舍电量，低电量提醒！！！

如想修改定时运行的时间，可修改 `.github/workflows/nju-electricity-reminder.yml` 中 `schedule` 属性。

## Github Actions 启用步骤

### 1. Fork 本项目

Fork 本项目: [actions-nju-electricity-reminder](https://github.com/zhangt2333/actions-nju-electricity-reminder) (Star 自然是更好)

### 2. 准备需要的参数

* 模板：
    ```json
    {
        "username": "学号",
        "password": "自己的统一认证密码",
        "threshold": 阈值，即电量低于多少需要警报
    }
    ```

* 样例：
    ```json
    {
        "username": "123456",
        "password": "abcdefg",
        "threshold": 30.00
    }
    ```
* 样例解释：
    * 学号为 `123456`
    * 密码为 `abcdefg`
    * 电量低于30.00将报警发邮件给用户

### 3. 启用 Github Actions

![image-20210216140844300](README/image-20210216140844300.png)

### 4. 将参数填到 Secrets

将填好的参数加入到 Secrets 中：其中 name 为 `DATA`，value 为步骤 2 中填好的多行字符串

![image-20210216140557947](README/image-20210216140557947.png)

### 5. 配置自己账号的邮件提醒

如下图正确配置，这样运行失败的 Github Actions 事件会自动邮件通知你
![](README/img5.png)
