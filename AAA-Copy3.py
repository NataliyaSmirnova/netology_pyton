#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
from numpy  import percentile
from numpy  import std
from numpy  import mean
import random
import scipy.stats as sts
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


# In[3]:


st_VLE= pd.read_csv('studentVle.csv')
courses = pd.read_csv('courses.csv')
students=pd.read_csv('studentInfo.csv')
registration = pd.read_csv('studentRegistration.csv')
results = pd.read_csv('studentAssessment.csv')
assessment = pd.read_csv('assessments.csv')
VLE= pd.read_csv('vle.csv')


# In[4]:


courses 


# ## Создание общей таблицы

# Необходимо создать таблицу

# In[3]:


st_VLE.head()


# Группируем данные с целью определения суммы кликов по всем ресурсам в активные дни для каждого студента в рамках 1-го курса

# In[4]:


st_VLE_sum= st_VLE.groupby(['code_module','code_presentation', 'id_student', 'date']).sum().reset_index().drop(['id_site'], axis=1)
st_VLE_sum.head()


# Добавляем к таблице с результатами контрольх испытаний финльный результат прохождения курса. Убираем из рассматрения студентов, которые покинули обучение еще до его начала. А также тех, кто курс проходит повторно.

# In[5]:


students_reg= students[(students.num_of_prev_attempts ==0)].         merge(registration[(registration.date_unregistration >0) | (pd.isna(registration.date_unregistration) == True)],         how ='inner', on=['code_module','code_presentation', 'id_student'])

st_VLE_fr=st_VLE_sum.merge(students_reg, how ='inner', on=['code_module','code_presentation','id_student'])


total_table=st_VLE_fr.drop(st_VLE_fr.iloc[:, [6,8,10,11,14,15]], axis=1)
total_table.tail()


# In[6]:


students_reg


# Проверяем на наличие незаполненных строк

# In[7]:


total_table.isnull().sum()


# ## Отбор курсов

# In[8]:


assessment[(assessment.assessment_type != 'Exam')].groupby(['code_module', 'code_presentation']).sum(). drop(['id_assessment', 'date'], axis =1)


# Исключаем из рассмотрения курс GGG, тк промежуточные испытания не имели веса в итоговой оценке за курс, что не сооттветствует требованиям к рассматриваемым нами данным.

# In[9]:


st_VLE[(st_VLE['code_module']== 'GGG')].code_presentation.unique()


# In[10]:


st_VLE_GGG= st_VLE[(st_VLE['code_module'] == 'GGG') & (st_VLE['code_presentation'] == '2013J')]
clicks_GGG= st_VLE_GGG.groupby('date').agg({'sum_click': 'sum'}).reset_index()


# In[11]:


x_GGG = clicks_GGG['date']
y_GGG= clicks_GGG['sum_click']

fig, ax = plt.subplots()

ax.plot(x_GGG, y_GGG, color = 'r', linewidth = 3)
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

plt.xlabel('День', fontsize =12)
plt.ylabel('Сумма кликов по всем студентам курса GGG', fontsize =12)
plt.title('Активность студентов курса "GGG" в виртуальной среде обучения' , fontsize =15)
plt.grid()

fig.set_figwidth(15)
fig.set_figheight(8)


# In[12]:


assessment_GGG= assessment[(assessment['code_module'] == 'GGG') & (assessment['code_presentation'] == '2014B')]
assessment_GGG


# Для выбора курсов и конкретного потока в частности, необходимо убедиться, что поведение студентов в выбранных потоках не является аномальным. Для этого сравним активность стдентов разных потоков и курсов. Однако перед этим убедимся, что в потоках одного курса сохраняется одинаковое количество контрольных испытаний. Если количество испытаний в разных потоках одного курса будет различным, эти потоки исключаются из рассмотрения.

# In[13]:


assessment[(assessment.code_module != 'GGG')&(assessment.assessment_type != 'Exam')].groupby(['code_module','code_presentation','assessment_type']).count().drop(['date','weight'], axis=1)


# Из таблицы видно, что в рамках курса ВВВ у потока 2014J изменилось количество испытаний: остались только 5 испытаний, оцениваемых преподавателем (ТМА), хотя у остальных потоков их было 6, а также было 5 испытаний, оцениваемых компьютером (СМА). \
# Кроме того, в потоке 2013В в рамках курса DDD было 7 СМА и 6 ТМА, впоследующих же потоках осталось только 6 ТМА. Поэтому поток 2013В исключаем из рассмотрения

# In[14]:


#исключаем неподходящие курсы из рассмотрения
activity=total_table[(total_table.code_module != 'GGG')&                    ((total_table.code_module != 'DDD')| (total_table.code_presentation != '2013B'))&                    ((total_table.code_module != 'BBB')| (total_table.code_presentation != '2014J'))]

activity_graph=activity.iloc[:,[0,1,3,4]].groupby(['code_module','code_presentation','date']).sum().reset_index()


# In[15]:


"""Cоздаем таблицу, на основе которой будем рисовать график. 
В таблице отображаем сумму кликов в системе VLE по всем студентам каждого потока"""

activity_graph=activity.iloc[:,[0,1,3,4]].groupby(['code_module','code_presentation','date']).sum().reset_index()


# In[16]:


