import logging
import time
import traceback

import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header


#配置邮件服务器用以邮件通知
def sendMail(result):
    mail_host = "smtp.126.com"  # 设置服务器
    mail_user = "xxxx@126.com"  # 用户名
    mail_pass = "xxxx"  # 口令

    sender = 'xxxx@126.com'
    receivers = ['xxxxx@qq.com','1xxxxxx5@qq.com']

    message = MIMEText(result, 'plain', 'utf-8')
    message['from'] = 'xxxxxx@126.com'
    message['to'] = 'xxxxxxxx0@qq.com'
    message['subject']='pmp监控'
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


def sendDATA():

    try:
        header={
        'Authorization':'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjUwQTQ0RDY3RUFBRDc3MjQyOTNBNTVGMEExOEExRjcxOUY4M0RFMjciLCJ0eXAiOiJhdCtqd3QiLCJjdHkiOiJKV1QiLCJ4NXQiOiJVS1JOWi1xdGR5UXBPbFh3b1lvZmNaLUQzaWMifQ.eyJuYmYiOjE2NjQxOTQ0NDUsImV4cCI6MTY2NDE5ODA0NSwiaXNzIjoiaHR0cHM6Ly9pZHAucG1pLm9yZyIsImF1ZCI6WyJjZXJ0LXByb2ZpbGUtYXBpIiwiY2VydC1hcHBsaWNhdGlvbi1hcGkiLCJteXBtaS1hcHBsaWNhdGlvbi1hcGkiLCJuYXZpZ2F0b3ItYXBwbGljYXRpb24tYXBpIl0sImNsaWVudF9pZCI6InNpdGVjb3JlX2NmOGVmY2JhMGU1MjQ4MDI5ZWI2OTcyMDk1OWFkOWY1IiwiYXV0aF90aW1lIjoxNjY0MTk0Mzg3LCJpZHAiOiJsb2NhbCIsInN1YiI6IjEzNDM5MDIzMTVAcXEuY29tIiwibmFtZSI6IjEzNDM5MDIzMTVAcXEuY29tIiwiaWQiOiI4MzUxNDMxIiwicGVyc29uX2lkIjoiODM1MTQzMSIsImdpdmVuX25hbWUiOiJGdXJvbmciLCJmYW1pbHlfbmFtZSI6IkN1aSIsImVtYWlsIjoiMTM0MzkwMjMxNUBxcS5jb20iLCJjb21wYW55IjoiSGFuZ3pob3UgTW8gYW4gVGVjaG5vbG9neSBDby4gTFREIiwiaXNfZWxjIjoiRmFsc2UiLCJpc19tZW1iZXIiOiJOb25lIiwiZXh0cGlkIjoiZGU0MjA3NmYtM2M0My00ZjYyLTg4NWMtYWEzY2FmMDE2ZGY4IiwiaXNQTVAiOiJmYWxzZSIsIm1lbXR5cGUiOiJOb25lIiwic2VnbWVudCI6Ik5leHQgR2VuIiwic2NvcGUiOlsib3BlbmlkIiwicHJvZmlsZSIsImVtYWlsIiwiQ0VSVFBST0ZJTEVBUEkiLCJDRVJUQVBJIiwiTVlQTUlBUFBBUEkiLCJOQVZBUFBBUEkiXSwiYW1yIjpbInB3ZCJdfQ.PBcX4SQv_R98ldeqyMxFNV1PTKth9v6uSZAw2w3K-k3S44KFVCaRFXpWV1T-wLa6MyiQsb6yt-v80eLQhVAalxUDU16XPqkPa6zK0xDl2p_DEOU6aGv4DX3ARjrf7SMcH4LO9U36S8yRwjW3DSO9NSsSFK2cgMWxXov9Fm3jobAxQp-q-t36Ok0_YK8lV2gIOGMtPE7MqmXCZaHry7ht5rs_r9AiQxikC4ShQRr6RntM5GAxoE__R4dud0aW7jheYIsRJPf8girlzcUFS80bPo_xUZq0vWRF5XDN2YylB4XrK9x6oN1AYad5d-KHxoXO37inkn-vGQupTeI0yaoTaA'}
        r = requests.get('https://mypmi-api.pmi.org/certifications/applications',headers=header)
        status = (r.json()['data'][0]['status'])
        info=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+" : "+'当前报名状态为'+str(status)
        print(info)
        if(status=='Submitted'):
            return "success",info
    except Exception as es:
        traceback.print_exc()
        info= traceback.format_exc()
        print(info)

        return "error",info

#此处添加返回包的判断逻辑


if __name__ == '__main__':
    while 1:
        status,info= sendDATA()
        if (status=='error'):
            sendMail(info)
            break
        elif(info.find('Submitted')==-1):
            sendMail(info)
        time.sleep(45)
