
## Задание 1

Дан список с визитами по городам и странам. 
Напишите код, который возвращает отфильтрованный список geo_logs, содержащий только визиты из России.


```python
geo_logs = [
    {'visit1': ['Москва', 'Россия']},
    {'visit2': ['Дели', 'Индия']},
    {'visit3': ['Владимир', 'Россия']},
    {'visit4': ['Лиссабон', 'Португалия']},
    {'visit5': ['Париж', 'Франция']},
    {'visit6': ['Лиссабон', 'Португалия']},
    {'visit7': ['Тула', 'Россия']},
    {'visit8': ['Тула', 'Россия']},
    {'visit9': ['Курск', 'Россия']},
    {'visit10': ['Архангельск', 'Россия']}
]
new_list = []
for visit in geo_logs:
    if list(visit.values()) [0][1] == 'Россия':
        new_list.append(visit)
print (new_list) 
```

    [{'visit1': ['Москва', 'Россия']}, {'visit3': ['Владимир', 'Россия']}, {'visit7': ['Тула', 'Россия']}, {'visit8': ['Тула', 'Россия']}, {'visit9': ['Курск', 'Россия']}, {'visit10': ['Архангельск', 'Россия']}]
    

## Задание 2

Выведите на экран все уникальные гео-ID из значений словаря ids. Т. е. список вида [213, 15, 54, 119, 98, 35]


```python
ids = {'user1': [213, 213, 213, 15, 213], 
       'user2': [54, 54, 119, 119, 119], 
       'user3': [213, 98, 98, 35]}
user1 = list(ids.values())[0]
user2 = list(ids.values())[1]
user3 = list(ids.values())[2]

set_user1 = set(user1)
set_user2 = set(user2)
set_user3 = set(user3)
print (set_user1 | set_user2 | set_user3)
```

    {98, 35, 213, 54, 119, 15}
    

## Задание 3

Дан список поисковых запросов. Получить распределение количества слов в них. 
Т. е. поисковых запросов из одного - слова 5%, из двух - 7%, из трех - 3% и т.д.


```python
queries = [
    'смотреть сериалы онлайн',
    'новости спорта',
    'афиша кино',
    'курс доллара',
    'сериалы этим летом',
    'курс по питону',
    'сериалы про спорт'
]
one_word = []
two_words = [] 
three_words = []
for words in queries: 
    words.split(' ') 
    words_amount = (words.count(' ')) + 1 
    if words_amount == 1:
        one_word.append(words_amount)
    elif words_amount == 2:
        two_words.append(words_amount)
    elif words_amount == 3:
        three_words.append(words_amount)
one_word_percent = round((len(one_word) / len(queries) * 100),2)
two_words_percent = round((len(two_words) / len(queries) * 100),2)
three_words_percent = round((len(three_words) / len(queries) * 100),2)
print(one_word_percent , two_words_percent , three_words_percent)
```

    0.0 42.86 57.14
    

## Задание 4

Дана статистика рекламных каналов по объемам продаж. Напишите скрипт, который возвращает название канала с максимальным объемом.
Т. е. в данном примере скрипт должен возвращать 'yandex'.


```python
stats = {'facebook': 55, 'yandex': 120, 'vk': 115, 'google': 99, 'email': 42, 'ok': 98}
max(stats, key=stats.get)

```




    'yandex'



## Задание 5

Дан поток логов по количеству просмотренных страниц для каждого пользователя. Список отсортирован по ID пользователя. Вам необходимо написать алгоритм, который считает среднее значение просмотров на пользователя. 
Т. е. надо посчитать отношение суммы всех просмотров к количеству уникальных пользователей.


```python
stream = [
    '2018-01-01,user1,3',
    '2018-01-07,user1,4',
    '2018-03-29,user1,1',
    '2018-04-04,user1,13',
    '2018-01-05,user2,7',
    '2018-06-14,user3,4',
    '2018-07-02,user3,10',
    '2018-03-21,user4,19',
    '2018-03-22,user4,4',
    '2018-04-22,user4,8',
    '2018-05-03,user4,9',
    '2018-05-11,user4,11',
]
users_set= set()
views_sum= []
for date_views in stream : 
    
    users_set.add(date_views.split(',')[1])
    views = int(date_views.split(',')[2])
    views_sum.append(views)
print ((sum(views_sum)) / (len(users_set)))
    
```

    23.25
    

## Задание 6

Дана статистика рекламных кампаний по дням. Напишите алгоритм, который по паре дата-кампания ищет значение численного столбца. 
Т. е. для даты '2018-01-01' и 'google' нужно получить число 25. 
Считайте, что все комбинации дата-кампания уникальны.


```python
stats = [
    ['2018-01-01', 'google', 25],
    ['2018-01-01', 'yandex', 65],
    ['2018-01-01', 'market', 89],
    ['2018-01-02', 'google', 574],
    ['2018-01-02', 'yandex', 249],
    ['2018-01-02', 'market', 994],
    ['2018-01-03', 'google', 1843],
    ['2018-01-03', 'yandex', 1327],
    ['2018-01-03', 'market', 1764],
]
date = input ('Введите дату')
company = input ('Введите компанию')
for elements in stats:
    if company == elements[1] and date == elements[0]:
        print (elements[2])
   
```

    Введите дату2018-01-02
    Введите компаниюmarket
    994
    


```python

```
