from requests import Session
import json
import pyotp


TOTPKEY=''
ZERODHA_USERID=''
ZERODHA_PASSWORD=''

twofa=pyotp.TOTP(TOTPKEY).now()
#Initiating The Session
s = Session()
base_url = "https://kite.zerodha.com/"
r = s.get(base_url)
print(s.cookies)

#Fetching Request Id Using Username/Password
login_url = "https://kite.zerodha.com/api/login"
r = s.post(login_url, data={"user_id": ZERODHA_USERID, "password":ZERODHA_PASSWORD})
j = json.loads(r.text)
print(j)

#Finnlay Logged In
twofa_url = "https://kite.zerodha.com/api/twofa"
data = {"user_id": ZERODHA_USERID, "request_id": j['data']["request_id"], "twofa_value": twofa }
r = s.post(twofa_url, data=data)
j = json.loads(r.text)
print(j)



if  s.cookies["enctoken"]:
    print("Logged in")
else:
    print("Not logged in")
