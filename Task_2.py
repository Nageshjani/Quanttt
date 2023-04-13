import requests
import json
import pandas as pd

#BASE_URL=https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY

def OptionChain(symbol,expiryDate):

        url='https://www.nseindia.com/api/option-chain-indices?symbol='+symbol
        headers = {'accept':'*/*',
                'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36',
                'Referer': url,
                'X-Requested-With': 'XMLHttpRequest'
                }

        res=requests.get(url,headers=headers)
        JsonData=json.loads(res.text)
        dataList=JsonData['records']['data']
        frames=[]
        for l in dataList:
            if l['expiryDate']==expiryDate:

                for key in l:
                    if key=='CE':
                        df1=pd.DataFrame(l[key],index=[0])
                        df1['TYPE']='CE'
                        
                    
                    if key=='PE':
                        df2=pd.DataFrame(l[key],index=[0])
                        df2['TYPE']='PE'
                        
     
                df=pd.concat([df1,df2])
                frames.append(df)

                

                    
        df=pd.concat(frames)
        cols = list(df.columns)
        cols = [cols[-1]] + cols[:-1]
        df = df[cols]
        df.set_index('expiryDate')
        df.to_csv('NIFTY__20_APR.csv')
                
            

OptionChain('BANKNIFTY',"20-Apr-2023")



