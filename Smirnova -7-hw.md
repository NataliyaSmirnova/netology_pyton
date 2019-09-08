
# Задание 1
### Напишите функцию, которая классифицирует фильмы из материалов занятия по следующим правилам:
##### - оценка 2 и меньше - низкий рейтинг
##### - оценка 4 и меньше - средний рейтинг
##### - оценка 4.5 и 5 - высокий рейтинг

### Результат классификации запишите в столбец class


```python
import pandas as pd
data = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\ratings_small.csv')
data.head()

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
      <th>userId</th>
      <th>movieId</th>
      <th>rating</th>
      <th>timestamp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>4.0</td>
      <td>964982703</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>3</td>
      <td>4.0</td>
      <td>964981247</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>6</td>
      <td>4.0</td>
      <td>964982224</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>47</td>
      <td>5.0</td>
      <td>964983815</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>50</td>
      <td>5.0</td>
      <td>964982931</td>
    </tr>
  </tbody>
</table>
</div>




```python
def classification(a):
    if a ['rating'] <= 2.0:
        return 'low_rating'
    elif a ['rating'] <= 4.0:
        return 'middle_rating'
    return 'high_rating'
data['class'] = data.apply(classification, axis=1)
data.head()
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
      <th>userId</th>
      <th>movieId</th>
      <th>rating</th>
      <th>timestamp</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>4.0</td>
      <td>964982703</td>
      <td>middle_rating</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>3</td>
      <td>4.0</td>
      <td>964981247</td>
      <td>middle_rating</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>6</td>
      <td>4.0</td>
      <td>964982224</td>
      <td>middle_rating</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>47</td>
      <td>5.0</td>
      <td>964983815</td>
      <td>high_rating</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>50</td>
      <td>5.0</td>
      <td>964982931</td>
      <td>high_rating</td>
    </tr>
  </tbody>
</table>
</div>



# Задание 2
### Используем файл keywords.csv.

### Необходимо написать гео-классификатор, который каждой строке сможет выставить географическую принадлежность определенному региону. Т. е. если поисковый запрос содержит название города региона, то в столбце 'region' пишется название этого региона. Если поисковый запрос не содержит названия города, то ставим 'undefined'.

#### Правила распределения по регионам Центр, Северо-Запад и Дальний Восток:

geo_data = {

    'Центр': ['москва', 'тула', 'ярославль'],

    'Северо-Запад': ['петербург', 'псков', 'мурманск'],

    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']

}

#### Результат классификации запишите в отдельный столбец region.



```python
df = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\keywords.csv')

```


```python
geo_data = {

    'Центр': ['москва', 'тула', 'ярославль'],

    'Северо-Запад': ['петербург', 'псков', 'мурманск'],

    'Дальний Восток': ['владивосток', 'сахалин', 'хабаровск']
}

def region(a):
    for city in geo_data['Центр']:
        if city in a['keyword'].lower():
            return list(geo_data.keys())[0]
    for city in geo_data['Северо-Запад']:
        if city in a['keyword'].lower():
            return list(geo_data.keys())[1]
    for city in geo_data['Дальний Восток']:
        if city in a['keyword'].lower():
            return list(geo_data.keys())[2]
    return 'Undefined'
df['region'] = df.apply(region, axis=1)
df.head()
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
      <th>keyword</th>
      <th>shows</th>
      <th>region</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>вк</td>
      <td>64292779</td>
      <td>Undefined</td>
    </tr>
    <tr>
      <th>1</th>
      <td>одноклассники</td>
      <td>63810309</td>
      <td>Undefined</td>
    </tr>
    <tr>
      <th>2</th>
      <td>порно</td>
      <td>41747114</td>
      <td>Undefined</td>
    </tr>
    <tr>
      <th>3</th>
      <td>ютуб</td>
      <td>39995567</td>
      <td>Undefined</td>
    </tr>
    <tr>
      <th>4</th>
      <td>вконтакте</td>
      <td>21014195</td>
      <td>Undefined</td>
    </tr>
  </tbody>
</table>
</div>



# Задание 3
### Есть мнение, что "раньше снимали настоящее кино, не то что сейчас". Ваша задача проверить это утверждение, используя файлы с рейтингами фильмов из материалов занятия. Т. е. проверить верно ли, что с ростом года выпуска фильма его средний рейтинг становится ниже.

#### При этом мы не будем затрагивать субьективные факторы выставления этих рейтингов, а пройдемся по следующему алгоритму:

1. В переменную years запишите список из всех годов с 1950 по 2010.

2. Напишите функцию production_year, которая каждой строке из названия фильма выставляет год выпуска. Не все названия фильмов содержат год выпуска в одинаковом формате, поэтому используйте следующий алгоритм:
	- для каждой строки пройдите по всем годам списка years
	- если номер года присутствует в названии фильма, то функция возвращает этот год как год выпуска
	- если ни один из номеров года списка years не встретился в названии фильма, то возвращается 1900 год

3. Запишите год выпуска фильма по алгоритму пункта 2 в новый столбец 'year'

4. Посчитайте средний рейтинг всех фильмов для каждого значения столбца 'year' и отсортируйте результат по убыванию рейтинга


```python
movies = pd.read_csv(r'C:\Users\Natalia\Documents\Аналитик данных\Pyton\Практика\movies_small.csv')
movies
years=list(range(1950, 2011))

