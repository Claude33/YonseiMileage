#!/usr/bin/env python
# coding: utf-8

# In[130]:


def delete_column(data, column):
    ''' data: 데이터 프레임 이름, column: 변수 이름(string type으로 입력)
        원하는 컬럼 제거 후 리턴
    '''
    result = data.drop(columns=[column])
    return result

def to_category(data, column):
    ''' 선택한 컬럼의 변수 타입을 카테고리 타입으로 변경
        data = 데이터프레임, column = 컬럼
    '''
    result = data.astype({column:'category'})
    return result

def combine_category(data, column, before, after):
    ''' 한 컬럼 내의 특정 카테고리들 합치기
        data = 데이터셋(pd.DataFrame), column = 선택할 컬럼(string),
        before = 합칠 카테고리들(list),  after = 합치고 난 후의 클래스 이름(string)
    '''
    num_of_classes = len(before)
    l_after = []
    
    for i in range(num_of_classes):
        l_after.append(after)
        
    answer = data[column].replace(before, l_after)
    data[column] = answer
    
    return data


# # 연세대학교 마일리지 예측모델

# In[1]:


get_ipython().run_line_magic('matplotlib', 'inline')


import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import font_manager, rc
from matplotlib import style

import seaborn as sns
import random


# In[22]:


import pandas_profiling
# 컬럼 갯수 무제한으로
pd.set_option('display.max_columns', None)


# ### 데이터 가져오기

# In[29]:


# 인덱스가 없음으로 'index_col=False' 추가
data1 = pd.read_csv('/Users/appdesign490/Desktop/YBIGTA/ScienceTeam/MiniP/final/yonseimileage_2019_1.csv', encoding='euc-kr', index_col=False)
data1.head()


# In[30]:


data1.describe()


# In[31]:


data2 = pd.read_csv('/Users/appdesign490/Desktop/YBIGTA/ScienceTeam/MiniP/final/yonseimileage_2019_2.csv', encoding='euc-kr',index_col=False)
data2.head()


# In[32]:


data2.describe()


# ### 2019년 1학기, 2학기 데이터 병합

# In[33]:


test = [data1, data2]


# In[34]:


result = pd.concat(test)


# In[99]:


result


# In[35]:


result.describe()


# # Pandas Profiling 이용한 전처리 준비 (결과는 처참함...)
# 
# ## 데이터 타입 변경 필요

# # 컬럼 하나씩 다 보면서 데이터 타입 변경 및 불필요 컬럼 제거

# In[39]:


result.columns


# # 1. '구분1' column --> 필요 없음.
# ## 이상치 파악 결과, 4번에 걸쳐 크롤링을 해서 header가 4번 들어갔음을 확인하였다
# ## 처음 불러올 때 해당 인덱스들 확인 후 삭제 요망

# In[42]:


result['구분1'].unique()


# In[43]:


result['구분1'].describe()


# In[46]:


result[result['구분1'] == '구분1']


# - 이상치 파악 결과, 4번에 걸쳐 크롤링을 해서 header가 4번 들어갔음을 확인하였다
# - 처음 불러올 때 해당 인덱스들 확인 후 삭제 요망

# In[48]:


data = result.drop([33615, 50281, 34063, 49587])


# In[49]:


data['구분1'].unique()


# # 2. '구분2' column = 학부대학
# ## data type = object --> category
# - '공통기초(10-18)'은 '교양기초(2019~)'와 같음. 
# - 단과대들은 놔두고, 나무지 전공이 아닌 것들은 따로 변수로 통합하면 된다
# 
# ('교양기초(2019~)', '대학교양(2019~)', '기초교육(2019~)', '공통기초(10~18)','필수교양(10~18)', '선택교양(10~18)', '학부기초(~2009)', '학부필수(~2009)','계열기초(~2009)', '학부선택(~2009)','국제캠퍼스(2019~)', '(~2018)국제캠퍼스')

# In[50]:


data['구분2'].unique()


# 안전빵으로 data2 만들어 object --> category 변환 시작

# In[56]:


data2 = data.copy()


# In[68]:


data2 = data2.astype({"구분2":'category'}) 


# In[69]:


data2['구분2'].unique()


# In[187]:





# In[188]:


tt = combine_category(data2, '구분2', before, '교양')


# In[185]:


before = ['교양기초(2019~)', '대학교양(2019~)', '기초교육(2019~)', '공통기초(10~18)','필수교양(10~18)', '선택교양(10~18)', '학부기초(~2009)', '학부필수(~2009)','계열기초(~2009)', '학부선택(~2009)','국제캠퍼스(2019~)', '(~2018)국제캠퍼스']


# In[191]:


tt['구분2'].unique()


# In[177]:


a = '채플'


# In[182]:


l=[]
for i in range(12):
    l.append(a)


# In[183]:


l


# In[ ]:





# In[131]:


test = data2.copy()


# In[168]:


t1 = test['구분2'].replace(
    ['교양기초(2019~)', '대학교양(2019~)', '기초교육(2019~)', '공통기초(10~18)','필수교양(10~18)', '선택교양(10~18)', '학부기초(~2009)', '학부필수(~2009)','계열기초(~2009)', '학부선택(~2009)','국제캠퍼스(2019~)', '(~2018)국제캠퍼스'],
    ['교양','교양','교양','교양','교양','교양','교양','교양','교양','교양','교양','교양']
)


# In[173]:


test['구분2'] = t1


# In[174]:


test


# In[176]:


test['구분2'].unique()


# In[162]:


c_list = ['교양기초(2019~)', '대학교양(2019~)', '기초교육(2019~)', '공통기초(10~18)','필수교양(10~18)', '선택교양(10~18)', '학부기초(~2009)', '학부필수(~2009)','계열기초(~2009)', '학부선택(~2009)','국제캠퍼스(2019~)', '(~2018)국제캠퍼스']
print(type(c_list))
len(c_list)


# In[158]:


test.head()


# In[ ]:





# In[149]:


'교양기초(2019~)' in c_list


# In[148]:


test.loc[:,'구분2'] == '교양기초(2019~)'


# In[ ]:





# In[ ]:





# # 3. '구분3' column = 전공
# ## data type object --> category

# In[79]:


data2['구분3'].unique()


# In[80]:


data2 = data2.astype({"구분3":'category'}) 


# In[81]:


data2['구분3'].unique()


# In[106]:


len(data2['과목명'].unique())


# # 4. '학정번호-분반-실습' column  --> 제거
# 1. 수업을 구분하는  변수로 이미 '교과목명'이 있음
# 2. 동일 과목 별 다른 수업을 구분하나, 이미 교수 별로 나누어져 있고, 같은 교수의 동일한 두 과목이라도 시간으로 구분되어 있기 때문에 추가적인 정보는 제공하지 않는다고 판단.

# <img src="reason1.png" width="1200">

# In[86]:


data2['학정번호-분반-실습'].unique()


# In[100]:


data2['학정번호-분반-실습'].isnull().sum()


# In[103]:


len(data2['학정번호-분반-실습'].unique())


# # 5. '과목명' column = 과목명
# # 채플과 같이 과목명 다르지만 같은 수업들 선별해야함

# In[87]:


data2['과목명'].unique()


# In[93]:


data2[data2['과목명'] == '채플']


# In[ ]:




