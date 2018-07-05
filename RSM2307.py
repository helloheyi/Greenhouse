import pandas as pd
import numpy as np
import statsmodels.api as sm
from sklearn import linear_model
import datetime
import matplotlib.pyplot as plt
from dateutil.relativedelta import*
from datetime import*
from copy import deepcopy



df_C = pd.read_csv("Call.csv",index_col=[2],parse_dates = True)
df_P = pd.read_csv("Put.csv",index_col=[2],parse_dates = True)


# # Create dictionary
d_C = {}
d_P = {}
for ii in range(0,9):
    d_C["df_delta_{0}".format(ii+1)]=df_C.loc[(df_C[:]['delta']>= (ii*0.1+0.05))&(df_C[:]['delta'])<(ii*0.1+0.15)] 
    d_P["df_deltaP_{0}".format(ii+1)]= df_P.loc[(df_P[:]['delta']>=(ii*0.1-0.95))&(df_P[:]['delta']<(ii*0.1-0.85))]
    


# # Descriptive Statistics:
def stat(data):
    df_name = ['spx_level','strike_price','impl_volatility']
    mean_value = []
    std_value = [] 
    for jj in range(0,len(df_name)):
            mean_value.append((data[:][df_name[jj]]).mean())
            std_value.append((data[:][df_name[jj]]).std())
    return mean_value,std_value


stat_C = []
stat_P = []
for ii in range(0,9):
    dfC_value = df_C.loc[(df_C[:]['delta']>=(ii*0.1+0.05))&(df_C[:]['delta']<(ii*0.1+0.15))]
    dfP_value = df_P.loc[(df_P[:]['delta']>=(ii*0.1-0.95))&(df_P[:]['delta']<(ii*0.1-0.85))] 
    stat_C.append(stat(dfC_value))
    stat_P.append(stat(dfP_value))


# # Gain Function:

def Gain(data,is_Call=True):
    
    # find sse of mv 
    delta_M = data[:]['delta_f'] - data[:]['delta_s']* data[:]['delta']
    x_1 = data[:]['vega']*data[:]['delta_s']/(data[:]['spx_level']*np.sqrt(data[:]['modT']))
    x_2 = data[:]['delta']*x_1
    x_3 = x_2*data[:]['delta']
    df_1 = pd.DataFrame({'y':delta_M,'x_1':x_1,'x_2':x_2,'x_3':x_3})
    x = df_1.iloc[:,0:3]
    x = sm.add_constant(x)
    model = sm.OLS(df_1[:]['y'],x).fit()
    params = model.params
    error_bs = data[:]['delta_f'] - data[:]['delta_s']*data[:]['delta']
    SSE_BS = sum(np.square(error_bs-error_bs.mean()))   
    error_MV= error_bs - (params[0]+params[1]*x_1+params[2]*x_2+params[3]*x_3)
    SSE_MV = sum(np.square(error_MV-error_MV.mean()))
    Gain_Total = (1- SSE_MV/SSE_BS)    
    Gain_name = ['delta_1','delta_2','delta_3','delta_4','delta_5','delta_6','delta_7','delta_8','delta_9']  
    Gain = pd.DataFrame({'Total':[Gain_Total]})
    
    for ii in range(0,9):
        if is_Call:
            sub_df = data.loc[(data[:]['delta']>=(ii*0.1+0.05))&(data[:]['delta']<(ii*0.1+0.15))]
        else:
            sub_df = data.loc[(data[:]['delta']>=(ii*0.1-0.95))&(data[:]['delta']<(ii*0.1-0.85))]    
        
        ## find error_bs
        error_bs = sub_df[:]['delta_f'] - sub_df[:]['delta_s']*sub_df[:]['delta']
        SSE_BS = sum(np.square(error_bs-error_bs.mean()))   
        
        ### 
        new_x_1 = sub_df[:]['vega']*sub_df[:]['delta_s']/(sub_df[:]['spx_level']*np.sqrt(sub_df[:]['modT']))
        new_x_2 = sub_df[:]['delta']*new_x_1
        new_x_3 = new_x_2*sub_df[:]['delta']        
        error_MV= error_bs - (params[0]+params[1]*new_x_1+params[2]*new_x_2+params[3]*new_x_3)
        SSE_MV = sum(np.square(error_MV-error_MV.mean()))
        result = pd.DataFrame({Gain_name[ii]:[1- SSE_MV/SSE_BS]})
        Gain = pd.concat([Gain,result],axis=1)
    # find sse of bs
    params = pd.DataFrame({'con':[params[0]],'x_1':[params[1]],'x_2':params[2],'x_3':params[3]})
    return [Gain,params]




def Plot_f(x,y,title):
    plt.plot(x,y,'mo:')
    plt.ylabel('Gain')
    plt.xlabel('delta')
    plt.title(title)
    plt.show()


# In[9]:


result_C = pd.DataFrame()
result_para_C = pd.DataFrame()
result_P = pd.DataFrame()
result_para_P = pd.DataFrame()

total_months= relativedelta(df_C.index[-1],df_C.index[0]).years*12 + relativedelta(df_C.index[-1],df_C.index[0]).months-36
index = []
for ii in range(0,total_months):
    # Call
    #Gain Function
    df_C_3 = df_C.loc[(df_C.index[0]+relativedelta(months=+ii)):(df_C.index[0]+relativedelta(months=+ii) + relativedelta(months=+36))]    
    index.append((df_C.index[0]+relativedelta(months=+ii)))
    result = Gain(df_C_3,is_Call=True)  
    result_C = pd.concat([result_C,(result[0])],ignore_index=True)
    result_para_C = pd.concat([result_para_C,(result[1])],ignore_index=True)
    
    # Put 
    #Gain Function
    df_P_3 = df_P.loc[(df_P.index[0]+relativedelta(months=+ii)):(df_P.index[0]+relativedelta(months=+ii) + relativedelta(months=+36))]    
    result = Gain(df_P_3,is_Call=False)  
    result_P = pd.concat([result_P,(result[0])],ignore_index=True)
    result_para_P = pd.concat([result_para_P,(result[1])],ignore_index=True)

    

