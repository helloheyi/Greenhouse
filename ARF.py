from ftplib import FTP
import sys, os
from os import path
sys.path.insert(0, path.expanduser('~/Documents/prometheus/ARF'))
#import tempfile
import numpy as np
import zipfile 
import pandas as pd
import smtplib 
from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart   

ftp = FTP()        
def ftp_Connect(host,username,password):
        # connect the FTP
        ftp.connect(host,21)
        # log in the FTP
        ftp.login(username, password)     
        return ftp


def downloadfile(ftp,file_char):
        files_name  = ftp.nlst()
        files_names= [x for x in files_name if file_char in x]
        names_list = []
        n = len(files_names)
        for jj in range(0, n):
                result = ''.join([i for i in files_names[jj] if  i.isdigit()])
                names_list.append(result)      

        name_num = max(list(map(int, names_list)))
        index = names_list.index(str(name_num))
        filename = files_names[index]
        # 'wb' File mode, write and binary
        ftp.retrbinary("RETR " + filename, open(filename, 'wb').write) 
        ftp.quit()     
        ftp.close()        
        return filename


def unzip(filename):
        zf = zipfile.ZipFile(filename)
        zf.extractall(path.expanduser('~/Documents/prometheus/ARF'))
        extract_file_name = filename.replace('d_9247_.zip','_D_9247_') 
        return extract_file_name


def clean_data(filename):
        data = pd.read_csv(filename)
        data = data.loc[:, ~data.columns.str.contains('Unnamed')]
        n = len(data)
        index = []
        for ii in range(0,n):
                if data.iat[ii, 0] =='*':
                        index.append(ii)
        table_name = []
        ## we only use table 3,5,7 
        num_table = np.array([2,4,6])
        num = len(num_table)
        for kk in range(0,num):
                table_name.append((data.loc[index[num_table[kk]*3]+1]).astype(str).values[0])
                title = data[index[num_table[kk]*3]+1:index[num_table[kk]*3+1]]    
                data_1 = data[index[num_table[kk]*3+1]+3:index[num_table[kk]*3+2]-1]    
                data_org_2 = []
                n_data_2 = len(data_1)
                for ii in range(0,n_data_2):
                        a = data_1.iat[ii, 0]
                        b = a.split("|")
                        data_org_2.append(b)
        
                data_org_2 =([list(x) for x in zip(*data_org_2)])
                m = len (title)
                if (n_data_2==0 or m==0):
                        continue
                table =pd.DataFrame({(title.iat[1, 0]):(data_org_2)[:][1]})
        
                for jj in range(2,m):
                        table.insert(0,(title.iat[jj, 0]),data_org_2[:][jj])
                table.to_csv(table_name[kk]+'.csv')   
        
        
        Sec  = pd.read_csv(table_name[0]+'.csv')
        Sec = Sec.loc[:,['# 18 ISO Currency Symbol of Price prev price_ISO_curr_symbol_prev     S   3  0','# 10 ISO Country Symbol                ISO_country_symbol             S   2  0','#  3 MSCI Security Code                msci_security_code             N   7  0']]
        Sec= Sec.rename(index=str,columns= {'#  3 MSCI Security Code                msci_security_code             N   7  0' :'MSCI Security Code'})
        
                # choose data we need 
        Sec_Consitit = pd.read_csv(table_name[1]+'.csv')
        Sec_Consitit = Sec_Consitit.loc[:,['# 11 Closing weight in percentage      closing_weight                 N  18 13','#  4 MSCI Security Code                msci_security_code             N   7  0','#  3 MSCI Index Code                   msci_index_code                N   6  0']]
        Sec_Consitit= Sec_Consitit.rename(index=str,columns= {'#  4 MSCI Security Code                msci_security_code             N   7  0' :'MSCI Security Code'})
        Sec_Consitit['allocation'] = Sec_Consitit.apply(lambda row:(row['# 11 Closing weight in percentage      closing_weight                 N  18 13'])/100,axis=1)
                #print(Sec_Consitit)
        
        Sec_Code = pd.read_csv(table_name[2]+'.csv')
        Sec_Code = Sec_Code.loc[:,['# 13 MIC                               mic                            S   5  0','# 11 Security Ticker                   bb_ticker                      S  20  0','#  9 Isin                              isin                           S  12  0','#  3 Security Name                     security_name                  S  25  0','#  4 MSCI Security Code                msci_security_code             N   7  0']]
        Sec_Code = Sec_Code.drop_duplicates(subset=['#  4 MSCI Security Code                msci_security_code             N   7  0'])
        Sec_Code = Sec_Code.reset_index(drop=True)
        Sec_Code = Sec_Code.rename(index=str,columns= {'#  4 MSCI Security Code                msci_security_code             N   7  0' :'MSCI Security Code'})
        S =  pd.merge(Sec,Sec_Code,on = 'MSCI Security Code')
        S['asset_type'] ='Stock'
        num_asset = len(S['asset_type'])
        print(num_asset)
        asset_class = []
        symbol = []
        
        for hh in range(0,num_asset):
                ticket_name = (S.iloc[hh]['# 11 Security Ticker                   bb_ticker                      S  20  0'])
                symb = (ticket_name.split(" "))[1]
                symbol.append(symb)                
                if ((S.iloc[hh]['# 10 ISO Country Symbol                ISO_country_symbol             S   2  0']).strip()=='CA'):
                        asset_class.append('canadian_stocks') 
                        continue
                if ((S.iloc[hh]['# 10 ISO Country Symbol                ISO_country_symbol             S   2  0']).strip()=='US'):
                        asset_class.append('us_stocks') 
                        continue
                if ((S.iloc[hh]['# 10 ISO Country Symbol                ISO_country_symbol             S   2  0']).strip()=='JP'):     
                        asset_class.append('japar_stocks')
                        continue
                if ((S.iloc[hh]['# 10 ISO Country Symbol                ISO_country_symbol             S   2  0']).strip()=='CN'):     
                        asset_class.append('asia_stocks')  
                        continue
                else:
                        asset_class.append('eu_stocks')  
                        continue
             
                
        asset_class = pd.DataFrame({'asset_class':asset_class,'symbol':symbol})
        S = pd.concat([S,asset_class], axis=1)
        US = Sec_Consitit[Sec_Consitit['#  3 MSCI Index Code                   msci_index_code                N   6  0']==714812]
        
        US = pd.merge(US,S,on = 'MSCI Security Code')
        US.to_csv('US.csv')  
        
        CA = Sec_Consitit[Sec_Consitit['#  3 MSCI Index Code                   msci_index_code                N   6  0'] !=714812]
        CA = CA.reset_index(drop=True)
        CA = pd.merge(CA,S,on = 'MSCI Security Code')
        CA.to_csv('CA.csv') 
        for jj in range(0,3):
                os.remove((table_name[jj]+'.csv'))
               
