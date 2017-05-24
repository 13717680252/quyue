import smtplib  # 加载smtplib模块
from email.mime.text import MIMEText
from email.utils import formataddr
from flask import url_for
from flask import render_template
my_sender = '13717680252@163.com'  # 发件人邮箱账号，为了后面易于维护，所以写成了变量
my_user = '1271369334@qq.com'  # 收件人邮箱账号，为了后面易于维护，所以写成了变量
from itsdangerous import URLSafeTimedSerializer


def generate_confirmation_token(email):
 serializer = URLSafeTimedSerializer('hos950928')
 return serializer.dumps(email, salt='my_precious_two')

def confirm_token(token, expiration=3600):
 serializer = URLSafeTimedSerializer('hos950928')
 try:
  email = serializer.loads(token,salt='my_precious_two',max_age=expiration)
 except:
  return False
 return email



def mail(userid,receiver):
    ret = True
    tk = generate_confirmation_token(receiver)
    confirm_url = url_for('vcommon.activate', token=tk,_external=True)
    html = render_template('test.html', confirm_url=confirm_url)
    try:
        mail_msg = """
       <p>Python 邮件发送测试...</p>
       <p><a href="http://www.runoob.com">这是一个链接</a></p>
       """
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = formataddr(["去约团队", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["尊敬的用户", receiver])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "主题"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP("smtp.163.com", 25)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, "hos950928")  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail("from@hos.com", [receiver], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 这句是关闭连接的意思
    except Exception:  # 如果try中的语句没有执行，则会执行下面的ret=False
        ret = False
    print(ret)
    return ret