def production_year(a):
    for year in years:
        if (str(year)) in a['title']:
            return year
    return 'Not in range'
movies['year'] = movies.apply(production_year, axis=1)
joined = movies.merge(data, on = 'movieId',how = 'left')
year1950_2010= joined[joined['year']!= 'Not in range']
year1950_2010.groupby('year').mean()[['rating']].sort_values('rating', ascending = False)
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
      <th>rating</th>
    </tr>
    <tr>
      <th>year</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1957</th>
      <td>4.039535</td>
    </tr>
    <tr>
      <th>1954</th>
      <td>4.009191</td>
    </tr>
    <tr>
      <th>1962</th>
      <td>3.969466</td>
    </tr>
    <tr>
      <th>1952</th>
      <td>3.953125</td>
    </tr>
    <tr>
      <th>1972</th>
      <td>3.944293</td>
    </tr>
    <tr>
      <th>1964</th>
      <td>3.940160</td>
    </tr>
    <tr>
      <th>1974</th>
      <td>3.935622</td>
    </tr>
    <tr>
      <th>1967</th>
      <td>3.922572</td>
    </tr>
    <tr>
      <th>1975</th>
      <td>3.879121</td>
    </tr>
    <tr>
      <th>1958</th>
      <td>3.842424</td>
    </tr>
    <tr>
      <th>1971</th>
      <td>3.841463</td>
    </tr>
    <tr>
      <th>1966</th>
      <td>3.823684</td>
    </tr>
    <tr>
      <th>1950</th>
      <td>3.813665</td>
    </tr>
    <tr>
      <th>1968</th>
      <td>3.812212</td>
    </tr>
    <tr>
      <th>1977</th>
      <td>3.810406</td>
    </tr>
    <tr>
      <th>1951</th>
      <td>3.804945</td>
    </tr>
    <tr>
      <th>1959</th>
      <td>3.794239</td>
    </tr>
    <tr>
      <th>1981</th>
      <td>3.760732</td>
    </tr>
    <tr>
      <th>1976</th>
      <td>3.760047</td>
    </tr>
    <tr>
      <th>1973</th>
      <td>3.757764</td>
    </tr>
    <tr>
      <th>1970</th>
      <td>3.754098</td>
    </tr>
    <tr>
      <th>1965</th>
      <td>3.735043</td>
    </tr>
    <tr>
      <th>1980</th>
      <td>3.733581</td>
    </tr>
    <tr>
      <th>1960</th>
      <td>3.721116</td>
    </tr>
    <tr>
      <th>1955</th>
      <td>3.719780</td>
    </tr>
    <tr>
      <th>1961</th>
      <td>3.700000</td>
    </tr>
    <tr>
      <th>1969</th>
      <td>3.682648</td>
    </tr>
    <tr>
      <th>1956</th>
      <td>3.682609</td>
    </tr>
    <tr>
      <th>1979</th>
      <td>3.676845</td>
    </tr>
    <tr>
      <th>1953</th>
      <td>3.647059</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
    </tr>
    <tr>
      <th>1963</th>
      <td>3.628920</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>3.569096</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>3.568966</td>
    </tr>
    <tr>
      <th>1991</th>
      <td>3.552265</td>
    </tr>
    <tr>
      <th>1984</th>
      <td>3.529493</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>3.528126</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>3.522433</td>
    </tr>
    <tr>
      <th>1982</th>
      <td>3.510921</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>3.507227</td>
    </tr>
    <tr>
      <th>1994</th>
      <td>3.500944</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>3.499033</td>
    </tr>
    <tr>
      <th>1999</th>
      <td>3.498677</td>
    </tr>
    <tr>
      <th>1987</th>
      <td>3.488312</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>3.482125</td>
    </tr>
    <tr>
      <th>1989</th>
      <td>3.463061</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>3.462321</td>
    </tr>
    <tr>
      <th>1986</th>
      <td>3.460152</td>
    </tr>
    <tr>
      <th>1978</th>
      <td>3.455102</td>
    </tr>
    <tr>
      <th>1993</th>
      <td>3.452152</td>
    </tr>
    <tr>
      <th>1995</th>
      <td>3.443848</td>
    </tr>
    <tr>
      <th>1985</th>
      <td>3.434115</td>
    </tr>
    <tr>
      <th>1990</th>
      <td>3.427310</td>
    </tr>
    <tr>
      <th>1998</th>
      <td>3.427186</td>
    </tr>
    <tr>
      <th>1988</th>
      <td>3.419032</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>3.414584</td>
    </tr>
    <tr>
      <th>2000</th>
      <td>3.398922</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>3.359976</td>
    </tr>
    <tr>
      <th>1992</th>
      <td>3.353555</td>
    </tr>
    <tr>
      <th>1997</th>
      <td>3.347241</td>
    </tr>
    <tr>
      <th>1996</th>
      <td>3.335329</td>
    </tr>
  </tbody>
</table>
<p>61 rows × 1 columns</p>
</div>


