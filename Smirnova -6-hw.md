
# Задание 1
#### Скачайте с сайта https://grouplens.org/datasets/movielens/ датасет любого размера. Определите какому фильму было выставлено больше всего оценок 5.0.


```python
import pandas as pd
```


```python
data = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\ratings.csv')

rating_5= data[ (data['rating'] == 5.0)]
movie_id = rating_5.groupby('movieId').count()[['rating']].sort_values('rating', ascending = False)

movies = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\movies.csv')

joined = movie_id.merge(movies, on = 'movieId',how = 'left')
joined.title[0]
```




    'Shawshank Redemption, The (1994)'



# Задание 2
#### По данным файла power.csv посчитайте суммарное потребление стран Прибалтики (Латвия, Литва и Эстония) категорий 4, 12 и 21 за период с 2005 по 2010 года. Не учитывайте в расчетах отрицательные значения quantity.


```python
power = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\power.csv')

filtered_data = power[ ((power['country']=='Latvia') | (power['country']=='Lithuania') | (power['country']=='Estonia')) \
    & ( ( (power['category']== 4)) |(power['category']== 12) | (power['category']== 21)) \
    & (( power['year'].between(2005, 2010, inclusive= True))) \
    & ((power['quantity'] >= 0))]

total_sum_quantity = sum(filtered_data['quantity'])

total_sum_quantity
```




    240580.0



# Задание 3
#### Выберите страницу любого сайта с табличными данными. Импортируйте таблицы в pandas dataframe.
#### Примеры страниц (необязательно брать именно эти): 
https://fortrader.org/quotes
https://www.finanz.ru/valyuty/v-realnom-vremeni


```python
pd.read_html('https://www.hse.ru/sveden/education')[1]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>0</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5</th>
      <th>6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Класс обучения</td>
      <td>Профиль (направление) обучения</td>
      <td>Уровень образования</td>
      <td>Срок действия государственной аккредитации (да...</td>
      <td>Языки, на которых осуществляется образование (...</td>
      <td>Форма обучения</td>
      <td>Нормативный срок обучения</td>
    </tr>
    <tr>
      <th>1</th>
      <td>10-11 класс</td>
      <td>Востоковедение</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>2</th>
      <td>10-11 класс</td>
      <td>Гуманитарные науки</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>3</th>
      <td>10-11 класс</td>
      <td>Дизайн</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>4</th>
      <td>10-11 класс</td>
      <td>Математика, информатика и инженерия</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>5</th>
      <td>10-11 класс</td>
      <td>Психология</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10-11 класс</td>
      <td>Экономика и математика</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>7</th>
      <td>10-11 класс</td>
      <td>Экономика и социальные науки</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>8</th>
      <td>10-11 класс</td>
      <td>Юриспруденция</td>
      <td>Среднее общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>2 года</td>
    </tr>
    <tr>
      <th>9</th>
      <td>9 класс</td>
      <td>NaN</td>
      <td>Основное общее образование</td>
      <td>до 30.03.2028</td>
      <td>Русский язык</td>
      <td>Очная</td>
      <td>1 год</td>
    </tr>
  </tbody>
</table>
</div>