def send_email(user,password,filename):
        msg = MIMEMultipart('mixed')
        msg['From'] = user
        msg['To'] = 'yihe8258@gmail.com'
        msg['Cc'] = 'yhe38095@gmail.com'
        msg['Subject'] = 'Halal Portfolio Rebalanced '
        sendfile=open('US.csv','rb').read()
        text_att = MIMEText(sendfile, 'base64', 'utf-8')    
        text_att["Content-Type"] = 'application/octet-stream'  
        text_att["Content-Disposition"] = 'attachment; filename="US.csv"'
        msg.attach(text_att)
        #body = MIMEText('Do you love me? \n'+'Yes you do')
        body = MIMEText('Please see the attach')
        msg.attach(body)
        sendfile=open('CA.csv','rb').read()
        text_att_1 = MIMEText(sendfile, 'base64', 'utf-8')    
        text_att_1["Content-Type"] = 'application/octet-stream'  
        #text_att_1["Content-Disposition"] = 'attachment; filename="filename[:-4]"+"CA.csv"'
        text_att_1["Content-Disposition"] = 'attachment; filename="CA.csv"'
        msg.attach(text_att_1)
        server = smtplib.SMTP('smtp.gmail.com',587)
        ##check status
        #print(server.set_debuglevel(1))
        server.ehlo()
        server.starttls()
        server.login(user, password)
        server.sendmail(msg['From'], msg['To'].split(',') + msg['Cc'].split(','),msg.as_string())
        server.quit() 
if __name__ == "__main__":
                ftp = ftp_Connect("ftp2.msci.com", 'xzmdmrpn','L5ycqptp')
                filename = downloadfile(ftp, '9247')
                extract_file_name = unzip(filename)
                data = pd.read_csv(extract_file_name, header = None)
                data.to_csv('Halal_'+filename[0:8]+'.csv')
                clean_data('Halal_'+filename[0:8]+'.csv')
                send_email('yhe@wealthsimple.com', 'Again8258','Halal_'+filename[0:8]+'.csv')
                file = [filename,extract_file_name,'CA.csv','US.csv','Halal_'+filename[0:8]+'.csv']
                n = len(file)
                for kk in range(0,n):
                        os.remove(file[kk])                
             
        