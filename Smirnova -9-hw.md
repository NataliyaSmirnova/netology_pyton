
### Задание 1
Напишите функцию date_range, которая возвращает список дней между датами start_date и end_date. Даты должны вводиться в формате YYYY-MM-DD.


```python
from datetime import datetime
from datetime import timedelta
```

#### Вариант1
Начальная и конечная даты задаются через input

Есть проверка на корректность формата даты

В случае некорректной даты выдается запись: 'Неправильный формат даты'

В этом варианте формат корректный


```python
list_=[]
def date_range():
    start_date = input('Введите начало периода в формате ГГГГ-ММ-ДД: ')
    end_date = input('Введите конец периода в формате ГГГГ-ММ-ДД: ')
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return 'Неправильный формат даты'
    
    current_date = start_date
    
    while current_date <= end_date:
        list_.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    
    return list_
    
    
date_range()
```

    Введите начало периода в формате ГГГГ-ММ-ДД: 2019-02-03
    Введите конец периода в формате ГГГГ-ММ-ДД: 2019-02-10
    




    ['2019-02-03',
     '2019-02-04',
     '2019-02-05',
     '2019-02-06',
     '2019-02-07',
     '2019-02-08',
     '2019-02-09',
     '2019-02-10']



#### Вариант2
Начальная и конечная даты задаются в аргументе функции

Есть проверка на корректность формата даты

В случае некорректной даты выдается запись: 'Неправильный формат даты'

В этом варианте формат неверный


```python
list_=[]
def date_range(start_date, end_date): 
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return 'Неправильный формат даты'
    
    current_date = start_date
    
    while current_date <= end_date:
        list_.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)
    return list_

date_range('23525', '2252')
```




    'Неправильный формат даты'



### Задание 2
Дополните функцию из первого задания проверкой на корректность дат. В случае неверного формата или если start_date > end_date должен возвращаться пустой список


```python
list_=[]
def date_range(start_date, end_date): 
    
    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except:
        return list_
    
    current_date = start_date
    
    if start_date > end_date:
        return list_
    else:
        while current_date <= end_date:
            list_.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
    return list_

date_range('2019-02-03', '2019-02-10')
```




    ['2019-02-03',
     '2019-02-04',
     '2019-02-05',
     '2019-02-06',
     '2019-02-07',
     '2019-02-08',
     '2019-02-09',
     '2019-02-10']



### Задание 3
Дан поток дат в формате YYYY-MM-DD, в которых встречаются некорректные значения:
stream = ['2018-04-02', '2018-02-29', '2018-19-02']

Напишите функцию, которая проверяет эти даты на корректность. Т. е. для каждой даты возвращает True (дата корректна) или False (некорректная дата). 


```python
stream = ['2018-04-02', '2018-02-29', '2018-19-02']
stream_dict={}
def verification ():
    for dates in stream:
        try:
            datetime.strptime(dates, '%Y-%m-%d')
            stream_dict.setdefault(dates, True)
        except:
            stream_dict.setdefault(dates, False)
    return stream_dict
verification()
```




    {'2018-04-02': True, '2018-02-29': False, '2018-19-02': False}



### Задание 4
В последнем примере поиска по словарю мы использовали 3 столбца. Напишите функцию, которая формирует словарь для поиска по n столбцам.



```python
stats_dict = {}
list_=[]
def find_the_line(*line_to_find):
    n= len(line_to_find)
    
    with open('stats.csv') as f:
        for line in f:  
            line = line.strip().split(',') 
            
            if tuple(line[:n]) not in stats_dict:
                stats_dict.setdefault(tuple(line[:n]), line[n:])
            else:
                if tuple(line[:n]) == line_to_find:
                    return 'Ошибка! Недостаточно данных'
                else:
                    stats_dict.setdefault(tuple(line[:n]), line[n:])
        
        return stats_dict[line_to_find]
 
find_the_line('20', '20552')
```




    ['3', '39156']


