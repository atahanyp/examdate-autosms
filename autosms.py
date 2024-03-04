import pandas as pd
import os
from netgsm import SmsService

kursiyers = {}

with open("sinavsaat.txt", "r",encoding="utf-8") as f:
    
    icerik = f.readlines()
    ilkisim=[]
    ilktc=[]
    ilksaat=[]
    sertifika=[]
    for satir in icerik:
        
        list1 = []
        isimsoy=[]
        adson=""
        sonsinav=""
        list1= satir.split(" ")
        isimsoy = list1[3:-4]
        kursiyers[list1[2]] = []
        
        ilktc.append(list1[2])
        
        sertifika.append(list1[-4])
        
        for b in isimsoy:
            
            adson= adson + b + " "                         
        
                          
        saat=list1[-3:]                                      
        ilkisim.append(adson)
        for c in saat:
            
            c = c.replace("\n","")
            sonsinav=sonsinav+ c+ " "
        ilksaat.append(sonsinav)
      
    df=pd.DataFrame({"Tc" :ilktc,"İsim soyisim": ilkisim,"Sertifika Türü":sertifika, "Direksiyon Sinav Saati": ilksaat, "GSM" : None, "E sinav tarihi" : None})
    
    
    path = os.path.dirname(__file__)
    
    newPath = path.replace(os.sep, '/')
    
    kursiyerler = pd.read_excel( newPath +'/kursiyerlistesitum.xls')
    
    uzunluk = kursiyerler.shape[0]

    soz2={}
    
    for i in range(uzunluk):    
        
        tumtc= str(kursiyerler["TC KİMLİK"][i])
        tumgsm = str(kursiyerler["GSM1"][i])
        tumgsm=tumgsm.replace(".0","")
        
        if kursiyerler["TC KİMLİK"][i]== "":
            continue            
        
        elif pd.isna(kursiyerler["GSM1"][i])== True:
            soz2[str(kursiyerler["TC KİMLİK"][i])] = "------"
            print("aaaa")
            continue
        
        soz2[str(kursiyerler["TC KİMLİK"][i])] = str(kursiyerler["GSM1"][i]).replace(".0","")
        
    
    tcs=df["Tc"]
    tcs=list(tcs)
    print(tcs)


    for c in soz2:
        if c in tcs:

            df.loc[df[df["Tc"]==c].index.values,"GSM"]=soz2[c]

    df.to_csv('file_name.csv')   

    print(df)

with open("sms.txt","r+",encoding="utf-8") as g:
    text=g.read()
    
    for e in range(df.shape[0]):
        
        
        text2 = text.replace("________",df.iloc[e]["İsim soyisim"])
        
        text2 = text2.replace("--------",df.iloc[e]["Direksiyon Sinav Saati"])
        


        kwargs = {
        # you can also set user code from environment.
            'user_code': 'net gsm user code', # Default value : None
        # you can also set user password from environment.
            'user_password': 'net gsm user password',  # Default value : None
            'api_url': 'net gsm api url'  # Default value : 'https://api.netgsm.com.tr/sms/send/get'
        }
        sms_service = SmsService(**kwargs)
        sms_service.send_sms(phone=df.iloc[e]["GSM"], message=text2, header='SURUCU KURSU')
        # header default value : None if you don't pass this value your header is your user code