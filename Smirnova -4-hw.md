
# Задание 1

#### Напишите функцию, которая возвращает название валюты (поле 'Name') с максимальным значением курса с помощью сервиса https://www.cbr-xml-daily.ru/daily_json.js


```python
import requests
```


```python
class Rate:
    def __init__(self, format_='value'):
        self.format = format_
    
    def exchange_rates(self):
        """
        Возвращает ответ сервиса с информацией о валютах в виде:
        
        {
            'AMD': {
                'CharCode': 'AMD',
                'ID': 'R01060',
                'Name': 'Армянских драмов',
                'Nominal': 100,
                'NumCode': '051',
                'Previous': 14.103,
                'Value': 14.0879
                },
            ...
        }
        """
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        return r.json()['Valute']
    
    def max_valute(self):
        
        """
        Возвращает наименование валюты с максимальным значением курса
        """
        
        dict_ = self.exchange_rates()
        value_name={}
        for i in list(dict_.values()):
            value_name.setdefault(i['Value'],i['Name'])
        return (value_name[max(value_name)])
                       
r= Rate()
r.max_valute()

```




    'Датских крон'



# Задание 2

#### Добавьте в класс Rate параметр diff (со значениями True или False), который в случае значения True в методах eur и usd будет возвращать не курс валюты, а изменение по сравнению в прошлым значением. Считайте, self.diff будет принимать значение True только при возврате значения курса. При отображении всей информации о валюте он не используется.


```python
class Rate:
    def __init__(self, format_, diff):
        self.format = format_
        self.diff = bool(diff)
    
    def exchange_rates(self):
        """
        Возвращает ответ сервиса с информацией о валютах в виде:
        
        {
            'AMD': {
                'CharCode': 'AMD',
                'ID': 'R01060',
                'Name': 'Армянских драмов',
                'Nominal': 100,
                'NumCode': '051',
                'Previous': 14.103,
                'Value': 14.0879
                },
            ...
        }
        """
        r = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        return r.json()['Valute']
    
    def max_valute(self):
        
        """
        Возвращает наименование валюты с максимальным значением курса
        """
        
        dict_ = self.exchange_rates()
        value_name={}
        for i in list(dict_.values()):
            value_name.setdefault(i['Value'],i['Name'])
        return (value_name[max(value_name)])
    
    def make_format(self, currency):
        """
        Возвращает информацию о валюте currency в трех вариантах:
        - полная информация о валюте при self.format = 'full':
        Rate('full').make_format('EUR')
        {
            'CharCode': 'EUR',
            'ID': 'R01239',
            'Name': 'Евро',
            'Nominal': 1,
            'NumCode': '978',
            'Previous': 79.6765,
            'Value': 79.4966
        }
        - значение валюты при self.format = 'Value' и self.diff = False:
        Rate('value', False).make_format('EUR')
        79.4966
        - разница настоящего и предыдущего значений курса при self.format = 'Value' и self.diff = True:
        Rate('value', True).make_format('EUR')
        -0.57
        """
        response = self.exchange_rates()
        
        if currency in response:
            if self.format == 'full':
                return response[currency]
            
            if self.format == 'value':
                if self.diff == False:
                    return response[currency]['Value']
                elif self.diff == True:
                    return round(response[currency]['Value'] - response[currency]['Previous'],2)
        
        return 'Error'
    
    def eur(self):
        """Возвращает курс евро на сегодня в формате self.format"""
        return self.make_format('EUR')
    
    def usd(self):
        """Возвращает курс доллара на сегодня в формате self.format"""
        return self.make_format('USD')

r = Rate('value', True)
r.eur()
```




    -0.57



# Домашнее задание задача 3

Напишите класс Designer, который учитывает количество международных премий для дизайнеров. Считайте, что при выходе на работу сотрудник уже имеет две премии и их количество не меняется со стажем (конечно если хотите это можно вручную менять). Выполните проверку для 20 аккредитаций дизайнера Елены.


```python
class Employee:
    def __init__(self, name, seniority):
        self.name = name
        self.seniority = seniority
        
        self.grade = 1
    
    def grade_up(self):
        """Повышает уровень сотрудника"""
        self.grade += 1
    
    def publish_grade(self):
        """Публикация результатов аккредитации сотрудников"""
        print(self.name, self.grade)
        
class Designer(Employee):
    def __init__(self, name, seniority, awards=2):
        super().__init__(name, seniority)
        self.awards = awards
    
    
    def check_if_it_is_time_for_upgrade(self):
        self.seniority += 1
        
        if (self.seniority + self.awards*2) % 7 == 0:
            self.grade_up()
        
        # публикация результатов
        return self.publish_grade()
    

```


```python
elena = Designer('Елена', 0)
```


```python
for i in range(20):
    elena.check_if_it_is_time_for_upgrade()
```

    Елена 1
    Елена 1
    Елена 2
    Елена 2
    Елена 2
    Елена 2
    Елена 2
    Елена 2
    Елена 2
    Елена 3
    Елена 3
    Елена 3
    Елена 3
    Елена 3
    Елена 3
    Елена 3
    Елена 4
    Елена 4
    Елена 4
    Елена 4
    
