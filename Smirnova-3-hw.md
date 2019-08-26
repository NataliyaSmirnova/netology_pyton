
## Задание 1

Дан список вида:


```python
data = [
    [13, 25, 23, 34],
    [45, 32, 44, 47],
    [12, 33, 23, 95],
    [13, 53, 34, 35]
]

def sum_():
    sum_x=[]
    for ind, i in enumerate(data):
        sum_x.append(i[ind])
    return sum(sum_x)
sum_()

    

```




    103



Напишите функцию, которая возвращает сумму элементов на диагонали. Т. е. 13+32+23+35.

## Задание 2

Дан список чисел, часть из которых имеют строковый тип или содержат буквы. Напишите функцию, которая возвращает сумму квадратов элементов, которые могут быть числами.


```python
data = [1, '5', 'abc', 20, '2']
 


def sum_of_square():
    data_=[]
    
    for i in data:
        i_str = str(i)
        if 'a' <= i_str <= 'z':
            continue
        if '-9' <= i_str <= '9':
            i_int=int(i_str)
            data_.append(i_int**2)
    return sum(data_)
        
sum_of_square()
    
```




    430



## Задание 3

Напишите функцию, возвращающую сумму первых n чисел Фибоначчи.


```python
n = int(input('Введите порядковый номер'))
def fibonacci(n):
    if n in (1,2):
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)
def sum_fibonacci(n):
    fibonacci_list=[]
    while n>=1:
        fibonacci_list.append(fibonacci(n)) 
        n-=1
    return sum(fibonacci_list)
sum_fibonacci(n)
```

    Введите порядковый номер6
    




    20



## Задание 4

Дан набор данных об обучении студентов на курсе программирования, который содержит: 
1) имя
2) фамилию 
3) пол 
4) наличие у студента опыта в программировании 
5) набор оценок за домашние работы 
6) оценку за итоговую работу.

Напишите программу, которая будет принимать команду от пользователя и возвращать соотвествующий результат.
Список команд: 
1 - вывести на экран среднюю оценку за все ДЗ по группе и вывести на экран среднюю оценку за экзамен по группе;
2 - вывести среднюю оценку за ДЗ и за экзамен по группе в разрезе пола студентов
3 - вывести среднюю оценку за ДЗ и за экзамен в разрезе наличия опыта в программировании у студентов.

Прогрмма должна быть полностью декомпозирована на функции (кроме объявления функций и вызова итоговой функции в реализации ничего быть не должно).