"""Добавляем столбец %, в котором отображается информация о том, 
какой % кликов был сделан в конкретный день из всех кликов на курсе за все время"""

activity_graph_fnl=activity_graph.merge(activity_graph.groupby(['code_module','code_presentation']).                                        sum().reset_index().drop('date', axis=1), how ='left',                                         on=['code_module','code_presentation'])
activity_graph_fnl['%']=activity_graph_fnl['sum_click_x']/activity_graph_fnl['sum_click_y']*100
activity_graph_fnl=activity_graph_fnl.drop('sum_click_y',axis =1)
activity_graph_fnl.head()


# In[17]:


table_activity = pd.pivot_table(activity_graph_fnl, values='%', index=['date'],                                 columns=['code_module','code_presentation'],  aggfunc=np.sum, fill_value=0)


# In[18]:


table_activity['AAA'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс,%', fontsize =12)
plt.title('Активность студентов курса "AAA" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# In[19]:


assessment[(assessment.code_module == 'AAA')]


# In[20]:


table_activity['BBB'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс, %', fontsize =12)
plt.title('Активность студентов курса "BBB" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# In[21]:


table_activity['CCC'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс, %', fontsize =12)
plt.title('Активность студентов курса "CCC" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# In[22]:


table_activity['DDD'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс, %', fontsize =12)
plt.title('Активность студентов курса "DDD" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# In[23]:


assessment[(assessment.code_module == 'DDD')]


# In[24]:


table_activity['EEE'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс, %', fontsize =12)
plt.title('Активность студентов курса "EEE" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# In[25]:


table_activity['FFF'].plot(figsize=(15,8))
plt.xlabel('День', fontsize =12)
plt.ylabel('Доля кликов от общего числа кликов за курс, %', fontsize =12)
plt.title('Активность студентов курса "FFF" в виртуальной среде обучения ')
plt.grid()
plt.ylim(0)
plt.xlim(-25)
plt.xticks(np.arange(-25, 270, 10)) 
plt.show()


# На графиках видно, что поведение студентов из разных потоков, но в рамках одного курса очень схоже. Имеет место быть небольшое смещение пиков кривых в силу изменения дат контрольных испытаний. 
# 
# Поведение студентов различных курсов различается между собой. Но это говорит скорее о специфике курса, нежели о специфике поведения студентов
# 
# Также можно увидеть, что во всех потоках, которые стартовали в феврале 2014 года (2014В), в районе 215 дня имеется нулевое значение активности. Поскольку данная ситуация наблюдается на всех курсах, можно сделать вывод о том, что это связано с неполадкой программного обеспечения, отвечающего за контроль активности студентов. На этом основании потоки 2014В не включены в рассмотрение.
# 
# ИТОГ: В нашу выборку мы берем по 1 потоку от каждого курса, за исключением тех, которые мы отсеяли ранее

# ##  Курс ААА

# В рамках одного из потоков (2013 J) курса ААА разбиваем данные в зависимости от финального результата, полуенного студентом

# In[26]:


st_VLE_AAA=total_table[(total_table.code_module == 'AAA')& (total_table.code_presentation =='2013J')]
AAA_pass=st_VLE_AAA[(st_VLE_AAA.final_result == 'Pass')]
AAA_wd=st_VLE_AAA[(st_VLE_AAA.final_result == 'Withdrawn')]
AAA_fail=st_VLE_AAA[(st_VLE_AAA.final_result == 'Fail')]
AAA_dist=st_VLE_AAA[(st_VLE_AAA.final_result == 'Distinction')]

st_VLE_AAA.head()


# In[27]:


AAA_fail.head()


# Проверяем на наличие незаполненных строк

# In[28]:


st_VLE_AAA.info()


# ## Определяем выбросы

# Для определения выбросов в выборке рассмотрим по каждому студенту суммарное количество кликов  за весь курс

# In[29]:


AAA_fail.groupby('id_student').sum().reset_index().head()


# Для наглядной демонстрации наличия/отсутствия выбросов построим диаграмму размаха (ящик с усами)

# In[30]:


fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.set_title('Распределение суммы кликов среди студентов, проваливших курс ', fontsize = 15)
ax1.boxplot(AAA_fail.groupby('id_student').sum().reset_index()['sum_click'])


plt.ylabel('Суммарное количество кликов за курс', fontsize = 12)


# In[31]:


fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.set_title('Распределение суммы кликов среди студентов, завершивших курс ', fontsize = 15)
ax2.boxplot(AAA_pass.groupby('id_student').sum().reset_index()['sum_click'])
plt.ylabel('Суммарное количество кликов за курс', fontsize = 12)


# Из графика видно, что существуют выбросы, но необходимо точно расчитать границы выбросов для корректной фильтрации данных

# Рассчитаем границы выбросов
# 
# Если выборка имеет вид Гауссовского (нормального) распределения или схожего с ним, мы можем использовать метод среднеквадратичного отклонения (σ) для нахождения выбросов.
# 
# Для выборок не нормального распределения лучше всего использовать метод интерквартильного интервала (IQR)*.
# 
# *Источник:https://trainmydata.com/article/statistichieskiie-mietody-dlia-opriedielieniia-vybrosov-v-dannykh 

# Строим график частотного распределения суммарного числа кликов, сделанного студентом в течение курса

# In[32]:


plt.figure(figsize=(15,5))

plt.hist(AAA_fail.groupby('id_student').sum().reset_index()['sum_click'],20, color = 'r')

plt.xlabel('Суммарное количество кликов за весь курс')
plt.ylabel('Частота (количество студентов)')
plt.title('Частотный график распределения суммы кликов среди студентов, проваливших курс',fontsize = 12)
plt.xlim(0, AAA_fail.groupby('id_student').sum().reset_index()['sum_click'].max())
plt.grid(True)

plt.show()


# In[33]:


plt.figure(figsize=(15,5))

plt.hist(AAA_pass.groupby('id_student').sum().reset_index()['sum_click'],20, color = 'g')

plt.xlabel('Суммарное количество кликов за курс',fontsize = 12)
plt.ylabel('Частота (количество студентов)',fontsize = 12)
plt.title('Частотный график распределения суммы кликов среди студентов, завершивших курс',fontsize = 15)
plt.xlim(0, AAA_pass.groupby('id_student').sum().reset_index()['sum_click'].max())
plt.grid(True)

plt.show()


# In[34]:


plt.figure(figsize=(15,5))

plt.hist(AAA_wd.groupby('id_student').sum().reset_index()['sum_click'],20, color = 'orange')

plt.xlabel('Суммарное количество кликов за курс',fontsize = 12)
plt.ylabel('Частота (количество студентов)',fontsize = 12)
plt.title('Частотный график распределения суммы кликов среди студентов, покинувших курс',fontsize = 15)
plt.xlim(0, AAA_wd.groupby('id_student').sum().reset_index()['sum_click'].max())
plt.grid(True)

plt.show()


# In[35]:


plt.figure(figsize=(15,5))

plt.hist(AAA_dist.groupby('id_student').sum().reset_index()['sum_click'],20, color = 'b')

plt.xlabel('Суммарное количество кликов за курс',fontsize = 12)
plt.ylabel('Частота (количество студентов)',fontsize = 12)
plt.title('Частотный график распределения суммы кликов среди студентов, завершивших курс с отличием',fontsize = 15)
plt.xlim(0, AAA_dist.groupby('id_student').sum().reset_index()['sum_click'].max())
plt.grid(True)

plt.show()


# Ни в одной выборке распределение не является нормальным, поэтому применяем метод интерквартильного интервала (IQR)

# In[36]:


q25_f, q75_f = percentile(AAA_fail.groupby('id_student').sum().reset_index()['sum_click'], 25),                     percentile(AAA_fail.groupby('id_student').sum().reset_index()['sum_click'], 75)
iqr_f = q75_f - q25_f
cut_off_f = iqr_f * 1.5
lower_f , upper_f = q25_f- cut_off_f, q75_f + cut_off_f

print('нижняя граница - ', lower_f ,';', 'верхняя граница - ', upper_f)


# In[37]:


q25_p, q75_p = percentile(AAA_pass.groupby('id_student').sum().reset_index()['sum_click'], 25),                     percentile(AAA_pass.groupby('id_student').sum().reset_index()['sum_click'], 75)
iqr_p = q75_p - q25_p
cut_off_p = iqr_p * 1.5
lower_p , upper_p = q25_p- cut_off_p, q75_p + cut_off_p

print('нижняя граница - ', lower_p ,';', 'верхняя граница - ', upper_p)


# In[38]:


q25_d, q75_d = percentile(AAA_dist.groupby('id_student').sum().reset_index()['sum_click'], 25),                     percentile(AAA_dist.groupby('id_student').sum().reset_index()['sum_click'], 75)
iqr_d = q75_d - q25_d
cut_off_d = iqr_d * 1.5
lower_d , upper_d = q25_d- cut_off_d, q75_d + cut_off_d

print('нижняя граница - ', lower_d ,';', 'верхняя граница - ', upper_d)


# In[39]:


q25_wd, q75_wd = percentile(AAA_wd.groupby('id_student').sum().reset_index()['sum_click'], 25),                         percentile(AAA_wd.groupby('id_student').sum().reset_index()['sum_click'], 75)
iqr_wd = q75_wd - q25_wd
cut_off_wd = iqr_wd * 1.5
lower_wd , upper_wd = q25_wd- cut_off_wd, q75_wd + cut_off_wd

print('нижняя граница - ', lower_wd ,';', 'верхняя граница - ', upper_wd)


# Рассчитаем, сколько выбросов в каждой выборке

# In[40]:


AAA_fail.groupby('id_student').sum()['sum_click'][(AAA_fail.groupby('id_student').sum()['sum_click'] >=upper_f)].count()


# In[41]:


AAA_pass.groupby('id_student').sum()['sum_click'][(AAA_pass.groupby('id_student').sum()['sum_click'] >=upper_p)].count()


# In[42]:


AAA_dist.groupby('id_student').sum()['sum_click'][(AAA_dist.groupby('id_student').sum()['sum_click'] >=upper_d)].count()


# In[43]:


AAA_wd.groupby('id_student').sum()['sum_click'][(AAA_wd.groupby('id_student').sum()['sum_click'] >= upper_wd)].count()


# #### Исключаем выбросы

# Создаем списки студентов, которые попали в финальную выборку

# In[44]:


pass_list=AAA_pass.groupby('id_student').sum().reset_index()           [(AAA_pass.groupby('id_student').sum().reset_index()['sum_click']< upper_p)]['id_student'].tolist()
len(pass_list)


# In[45]:


fail_list=AAA_fail.groupby('id_student').sum().reset_index()           [(AAA_fail.groupby('id_student').sum().reset_index()['sum_click']< upper_f)]['id_student'].tolist()

wd_list=AAA_wd.groupby('id_student').sum().reset_index()           [(AAA_wd.groupby('id_student').sum().reset_index()['sum_click']< upper_wd)]['id_student'].tolist()

dist_list=AAA_dist.groupby('id_student').sum().reset_index()           [(AAA_dist.groupby('id_student').sum().reset_index()['sum_click']< upper_d)]['id_student'].tolist()


# Фильтруем данные так, чтобы в выборке остались только id студентов из списков

# In[46]:


AAA_pass_cln= AAA_pass[(AAA_pass.id_student.isin(pass_list))]
AAA_dist_cln=AAA_dist[(AAA_dist.id_student.isin(dist_list))]
AAA_wd_cln=AAA_wd[(AAA_wd.id_student.isin(wd_list))]
AAA_fail_cln=AAA_fail[(AAA_fail.id_student.isin(fail_list))]

AAA_cln= pd.concat([AAA_pass_cln, AAA_fail_cln, AAA_dist_cln, AAA_wd_cln], ignore_index=True)


# In[47]:


AAA_pass_cln.head()


# Создаем общую таблицу с колнками "дата"  и суммами кликов по каждой группе студентов

# In[48]:


AAA_pass=AAA_pass_cln.iloc[:,[3,4]].groupby('date').sum().reset_index()
AAA_dist=AAA_dist_cln.iloc[:,[3,4]].groupby('date').sum().reset_index()
AAA_wd=AAA_wd_cln.iloc[:,[3,4]].groupby('date').sum().reset_index()
AAA_fail=AAA_fail_cln.iloc[:,[3,4]].groupby('date').sum().reset_index()

AAA_graph=AAA_pass.merge(AAA_dist, how ='outer', on='date').merge(AAA_wd, how ='outer', on='date')                .merge(AAA_fail, how ='outer', on='date')

AAA_graph.columns = ['date', 'pass_clicks', 'dist_clicks', 'wd_clicks', 'fail_clicks']
AAA_graph.tail(16)


# В таблице присутствуют пустые строки, которые свидетельствуют об отсутствии активности всех студентов конкретной группы в этот день. То есть количество кликов = 0. Заменим пустые значения на 0

# In[49]:


AAA_graph= AAA_graph.fillna(0)
AAA_graph.tail()


# Поскольку группы  отличаются по количеству студентов (а соответственно и по количеству кликов), будем сравнивать их между собой по % соотношению суммы кликов, сделанных в конкретный день к общей сумме кликов в группе

# In[50]:


pass_clicks_sum= AAA_graph.pass_clicks.sum()
dist_clicks_sum= AAA_graph.dist_clicks.sum()
fail_clicks_sum= AAA_graph.fail_clicks.sum()
wd_clicks_sum= AAA_graph.wd_clicks.sum()


# In[51]:


AAA_graph.sum()


# In[52]:


AAA_graph['pass_%']=round(AAA_graph['pass_clicks']/pass_clicks_sum*100,2)
AAA_graph['dist_%']=round(AAA_graph['dist_clicks']/dist_clicks_sum*100,2)
AAA_graph['wd_%']=round(AAA_graph['wd_clicks']/wd_clicks_sum*100,2)
AAA_graph['fail_%']=round(AAA_graph['fail_clicks']/fail_clicks_sum*100,2)
AAA_graph.head()


# Рисуем график динамики кликов в течение курса

# In[53]:


x = AAA_graph['date']
y1 = AAA_graph['pass_%']
y2 = AAA_graph['dist_%']
y3 = AAA_graph['wd_%']
y4 = AAA_graph['fail_%']

fig, ax = plt.subplots()

ax.plot(x, y1, color = 'g', label='Pass')
ax.plot(x, y2, color = 'b', label='Distinction')
ax.plot(x, y3, color = 'orange', label='Withdrawn')
ax.plot(x, y4, color = 'r', label='Fail')

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

fig.set_figwidth(15)
fig.set_figheight(8)
ax.legend(fontsize =12)

plt.title('Активность студентов в виртуальной среде обучения', fontsize= 20)
plt.xlabel('День',fontsize =15)
plt.ylabel('Доля кликов от общего числа в своей группе, %',fontsize =15)
plt.grid(True)

plt.ylim(0)
plt.xlim(-10)


# 
# ### Аналогичная статистика с рандомной  малой выборкой

# In[54]:


x = AAA_graph['date']
y1 = AAA_graph['fail_%']

fig, ax = plt.subplots()

ax.plot(x, y1, color = 'r', label='Fail',)


ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

fig.set_figwidth(15)
fig.set_figheight(8)
ax.legend(fontsize =12)
plt.title('Активность студентов, проваливших курс, в виртуальной среде обучения', fontsize= 15)
plt.xlabel('День',fontsize =12)
plt.ylabel('Доля кликов от общего числа в своей группе, %',fontsize =12)

plt.grid(True)

plt.ylim(0)
plt.xlim(AAA_graph['date'].min())


# In[55]:


Fail_30=random.sample(AAA_fail_cln['id_student'].unique().tolist(),30)
#Pass_30


# In[56]:


AAA_fail_30=AAA_fail_cln[AAA_fail_cln['id_student'].isin(Fail_30)]


# In[57]:


AAA_fail_30=AAA_fail_30.iloc[:,[3,4]].groupby('date').sum().reset_index()


# In[58]:


fail_30_sum=AAA_fail_30['sum_click'].sum()


# In[59]:


AAA_fail_30['fail_%']= AAA_fail_30['sum_click']/fail_30_sum*100
AAA_fail_30.head()


# In[60]:


x = AAA_fail_30['date']
y1 = AAA_fail_30['fail_%']

fig, ax = plt.subplots()

ax.plot(x, y1, color = 'r', label='Fail',)

ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))

fig.set_figwidth(15)
fig.set_figheight(8)
ax.legend()
plt.title('Активность 30 студентов, проваливших курс, в виртуальной среде обучения', fontsize = 15)
plt.xlabel('День', fontsize = 12)
plt.ylabel('Доля кликов от общего числа в своей группе, %', fontsize = 12)

plt.grid(True)

plt.ylim(0)
plt.xlim(AAA_graph['date'].min())


# ## Сравнение поведения студентов разных групп

# Для того, чтобы понять, отличается ли поведение студентов из разных групп, нужно провести тестирование, которое покажет, существует ли статистическое различие выборками.
# 
# Выбор вида теста зависит в частности от вида распределения данных

# In[61]:


plt.figure(figsize=(15,8))
sns.distplot(AAA_graph['pass_%'], color ='g')
sns.distplot(AAA_graph['wd_%'], color ='orange')
sns.distplot(AAA_graph['fail_%'], color ='r')
sns.distplot(AAA_graph['dist_%'], color ='b')

plt.legend(['Pass', 'Withdrawn', 'Fail', 'Didtinction'], fontsize = 12)
plt.title('График плотности распределения', fontsize = 15)
plt.xlabel('Клики в день(в % от общего числа кликов за курс)', fontsize = 12)


# Данные распределены ненормально, моэтому используем критерий Манна-Уитни
# 
# Условимся, что уровень значимости равен 5%

# #### PASS / FAIL

# In[62]:


u, p_value = sts.mannwhitneyu(AAA_graph['pass_%'], AAA_graph['fail_%'])
print("two-sample wilcoxon-test", p_value)


# Поскольку p-value < 0,05,  можно отвергнуть гипотезу Н0 об идентичности выборок, и говорим о существовании статистическом различии в поведении между провалившими и закончившими курс студентами

# #### PASS / WITHDRAWN

# In[63]:


u, p_value = sts.mannwhitneyu(AAA_graph['pass_%'], AAA_graph['wd_%'])
print("two-sample wilcoxon-test", p_value)


# P-value < 0,05,  Н0 отвергаем \
# Существует разница в поведении между покинувшими и закончившими курс студентами

# #### DISTINCTION / FAIL

# In[64]:


u, p_value = sts.mannwhitneyu(AAA_graph['dist_%'], AAA_graph['fail_%'])
print("two-sample wilcoxon-test", p_value)


# P-value < 0,05,  Н0 отвергаем \
# Существует разница в поведении между провалившими и закончившими курс с отличием студентами

# #### DISTINCTION / WITHDRAWN

# In[65]:


u, p_value = sts.mannwhitneyu(AAA_graph['dist_%'], AAA_graph['wd_%'])
print("two-sample wilcoxon-test", p_value)


# P-value < 0,05,  Н0 отвергаем \
# Существует разница в поведении между покинувшими и закончившими курс с отличием студентами

# #### DISTINCTION / PASS

# In[66]:


u, p_value = sts.mannwhitneyu(AAA_graph['pass_%'], AAA_graph['dist_%'])
print("two-sample wilcoxon-test", p_value)


# P-value > 0,05,  Н0 принимаем \
# Делаем вывод о схожести поведения студентов, которые закончили курс (с отличием и без)

# #### FAIL/ WITHDRAWN

# In[67]:


u, p_value = sts.mannwhitneyu(AAA_graph['fail_%'], AAA_graph['wd_%'])
print("two-sample wilcoxon-test", p_value)


# P-value < 0,05,  Н0 отвергаем \
# Существует разница в поведении между покинувшими и проваливими курс  студентами

# ### Коэффициент

# Рассчитаем коэффициент "равномерности" работы с VLE. Этот коэффициент отображает периодичность занятий. \
# Измеряется от 0 до 1, чем ближе к 1, тем чаще студенты взаимодействуют с VLE. \
# Формула:\
#         ∑(количество дней взаимодействия)/ Количество дней в курсе/ Количество студентов

# In[68]:


courses.head()


# In[69]:


days_courses = courses[(courses.code_module == 'AAA') &                        (courses.code_presentation == '2013J')]['module_presentation_length'][0] - AAA_wd_cln.date.min()

days_courses


# In[70]:


days_VLE_wd = AAA_wd_cln.date.count()
days_VLE_fail = AAA_fail_cln.date.count()
days_VLE_pass = AAA_pass_cln.date.count()
days_VLE_dist = AAA_dist_cln.date.count()
days_VLE_wd


# In[71]:


student_wd=len(AAA_wd_cln.id_student.unique())
student_fail=len(AAA_fail_cln.id_student.unique())
student_pass=len(AAA_pass_cln.id_student.unique())
student_dist=len(AAA_dist_cln.id_student.unique())


# In[72]:


ind_wd=days_VLE_wd/student_wd/days_courses
ind_fail=days_VLE_fail/student_fail/days_courses
ind_pass=days_VLE_pass/student_pass/days_courses
ind_dist=days_VLE_dist/student_dist/days_courses

print ('индекс равномерности взаимодействия с VLE среди покинувших курс:', round(ind_wd,2))
print ('среди проваливших курс:', round(ind_fail ,2))
print ('среди завершивших курс:', round(ind_pass,2)) 
print ('среди отличников:', round(ind_dist,2))


# ### Среднее количество кликов

# Посмотрим также какое среднее кличество кликов делают студенты разных групп в период контрольных испытаний и период обучения без оценки.\
# 
# Создаем список, который будет включать даты, относящиеся к периоду контрольных испытаний. Заранее условились, что этот период начинается за 5 дней до испытания и заканчивается непосредственно в день испытания.

# In[73]:


dates = assessment[(assessment.code_module == 'AAA')&(assessment.code_presentation== '2013J')&(assessment.assessment_type!= 'Exam')]['date'].tolist()


# In[74]:


dates_full_list=[]
for date in dates:
    for z in range (0, len(dates)):
        dates_full_list.append(date-z)
dates_full_list


# Добавляем новый столбец 'period_type' к общей таблице по всем студентам (AAA_cln), отображающий характеристику периода.
# 
# Условно периоды разделили на 2 типа:\
# study period - период обучения без контрольных испытаний\
# assessment period - 5-дневный период перед контрольным испытанием

# In[75]:


def period_type(a):
    if a.date in dates_full_list:
        return 'assessment period'
    return 'study period'


# In[76]:


AAA_cln['period_type'] = AAA_cln.apply(period_type, axis=1)
AAA_cln.tail()


# Смотрим, какое среднее число кликов в день делает каждая из групп в период испытаний и в обычном режиме.

# In[77]:


mean_table_FR =  pd.pivot_table(AAA_cln, values='sum_click', index=['period_type'],                                 columns=['final_result'],  aggfunc=np.mean)
mean_table_FR


# ### ДЕРЕВО РЕШЕНИЙ
# #### Подготовка данных

# In[78]:


total_table.head()


# In[79]:


dates_AAA = assessment[(assessment.code_module == 'AAA')&(assessment.code_presentation== '2013J')&(assessment.date.isnull() == False)]['date'].unique().tolist()
dates_BBB = assessment[(assessment.code_module == 'BBB')&(assessment.code_presentation== '2013B')&(assessment.date.isnull() == False)]['date'].unique().tolist()
dates_CCC = assessment[(assessment.code_module == 'CCC')&(assessment.code_presentation== '2014J')&(assessment.date.isnull() == False)]['date'].unique().tolist()
dates_DDD = assessment[(assessment.code_module == 'DDD')&(assessment.code_presentation== '2014J')&(assessment.date.isnull() == False)]['date'].unique().tolist()
dates_EEE = assessment[(assessment.code_module == 'EEE')&(assessment.code_presentation== '2014J')&(assessment.date.isnull() == False)]['date'].unique().tolist()
dates_FFF = assessment[(assessment.code_module == 'FFF')&(assessment.code_presentation== '2013B')&(assessment.date.isnull() == False)]['date'].unique().tolist()


# In[80]:


full_dates_AAA=[date-z for date in dates_AAA for z in range (0, 5) ]
full_dates_BBB=[date-z for date in dates_BBB for z in range (0, 5)]
full_dates_CCC=[date-z for date in dates_CCC for z in range (0, 5)]
full_dates_DDD=[date-z for date in dates_DDD for z in range (0, 5)]
full_dates_EEE=[date-z for date in dates_EEE for z in range (0, 5)]
full_dates_FFF=[date-z for date in dates_FFF for z in range (0, 5)]

assessment_dates =dict(zip(list(students_reg.code_module.unique()),                        [full_dates_AAA, full_dates_BBB, full_dates_CCC, full_dates_DDD, full_dates_EEE, full_dates_FFF]))


# In[81]:


def study_period(a):
    if a.code_module in list(assessment_dates.keys()):
        if a.date in assessment_dates[a.code_module]:
            return 'assessment period'
    return 'study period'


# In[187]:


activity_table=st_VLE.merge(VLE.iloc[:,:4], how ='inner', on=['code_module','code_presentation','id_site'])


# In[188]:


st_VLE.head()


# In[189]:


activity_table=st_VLE[(st_VLE.id_student.isin(total_table.id_student.unique().tolist()))]


# In[190]:


activity_table=activity_table[((activity_table.code_module == "AAA") & (activity_table.code_presentation == "2013J")) |                                  ((activity_table.code_module == "BBB") & (activity_table.code_presentation == "2013B")) |                                  ((activity_table.code_module == "CCC") & (activity_table.code_presentation == "2014J")) |                                  ((activity_table.code_module == "DDD") & (activity_table.code_presentation == "2014J")) |                                  ((activity_table.code_module == "EEE") & (activity_table.code_presentation == "2014J")) |                                  ((activity_table.code_module == "FFF") & (activity_table.code_presentation == "2013B"))]


# In[191]:


activity_table['period_type'] = activity_table.apply(study_period, axis=1)


# In[260]:


activity_table.head()


# In[262]:


period=pd.pivot_table(activity_table, values=['sum_click', 'date'], index=['code_module','id_student'],                                 columns=['period_type'],  aggfunc={'date': pd.Series.nunique,  'sum_click':  np.sum}, fill_value=0).reset_index()
period.columns=['code_module','id_student','date_assessment_period','date_study_period','clicks_assessment_period','clicks_study_period']

period.head()


# In[281]:


activity_table_2 = activity_table.groupby(['code_module','code_presentation','id_student']).agg({'date':[np.min, pd.Series.nunique],  'sum_click':  np.sum}).reset_index()
activity_table_2.columns=['code_module','code_presentation','id_student','start_activity_date', 'active_days','total_clicks']
activity_table_2.head()


# In[304]:


activity_table_3=activity_table_2.merge(registration, how='left', on =['code_module','code_presentation','id_student']).drop(['date_registration'], axis=1)
activity_table_4=activity_table_3.merge(period, on =['code_module','id_student'], how= 'left')
activity_table_4.head()


# In[305]:


activity_table_4.columns.values[7:11]=['active_days_assessment','active_days_study', 'clicks_assessment', 'clicks_study']
activity_table_4.head()


# In[306]:


def days_on_course(a):
    if pd.isna(a.date_unregistration) == True:
        return int((courses[((courses.code_module == a.code_module)& (courses.code_presentation == a.code_presentation))]['module_presentation_length'] - a.start_activity_date))
    return (a.date_unregistration - a.start_activity_date)


# In[307]:


activity_table_4['days_on_course'] = activity_table_4.apply(days_on_course, axis=1)


# In[308]:


activity_table_4.head()


# In[318]:


activity_table_5=activity_table_4[activity_table_4.days_on_course != 0]


# In[319]:


activity_table_5.head()


# In[320]:


activity_table_5['activity_index']= round(activity_table_5.active_days/activity_table_5.days_on_course, 2)


# In[ ]:





# In[321]:


activity_table_5['mean_clicks']= round(activity_table_5.total_clicks/activity_table_5.active_days,2).fillna(0)
activity_table_5['mean_clicks_assessment']=round(activity_table_5.clicks_assessment/activity_table_5.active_days_assessment,2).fillna(0)
activity_table_5['mean_clicks_study']=round(activity_table_5.clicks_study/activity_table_5.active_days_study,2).fillna(0)


# ### Модель

# In[342]:


model_table=activity_table_5.merge(students.iloc[:,[0,1,2,11]], how='left', on =['code_module','code_presentation','id_student']).drop(['start_activity_date','date_unregistration','days_on_course'], axis =1)


# In[343]:


model_table.columns


# In[344]:


dummies = pd.get_dummies(model_table.final_result)
model_table_dummies= pd.concat([model_table, dummies], axis =1)
model_table_dummies= model_table_dummies.drop('final_result', axis =1)


# In[345]:


#model_table_dummies.iloc[:,13:-4].columns =['dataplus','dualpane','externalquiz', 'forumng', 'glossary', 'homepage', 'oucollaborate', \
#'oucontent', 'ouelluminate', 'ouwiki','page', 'questionnaire','quiz','resource', 'sharedsubpage','subpage','url']
model_table_dummies.iloc[:,3:-4].columns


# In[346]:


X_data= model_table_dummies.iloc[:,3:-4]
X_data.corr()


# In[347]:


sns.heatmap(X_data.corr(),annot=True,cmap='coolwarm',linewidths=0.8,) 
fig=plt.gcf()
fig.set_size_inches(20,20)
plt.show()


# In[348]:


# создаем матрицу корреляций
corr_matrix = X_data.corr().abs()

# Выбираем верхний треугольник матрицы
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))

# Ищем индексы колонок с корреляцией большей чем 0.95
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]

print(to_drop)


# In[349]:


X_data = X_data.drop(X_data[to_drop], axis=1)
X_data.head()


# In[350]:


Y= model_table_dummies.iloc[:,-4:]
X= model_table_dummies.iloc[:,3:-4]


# In[351]:


print('Количество значений Distinction: ', Y[Y.Distinction ==1].shape)
print('Количество значений Fail: ', Y[Y.Fail ==1].shape)
print('Количество значений Pass: ', Y[Y.Pass ==1].shape)
print('Количество значений Withdrawn: ', Y[Y.Withdrawn ==1].shape)


# С проблемой классификации с несбалансированными данными хорошо работает метод решения деревьев. \
# Для нашей модели разделяем данные на тренировочные и тестовые в пропорции 70% на 30 соответственнo

# In[352]:


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3)


# In[353]:


X_train.columns


# In[354]:


model=RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)


# In[355]:


headers = list(X_train.columns.values)

feature_imp = pd.Series(model.feature_importances_,index=headers).sort_values(ascending=False)

f, ax = plt.subplots(figsize=(20, 20))
sns.barplot(x=feature_imp, y=feature_imp.index)

plt.xlabel('Важность атрибутов')
plt.ylabel('Атрибуты')
plt.title("Наиболее важные атрибуты")
plt.show()


# In[356]:


model.score(X_test, y_test)


# In[388]:



model_table_2=model_table.merge(students.iloc[:,[0,1,2,3,5,6,7,10]], how='left', on =['code_module','code_presentation','id_student'])


# In[389]:


model_table_2.head()


# In[390]:


cols=list(model_table_2)


# In[391]:


cols.insert(18, cols.pop(cols.index('final_result')))


# In[392]:


model_table_2 = model_table_2.ix[:, cols]


# In[393]:


def gender(a):
    if a == 'F':
        return 1
    return 0
model_table_2.gender=model_table_2.gender.apply(gender)


# In[394]:


def education(a):
    if a == 'Lower Than A Level':
        return 1
    if a == 'A Level or Equivalent':
        return 2
    if a == 'HE Qualification':
        return 3
    if a == 'Post Graduate Qualification':
        return 4
    return 0
    
model_table_2.highest_education=model_table_2.highest_education.apply(education)


# In[395]:


def imd(a):
    if a == '10-20%':
        return 1
    if a == '20-30%':
        return 2
    if a == '30-40%':
        return 3
    if a == '40-50%':
        return 4
    if a == '50-60%':
        return 5
    if a == '60-70%':
        return 6
    if a == '70-80%':
        return 7
    if a == '80-90%':
        return 8
    if a == '90-100%':
        return 9
    return 0
model_table_2.imd_band=model_table_2.imd_band.apply(imd)


# In[396]:


def age(a):
    if a == '0-35':
        return 0
    if a == '35-55':
        return 1
    return 2
model_table_2.age_band=model_table_2.age_band.apply(age)


# In[397]:


def disability(a):
    if a == 'Y':
        return 1
    return 0
model_table_2.disability=model_table_2.disability.apply(disability)


# In[398]:


model_table_dummies_2= pd.concat([model_table_2, dummies], axis =1)
model_table_dummies_2= model_table_dummies_2.drop('final_result', axis =1)
model_table_dummies_2.head()


# In[399]:


Y_2= model_table_dummies_2.iloc[:,-4:]
X_2= model_table_dummies_2.iloc[:,3:-4]


# In[400]:


X_2_train, X_2_test, y_2_train, y_2_test = train_test_split(X_2, Y_2, test_size=0.3)


# In[401]:


model_2=RandomForestClassifier(n_estimators=100)

model_2.fit(X_2_train, y_2_train)


# In[402]:


headers = list(X_2_train.columns.values)

feature_imp = pd.Series(model_2.feature_importances_,index=headers).sort_values(ascending=False)

f, ax = plt.subplots(figsize=(10, 10))
sns.barplot(x=feature_imp, y=feature_imp.index)

plt.xlabel('Важность атрибутов')
plt.ylabel('Атрибуты')
plt.title("Наиболее важные атрибуты")
plt.show()


# In[387]:


print ('Точность предсказания модели:', round(model_2.score(X_2_test, y_2_test),2)*100,'%')


# In[194]:


VLE.activity_type.unique()


# In[539]:


activity_type = activity_table.merge(VLE[['id_site','activity_type']], on = 'id_site', how = 'left').merge(students[['code_module','code_presentation','id_student','final_result']], how='left', on =['code_module','code_presentation','id_student']).groupby(['code_module','final_result','activity_type']).agg({'sum_click': 'sum'}).reset_index()


# In[540]:


activity_type=activity_type.merge (activity_type.groupby(['code_module','final_result']).sum().reset_index(),                                   on=['code_module','final_result'])
activity_type['%']=round(activity_type.sum_click_x/activity_type.sum_click_y*100,2)


# In[550]:


activity_type_graph = pd.pivot_table(activity_type, values='%', index=['code_module','final_result'],                                 columns=['activity_type'],  aggfunc=sum, fill_value=0)
activity_type_graph.loc['AAA']


# In[556]:


activity_type_graph.plot.barh(stacked=True,figsize=(15,8) )
plt.xlabel('Доля кликов', fontsize =12)
plt.ylabel('Группа студентов', fontsize =12)
plt.title('Распределение кликов по разным ресурсам')
plt.legend(bbox_to_anchor=(1, 0.61))


plt.show()


# In[264]:


activity_type=activity_table.merge(VLE.iloc[:,:-2], how ='left', on =['code_module','code_presentation','id_site'])
activity_type_1=activity_type.groupby(['code_module','code_presentation','id_student','activity_type']).agg({'sum_click':'sum'}).reset_index()
activity_type_1.head()


# In[267]:


activity_type_1.columns=['code_module','code_presentation','id_student','activity_type','sourses_sum_click']
activity_type_1= pd.pivot_table(activity_type_1, values=['sourses_sum_click'], index=['code_module','id_student'],                                 columns=['activity_type'],fill_value=0)


# In[268]:


activity_type_2= activity_type_1.reset_index()
activity_type_2.columns=['code_module','id_student','dataplus','dualpane','externalquiz', 'forumng', 'glossary', 'homepage', 'oucollaborate', 'oucontent', 'ouelluminate', 'ouwiki','page', 'questionnaire','quiz','resource', 'sharedsubpage','subpage','url']


# In[269]:


activity_type_2.head()