```python
students_list = [
    {'name': 'Василий', 'surname': 'Теркин', 'sex': 'м', 'program_exp': True, 'grade': [8, 8, 9, 10, 9], 'exam': 9},
    {'name': 'Мария', 'surname': 'Павлова', 'sex': 'ж', 'program_exp': True, 'grade': [7, 8, 9, 7, 9], 'exam': 8},
    {'name': 'Ирина', 'surname': 'Андреева', 'sex': 'ж', 'program_exp': True, 'grade': [10, 9, 8, 10, 10], 'exam': 10},
    {'name': 'Татьяна', 'surname': 'Сидорова', 'sex': 'ж', 'program_exp': True, 'grade': [7, 8, 8, 9, 8], 'exam': 8},
    {'name': 'Иван', 'surname': 'Васильев', 'sex': 'ж', 'program_exp': True, 'grade': [9, 8, 9, 6, 9], 'exam': 10},
    {'name': 'Роман', 'surname': 'Золотарев', 'sex': 'ж', 'program_exp': False, 'grade': [8, 9, 9, 6, 9], 'exam': 10}
]

sum_hwgrade=[]
sum_exgrade=[]
count_hwgrade=[]
def av_grade_in_group(): 
    n=0
    for d in students_list:
        sum_hwgrade.append(sum((students_list[n])['grade']))
        count_hwgrade.append(len((students_list[n])['grade']))
        sum_exgrade.append(students_list[n]['exam'])
        n+=1
    return round((sum(sum_hwgrade)/ sum(count_hwgrade)),2) , round(sum(sum_exgrade)/len(sum_exgrade),2)

m_hwgrade=[]
m_cont_hwgrade=[]
m_exgrade=[]
w_hwgrade=[]
w_cont_hwgrade=[]
w_exgrade=[]
def av_grade_by_sex():
    n=0
    for d in students_list: 
        if (students_list[n])['sex'] == 'м':
            m_hwgrade.append(sum((students_list[n])['grade']))
            m_exgrade.append(students_list[n]['exam'])
            m_cont_hwgrade.append((len((students_list[n])['grade'])))
        else:
            w_hwgrade.append(sum((students_list[n])['grade']))
            w_exgrade.append(students_list[n]['exam'])
            w_cont_hwgrade.append((len((students_list[n])['grade'])))
        n+=1
    return sum(m_hwgrade)/sum(m_cont_hwgrade), sum(m_exgrade)/len(m_exgrade), sum(w_hwgrade)/sum(w_cont_hwgrade), sum(w_exgrade)/len(w_exgrade)

exp_hwgrade=[]
exp_cont_hwgrade=[]
exp_exgrade=[]
noexp_hwgrade=[]
noexp_cont_hwgrade=[]
noexp_exgrade=[]
def av_grade_by_exp():
    n=0
    for d in students_list:
        if (students_list[n])['program_exp'] == True:
            exp_hwgrade.append(sum((students_list[n])['grade']))
            exp_exgrade.append(students_list[n]['exam'])
            exp_cont_hwgrade.append((len((students_list[n])['grade'])))
        else:
            noexp_hwgrade.append(sum((students_list[n])['grade']))
            noexp_exgrade.append(students_list[n]['exam'])
            noexp_cont_hwgrade.append((len((students_list[n])['grade'])))
        n+=1
    return (sum(exp_hwgrade)/sum(exp_cont_hwgrade),sum(exp_exgrade)/len(exp_exgrade), sum(noexp_hwgrade)/sum(noexp_cont_hwgrade), sum(noexp_exgrade)/len(noexp_exgrade))



def output():
    x= int(input("""Введите номер команды, которую необходимо выполнить. 
1 - вывести среднюю оценку за все ДЗ и экзамен в группе
2 - вывести среднюю оценку за все ДЗ и экзамен в зависимости от пола студентов
3 - вывести среднюю оценку за все ДЗ и экзамен в зависимости от наличия опыа программирования

"""))
    if x == 1:
        return print('Средняя оценка за ДЗ в группе -', av_grade_in_group()[0],"\n"
                     'Средняя оценка за экзамен в группе -', av_grade_in_group()[1] )
    elif x == 2:
        return print('Средняя оценка за ДЗ среди лиц мужского пола -', av_grade_by_sex()[0], "\n"
                     'Средняя оценка за экзамен среди лиц мужского пола -', av_grade_by_sex()[1], "\n"
                    'Средняя оценка за ДЗ среди лиц женского пола -', av_grade_by_sex()[2], "\n"
                     'Средняя оценка за экзамен среди лиц женского пола -', av_grade_by_sex()[3])
    elif x == 3:
        return print('Средняя оценка за ДЗ у студентов с опытом программирования -', av_grade_by_exp()[0], "\n"
                     'Средняя оценка за экзамен у студентов с опытом программирования -', av_grade_by_exp()[1], "\n"
                    'Средняя оценка за ДЗ у студентов без опыта программирования -', av_grade_by_exp()[2], "\n"
                     'Средняя оценка за экзамен у студентов без опыта программирования -', av_grade_by_exp()[3])
    else:
        return print('Некорректная команда')
output()
```

    Введите номер команды, которую необходимо выполнить. 
    1 - вывести среднюю оценку за все ДЗ и экзамен в группе
    2 - вывести среднюю оценку за все ДЗ и экзамен в зависимости от пола студентов
    3 - вывести среднюю оценку за все ДЗ и экзамен в зависимости от наличия опыа программирования
    
    3
    Средняя оценка за ДЗ у студентов с опытом программирования - 8.48 
    Средняя оценка за экзамен у студентов с опытом программирования - 9.0 
    Средняя оценка за ДЗ у студентов без опыта программирования - 8.2 
    Средняя оценка за экзамен у студентов без опыта программирования - 10.0
    


```python

```
