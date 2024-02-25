# Отчет о тестировании класса VendingMachine

## Обзор проекта
В качестве фреймворка unit-test'ов используется `pytest` (с плагином `pytest-timeout`).  
В качестве фреймворка проверки покрытия кода используется `coverage`.  

- `./coverage/`: папка с `html` отчетом о покрытии кода тестированием.
- `./src/`: папка с исходниками и тестами.
- `./.coveragerc`: конфигурационный файл для `coverage`.
- `./requirements.txt`: полный список зависимостей.

Используйте `pip install -r requirements.txt` для установки всех зависимостей.  

## Создание отчета покрытия кода тестированием
Используйте `$ make generate_coverage_report` для создания отчета покрытия кода. Будут проанализированы `./src/VendingMachine.py` и `./src/test_vendingmachine.py`. Отчет будет помещен в папку `./coverage/`.  
Для очистки папки с отчетом используйте `$ make clear_coverage`.  

## Обзор отчета
Удалось добиться 97% покрытия кода `VendingMachine.py` тестами.  
При этом, остались непокрытыми только те строки, которые были показаны, что недостижимы (см. "Недостижимый код"). Частично проверенные условия остались только в тех строках, которые были показаны, что никогда не выполняются.

## Найденные ошибки

### Замечание
В некоторых тестах полагаем, что мы позвали администратора и он сказал нам эталонный код, который мы теперь знаем. 

### Ошибка #1 

**Код до исправления**  
```python
def getCoins2(self):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return self.coins1
    return self.__coins2
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode == VendingMachine.Mode.OPERATION`, то при любых остальных входных данных при вызове функции `getCoins2(self)`, вызовется необработанное исключение.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
machine.exitAdminMode() # Удостоверяемся, что автомат находится в рабочем режиме.
machine.getCoins2()
```

**Полученное значение**  
Исключение: `AttributeError: 'VendingMachine' object has not attribute 'coins1'`.

**Ожидаемое значение**  
Значение `self.__coins1` *(видимо, ожидается, 0, но об этом далее)*

**Код после исправления**  
```python
def getCoins2(self):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return self.__coins1
    return self.__coins2
```









### Ошибка #2

**Код до исправления**  
```python
def enterAdminMode(self, code: int):
    if self.__balance != 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    if code != self.__id:
        return VendingMachine.Response.INVALID_PARAM
    self.__mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__balance != 0 and code != self.__id`, то метод вернет `VendingMachine.Response.UNSUITABLE_CHANGE`, хотя пункт i. требует вернуть `VendingMachine.Response.ILLEGAL_OPERATION` сначала, при несовпадении кодов.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Добавляем монету в баланс, удостоверяясь, что баланс точно ненулевой.
machine.putCoin1()
# Ожидаем, что при неправильном коде сначала должно вернуться VendingMachine.Response.INVALID_PARAM.
response = machine.enterAdminMode(1)
if response != VendingMachine.Response.OK:
    print(response == VendingMachine.Response.INVALID_PARAM)
# Но если мы угадали код, то возможно ошибка в другом.
# Проверим другой код, логично предположив, что только единственный код может быть верным.
# Заметим, что нам не нужно выходить из режима администратора, т. к. в требованиях не указано, 
# что нужно быть в рабочем режиме, чтобы войти в режим администратора.
else:
    print(machine.enterAdminMode(2) == VendingMachine.Response.INVALID_PARAM)
```
Заметим, что воспроизведение не зависит от начального баланса и кода.

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def enterAdminMode(self, code: int):
    if code != self.__id:
        return VendingMachine.Response.INVALID_PARAM
    if self.__balance != 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    self.__mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```









### Ошибка #3

**Код до исправления**  
```python
def enterAdminMode(self, code: int):
    if code != self.__id:
        return VendingMachine.Response.INVALID_PARAM
    if self.__balance != 0:
        return VendingMachine.Response.UNSUITABLE_CHANGE
    self.__mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `code == self.__id and self.__balance != 0`, то метод вернет `VendingMachine.Response.UNSUITABLE_CHANGE`, хотя пункт i. требует вернуть `VendingMachine.Response.CANNOT_PERFORM` при совпадении кодов и ненулевом балансе.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Удостоверяемся, что баланс ненулевой.
machine.putCoin1()
# Зовем администратора, который дает нам эталонный код.
# Ожидается, что вернется CANNOT_PERFORM.
print(machine.enterAdminMode(117345294655382) == VendingMachine.Response.CANNOT_PERFORM) 
```

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def enterAdminMode(self, code: int):
    if code != self.__id:
        return VendingMachine.Response.INVALID_PARAM
    if self.__balance != 0:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__mode = VendingMachine.Mode.ADMINISTERING
    return VendingMachine.Response.OK
```










### Ошибка #4

**Код до исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins2 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins2 != self.__maxc2`, то метод не увеличит количество 1-го вида монет в автомате, хотя пункт o. требует этого. Это проверяется методом `getCoins1()`, который пункт f. требует возвращать количество монет 1-го вида вне режима отладки.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Внесем одну монету 1-го типа.
machine.putCoin1()
# Попытаемся вернуть деньги.
# Будем условиться, что мы знаем реализацию putCoin1() и баги в ней.
# То есть, мы знаем, что сейчас на балансе 2 у.е., но, в теории,
# внесена только одна монета 1-го типа.
# Таким образом, ожидается, что вернется TOO_BIG_CHANGE (что неверно).
print(machine.returnMoney() == VendingMachine.Response.TOO_BIG_CHANGE)
```

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins1 += 1
    return VendingMachine.Response.OK
```







### Ошибка #5

**Код до исправления**  
```python
def getCoins2(self):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return self.__coins1
    return self.__coins2
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode == VendingMachine.Mode.OPERATION`, то метод вернет количество монет 1-го вида, хотя пункт g. требует вернуть `0`.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Кладя монету 1-го вида в автомат, мы удостоверяемся, что монет 1-го вида не может быть ноль,
# а, соответственно, мы можем различить ситуации, когда количество монет 1-го вида равно нулю
# (и по "воле случая" возвращается правильный ответ), и когда буквально возвращается ноль.
machine.putCoin1() 
print(machine.getCoins2())
```

**Полученное значение**  
В `stdout` выведется `1`.

**Ожидаемое значение**  
В `stdout` должно вывестись `0`.

**Код после исправления**  
```python
def getCoins2(self):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return 0
    return self.__coins2
```











### Ошибка #6

**Код до исправления**  
```python
def fillProducts(self):
    self.__num1 = self.__max2
    self.__num2 = self.__max2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Метод возвращает `VendingMachine.Response.OK` при любом режиме автомата, хотя пункт j. требует вернуть `VendingMachine.Response.ILLEGAL_OPERATION` в режиме отличном от отладки.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Удостоверимся, что автомат не в режиме отладки.
machine.exitAdminMode()
# Ожидается, что вернется VendingMachine.Response.ILLEGAL_OPERATION.
print(machine.fillProducts() == VendingMachine.Response.ILLEGAL_OPERATION)
```

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def fillProducts(self):
    if self.__mode != VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    self.__num1 = self.__max2
    self.__num2 = self.__max2
    return VendingMachine.Response.OK
```










### Ошибка #7

**Код до исправления**  
```python
def fillProducts(self):
    if self.__mode != VendingMachine.Mode.ADMINISTERING: # [fixed].
        return VendingMachine.Response.ILLEGAL_OPERATION
    self.__num1 = self.__max2
    self.__num2 = self.__max2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode == VendingMachine.Mode.ADMINISTERING`, то метод `fillProducts()` увеличит количество продуктов 1-го типа до максимального количества продуктов 2-го типа, хотя пункт j. требует увеличить количество продуктов 1-го типа до максимального количества продуктов 1-го типа.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Заполним автомат продуктами.
machine.fillProducts()
# Исходя из требования j., в max1 должно находится максимальное количество продуктов 1-го типа.
max1 = machine.getNumberOfProduct1()
# Дополнительно проверим, что max1 > 0 (что логично и понадобится далее).
assert max1 > 0
# Тогда, исходя из требования o., мы можем взять max1 продуктов 1-го типа.
# Для этого сначала выйдем из режима отладки.
machine.exitAdminMode()
# Попробуем взять max1 продуктов 1-го типа 
# (на самом деле, в giveProduct1() тоже есть баг, но мы не попадем под него, об этом позже).
# Ожидается, что giveProduct1() не возвратит INVALID_PARAM, т. к. max1 продуктов 1-го типа должно быть в автомате и max1, сейчас, точно больше нуля.
print(machine.giveProduct1(max1) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**  
В `stdout` выведется `True`, что означает, что наш `max1` не равен эталонному максимальному количеству продуктов 1-го типа из автомата, что говорит о том, что в методе `fillProducts()` неправильно заполняется количество продуктов 1-го типа.

**Ожидаемое значение**  
В `stdout` должно вывестись `False`.

**Код после исправления**  
```python
def fillProducts(self):
    if self.__mode != VendingMachine.Mode.ADMINISTERING: # [fixed].
        return VendingMachine.Response.ILLEGAL_OPERATION
    self.__num1 = self.__max1
    self.__num2 = self.__max2
    return VendingMachine.Response.OK
```

**Замечание**
Данное воспроизведение строится только на двух условностях: что `max1` больше нуля (что логично и подразумевается требованиями, иначе мы падаем на assert'е) и что в `giveProduct1()` мы не попадаем под баг, который там есть и связан с воспроизведением. На самом деле, воспроизведение находит баг в fillProducts() в независимости от того, исправлен ли этот баг в `giveProduct1()` или нет. Таким образом, в данном воспроизведении мы только полагаемся на корректность методов `getNumberOfProduct1()`, `exitAdminMode()` (в которых не найдено ошибок), `enterAdminMode()` (в котором исправлены все найденные ошибки), `fillProducts()` (ошибку в котором мы и обозреваем) и `giveProduct1()` (под ошибку которого воспроизведение не попадает, об этом далее).  
P. S. В ходе исследования было обнаружено, что если бы мы сначала рассматривали ошибку в методе `giveProduct1()`, то можно было бы вычислить "эталонный" `max1` (который на самом деле не является эталонным) только и полагаясь на `giveProduct1()`, и на этом как-то построить воспроизведение, однако дальнейшие рассуждения показали, что тогда бы пришлось полагаться на метод `fillProducts()`, под ошибку которого мы обязательно попадаем.  
Далее будем условиться, что эталонный `max1` больше нуля.










### Ошибка #8

**Код до исправления**  
```python
def giveProduct1(self, number: int):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number >= self.__max1:
        return VendingMachine.Response.INVALID_PARAM
    if number > self.__num1:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    ...
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and number > 0 and number == self.__max1`, то метод `giveProduct1()` вернет `VendingMachine.Response.INVALID_PARAM`, хотя пункт r. требует возвращать `VendingMachine.Response.INVALID_PARAM` только если `number` \<= 0 предметов или больше максимума предметов 1-го вида (т. е. выполнение метода должно продолжаться).

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Вычислим максимальное количество продуктов 1-го типа.
machine.fillProducts()
max1 = machine.getNumberOfProduct1()
# Выйдем из режима отладки.
machine.exitAdminMode()
# Попытаемся купить все продукты 1-го типа.
# Ожидается, что не возвратится VendingMachine.Response.INVALID_PARAM.
print(machine.giveProduct1(max1) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**  
В `stdout` выведется `True`.

**Ожидаемое значение**  
В `stdout` должно вывестись `False`.

**Код после исправления**  
```python
def giveProduct1(self, number: int):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number > self.__max1:
        return VendingMachine.Response.INVALID_PARAM
    if number > self.__num1:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    ...
```

**Замечание**
Это и есть тот баг, о котором говорится в ошибке #7.











### Ошибка #9

**Код до исправления**  
```python
def fillCoins(self, c1: int, c2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c2 > self.__maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c1 <= 0 or c2 > self.__maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self.__coins1 = c1
    self.__coins2 = c2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.OPERATION and c1 > 0 and c2 <= 0`, то метод `fillCoins()` возвратит `VendingMachine.Response.OK`, хотя пункт k. требует возвратить `VendingMachine.Response.INVALID_PARAM` при попытке задать `c2` больше максимума монет 2 вида.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Заходим в режим отладки.
machine.enterAdminMode(117345294655382)
# Ожидается, что возвратится INVALID_PARAM, так как второй аргумент неположителен.
print(machine.fillCoins(1, -1) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def fillCoins(self, c1: int, c2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c2 > self.__maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c2 <= 0 or c2 > self.__maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self.__coins1 = c1
    self.__coins2 = c2
    return VendingMachine.Response.OK
```













### Ошибка #10

**Код до исправления**  
```python
def fillCoins(self, c1: int, c2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c2 > self.__maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c2 <= 0 or c2 > self.__maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self.__coins1 = c1
    self.__coins2 = c2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.OPERATION and c1 > 0 and c1 > self.__maxc1 and c2 > 0 and c2 <= self.__maxc2`, то метод `fillCoins()` возвратит `VendingMachine.Response.OK`, хотя пункт k. требует возвратить `VendingMachine.Response.INVALID_PARAM`, если `c1` больше максимума монет 1-го вида.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Переходим в режим отладки.
machine.enterAdminMode(117345294655382)
# Вычислим эталонное значение maxc1. Для этого будем условиться, 
# что мы уже знаем о данном баге, с помощью которого и находим maxc1.
maxc1 = 0
while machine.fillCoins(1, maxc1 + 1) != VendingMachine.Response.INVALID_PARAM:
    maxc1 += 1
# Зная эталонный maxc1, попробуем подать его в качестве 1-го аргумента.
# Ожидается, что возвратится INVALID_PARAM.
print(machine.fillCoins(maxc1 + 1, 1) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**  
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def fillCoins(self, c1: int, c2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if c1 <= 0 or c1 > self.__maxc1:
        return VendingMachine.Response.INVALID_PARAM
    if c2 <= 0 or c2 > self.__maxc2:
        return VendingMachine.Response.INVALID_PARAM
    self.__coins1 = c1
    self.__coins2 = c2
    return VendingMachine.Response.OK
```











### Ошибка #11

**Код до исправления**  
```python
def setPrices(self, p1: int, p2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    self.__price1 = p1
    self.__price2 = p2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.OPERATION and p1 <= 0`, то метод `setPrices()` возвратит `VendingMachine.Response.OK`, хотя пункт n. требует возвратить `VendingMachine.Response.INVALID_PARAM` при попытке установки значений цен меньше или равно `0`.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Переход в режим отладки.
machine.enterAdminMode(117345294655382)
# Ожидается, что вернется INVALID_PARAM.
print(machine.setPrices(0, 1) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def setPrices(self, p1: int, p2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if p1 <= 0:
        return VendingMachine.Response.INVALID_PARAM
    self.__price1 = p1
    self.__price2 = p2
    return VendingMachine.Response.OK
```











### Ошибка #12

**Код до исправления**  
```python
def setPrices(self, p1: int, p2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if p1 <= 0:
        return VendingMachine.Response.INVALID_PARAM
    self.__price1 = p1
    self.__price2 = p2
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.OPERATION and p1 > 0 and p2 <= 0`, то метод `setPrices()` возвратит `VendingMachine.Response.OK`, хотя пункт n. требует возвратить `VendingMachine.Response.INVALID_PARAM` при попытке установки значений цен меньше или равно `0`.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Переход в режим отладки.
machine.enterAdminMode(117345294655382)
# Ожидается, что вернется INVALID_PARAM.
print(machine.setPrices(1, 0) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def setPrices(self, p1: int, p2: int):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if p1 <= 0 or p2 <= 0:
        return VendingMachine.Response.INVALID_PARAM
    self.__price1 = p1
    self.__price2 = p2
    return VendingMachine.Response.OK
```











### Ошибка #13

**Код до исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins1 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins2 != self.__maxc2`, то баланс пользователя не пополниться на стоимость 1 монеты, хотя этого требует пункт o. 

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Перейдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Результат getCurrentSum() задается выражением:
# coins1 * coinval1 + coins2 * coinval2
# Это означает, что мы можем составить систему из 2-ух уравнений
# и решить ее, чтобы найти эталонные значения coinval1 и coinval2.
# Составим 1-ое уравнение: v1 + v2 = s1.
machine.fillCoins(1, 1)
s1 = machine.getCurrentSum()
# Составим 2-ое уравнение.
# Возьмем такие c1 и c2, чтобы 2-ое уравнение не вырождалось в 1-ое:
# 2v1 + 3v2 = s2.
machine.fillCoins(2, 3)
s2 = machine.getCurrentSum()
# Из 1-ого уравнения следует, что v2 = s1 - v1.
# Заменив v2 этим равенством и упростив уравнение, получаем:
# v1 = 3s1 - s2.
coinval1 = 3*s1 - s2
# Перейдем в рабочий режим.
machine.exitAdminMode()
# Запомним изначальный баланс.
old_balance = machine.getCurrentBalance()
# Внесем одну монету 1-го типа на баланс.
machine.putCoin1()
# Вычислим новый баланс, получившийся в результате putCoin1().
new_balance = machine.getCurrentBalance()
# Таким образом, дельта баланса - используемый в putCoin1() coinval1.
got_coinval1 = new_balance - old_balance
# Ожидается, что coinval1 == got_coinval1.
print(coinval1 == got_coinval1)
```

**Полученное значение**   
В `stdout` выведется `False`. 

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins1 += 1
    return VendingMachine.Response.OK
```

**Замечание**  
По сути, воспроизведение полагается только на то, что метод `getCurrentSum()` реализован именно так, а не иначе, хотя именно такая реализация и является самой очевидной. В остальном, за исключением обозреваемого метода `putCoin1()`, все остальные методы в воспроизведении уже полностью исправлены.













### Ошибка #14

**Код до исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins1 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins1 >= self.__maxc1`, то при внесении еще одной монеты 1-го типа в автомат, метод `fillCoins()` не возвратит `VendingMachine.Response.CANNOT_PERFORM`, хотя этого требует пункт o. 

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Перейдем в режим отладки
machine.enterAdminMode(117345294655382)
# Вычислим эталонное значение maxc1.
maxc1 = 0
while machine.fillCoins(maxc1 + 1, 1) != VendingMachine.Response.INVALID_PARAM:
    maxc1 += 1
# Удостоверимся, что в автомат внесено максимальное количество монет 1-го типа.
machine.fillCoins(maxc1, 1)
# Перейдем в рабочий режим.
machine.exitAdminMode()
# Попытаемся внести монету 1-го типа. Исходя из требований, должно вернуться CANNOT_PERFORM.
print(machine.putCoin1() == VendingMachine.Response.CANNOT_PERFORM)
```

**Полученное значение**   
В `stdout` выведется `False`. 

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin1(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins1 += 1
    return VendingMachine.Response.OK
```












### Ошибка #15

**Код до исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins1 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins1 != self.__maxc1`, то при внесении монеты 2-го типа в автомат, метод `putCoin2()` не увеличит количество монет 2-го типа на 1, хотя этого требует пункт p.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Внесем одну монету 2-го типа.
machine.putCoin2()
# Попробуем вернуть деньги.
# Будем условиться, что мы знаем устройство putCoin2().
# То есть, мы знаем, что coins1 стало больше на 1 и баланс стал больше на coinval1.
# Хотя, в теории, coins2 должно стать больше на 1 и баланс должен стать больше на coinval2.
# Таким образом, ожидается, что не вернется UNSUITABLE_CHANGE (это неверно), 
# так как есть только одна монета стоимостью 2 у.е., но отдать автомату нужно 1 у.е.
print(machine.returnMoney() == VendingMachine.Response.UNSUITABLE_CHANGE)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins2 += 1
    return VendingMachine.Response.OK
```












### Ошибка #16

**Код до исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval1
    self.__coins2 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins1 != self.__maxc1`, то при внесении монеты 2-го типа в автомат, метод `putCoin2()` увеличит баланс на стоимость монеты 1-го типа, а не 2-го типа, как этого требует пункт p.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Перейдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Результат getCurrentSum() задается выражением:
# coins1 * coinval1 + coins2 * coinval2
# Это означает, что мы можем составить систему из 2-ух уравнений
# и решить ее, чтобы найти эталонные значения coinval1 и coinval2.
# Составим 1-ое уравнение: v1 + v2 = s1.
machine.fillCoins(1, 1)
s1 = machine.getCurrentSum()
# Составим 2-ое уравнение.
# Возьмем такие c1 и c2, чтобы 2-ое уравнение не вырождалось в 1-ое:
# 2v1 + 3v2 = s2.
machine.fillCoins(2, 3)
s2 = machine.getCurrentSum()
# Из 1-ого уравнения следует, что v1 = s1 - v2.
# Заменив v1 этим равенством и упростив уравнение, получаем:
# v2 = s2 - 2s1.
coinval2 = s2 - 2*s1
# Перейдем в рабочий режим.
machine.exitAdminMode()
# Запомним изначальный баланс.
old_balance = machine.getCurrentBalance()
# Внесем одну монету 1-го типа на баланс.
machine.putCoin2()
# Вычислим новый баланс, получившийся в результате putCoin2().
new_balance = machine.getCurrentBalance()
# Таким образом, дельта баланса - используемый в putCoin2() coinval2.
got_coinval2 = new_balance - old_balance
# Ожидается, что coinval2 == got_coinval2.
print(coinval2 == got_coinval2)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins2 += 1
    return VendingMachine.Response.OK
```












### Ошибка #17

**Код до исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins1 == self.__maxc1:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins2 += 1
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and self.__coins2 >= self.__maxc2`, то при внесении еще одной монеты 2-го типа в автомат, метод `putCoin2()` не возвратит `VendingMachine.Response.CANNOT_PERFORM`, хотя этого требует пункт p.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Перейдем в режим отладки
machine.enterAdminMode(117345294655382)
# Вычислим эталонное значение maxc2.
maxc2 = 0
while machine.fillCoins(1, maxc2 + 1) != VendingMachine.Response.INVALID_PARAM:
    maxc2 += 1
# Удостоверимся, что в автомат внесено максимальное количество монет 2-го типа.
machine.fillCoins(1, maxc2)
# Перейдем в рабочий режим.
machine.exitAdminMode()
# Попытаемся внести монету 2-го типа. Исходя из требований, должно вернуться CANNOT_PERFORM.
print(machine.putCoin2() == VendingMachine.Response.CANNOT_PERFORM)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def putCoin2(self):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if self.__coins2 == self.__maxc2:
        return VendingMachine.Response.CANNOT_PERFORM
    self.__balance += self.__coinval2
    self.__coins2 += 1
    return VendingMachine.Response.OK
```












### Ошибка #18

**Код до исправления**  
```python
def returnMoney(self):
    ...
    # using coinval1 == 1
    self.__coins1 -= self.__balance // self.__coinval2
    self.__coins2 -= 1
    self.__balance = 0
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__coins1 == 2 and self.__coins2 == 1 and self.__balance == 1`, то метод `returnMoney()` уменьшит количество монет 1-го типа на баланс/2 и 2-то типа на 1, хотя пункт q. требует уменьшить количество монет 2-го типа на баланс/2 и 1-го типа на 1.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Пополним автомат монетами: coins1 = 1, coins2 = 1.
machine.fillCoins(1, 1)
# Перейдем в рабочий режим.
machine.exitAdminMode()
# Внесем одну монету 1-го типа: coins1 = 2, coins2 = 1, balance = 1.
machine.putCoin1()
# Попробуем вернуть баланс.
# Исходя из прошлых тестов, где мы уже нашли эталонные coinval1 и coinval2, 
# далее будем предполагать, что мы их уже знаем.
# - mode != ADMINISTERING;
# - balance != 0;
# - balance <= coins1 * coinval1 + coins2 * coinval2 <=> 1 <= 2 * 1 + 1 * 2 <=> 1 <= 4;
# - balance % coinval2 != 0 <=> 1 % 2 != 0 <=> 1 != 0;
# - coins1 != 0;
# Итого, мы попадаем в последний случай из требования q.
# Таким образом, автомат должен вернуть одну монету 1-го типа и 0 монет 2-го типа. 
machine.returnMoney()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Ожидается, что выведется 1 1.
print(machine.getCoins1(), machine.getCoins2())
```

**Полученное значение**   
В `stdout` выведется `2 0`.

**Ожидаемое значение**  
В `stdout` должно вывестись `1 1`.

**Код после исправления**  
```python
def returnMoney(self):
    ...
    # using coinval1 == 1
    self.__coins2 -= self.__balance // self.__coinval2
    self.__coins1 -= 1
    self.__balance = 0
    return VendingMachine.Response.OK
```












### Ошибка #19

**Код до исправления**  
```python
def giveProduct1(self, number: int):
    ...
    if res % self.__coinval2 == 0:
        self.__coins2 -= res / self.__coinval2
        self.__balance = 0
        self.__num1 -= number
        return VendingMachine.Response.OK
    ...
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and number == 1 and res >= 0 and res <= self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2 and res <= self.__coins2 * self.__coinval2 and res % self.__coinval2 == 0`, то метод `giveProduct1()` уменьшит количество монет 2-го типа на `res / self.__coinval2`, что сделает `self.__coins2` нецелым, приводя к тому, что метод `getCoins2()` возвратит число с плавающей точкой, хотя пункт g. требует возвратить целое число.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Внесем продукты.
machine.fillProducts()
# Найдем стоимость продукта 1-го типа.
price1 = machine.getPrice1()
# Зайдем в рабочий режим.
machine.exitAdminMode()
# Внесем четное число у.е. на баланс так, чтобы хватило на 1 продукт 1-го типа.
if price1 % 2 == 1:
    machine.putCoin1()
while machine.getCurrentBalance() < price1:
    machine.putCoin2()
# Купим 1 продукт 1-го типа.
machine.giveProduct1(1)
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Проверим, что метод getCoins2() возвращает int, как этого требует пункт g. 
print(isinstance(machine.getCoins2(), int))
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def giveProduct1(self, number: int):
    ...
    if res % self.__coinval2 == 0:
        self.__coins2 -= res // self.__coinval2
        self.__balance = 0
        self.__num1 -= number
        return VendingMachine.Response.OK
    ...
```












### Ошибка #20

**Код до исправления**  
```python
def giveProduct2(self, number: int):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number >= self.__max2:
        return VendingMachine.Response.INVALID_PARAM
    if number > self.__num2:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    ...
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and number > 0 and number == self.__max2`, то метод `giveProduct2()` вернет `VendingMachine.Response.INVALID_PARAM`, хотя пункт s. требует возвращать `VendingMachine.Response.INVALID_PARAM` только если `number` \<= 0 предметов или больше максимума предметов 2-го вида (т. е. выполнение метода должно продолжаться).

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Вычислим максимальное количество продуктов 2-го типа.
machine.fillProducts()
max2 = machine.getNumberOfProduct2()
# Выйдем из режима отладки.
machine.exitAdminMode()
# Попытаемся купить все продукты 2-го типа.
# Ожидается, что не возвратится VendingMachine.Response.INVALID_PARAM.
print(machine.giveProduct2(max2) == VendingMachine.Response.INVALID_PARAM)
```

**Полученное значение**  
В `stdout` выведется `True`.

**Ожидаемое значение**  
В `stdout` должно вывестись `False`.

**Код после исправления**  
```python
def giveProduct2(self, number: int):
    if self.__mode == VendingMachine.Mode.ADMINISTERING:
        return VendingMachine.Response.ILLEGAL_OPERATION
    if number <= 0 or number > self.__max2:
        return VendingMachine.Response.INVALID_PARAM
    if number > self.__num2:
        return VendingMachine.Response.INSUFFICIENT_PRODUCT
    ...
```











### Ошибка #21

**Код до исправления**  
```python
def giveProduct2(self, number: int):
    ...
    if res % self.__coinval2 == 0:
        self.__coins2 -= res / self.__coinval2
        self.__balance = 0
        self.__num2 -= number
        return VendingMachine.Response.OK
    ...
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and number == 1 and res >= 0 and res <= self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2 and res <= self.__coins2 * self.__coinval2 and res % self.__coinval2 == 0`, то метод `giveProduct2()` уменьшит количество монет 2-го типа на `res / self.__coinval2`, что сделает `self.__coins2` нецелым, приводя к тому, что метод `getCoins2()` возвратит число с плавающей точкой, хотя пункт g. требует возвратить целое число.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Внесем продукты.
machine.fillProducts()
# Установим цены, чтобы избавиться от рассмотрения четной и нечетной цены.
machine.setPrices(1, 2)
# Зайдем в рабочий режим.
machine.exitAdminMode()
# Внесем четное число у.е. на баланс так, чтобы хватило на 1 продукт 2-го типа.
while machine.getCurrentBalance() < machine.getPrice2():
    machine.putCoin2()
# Купим 1 продукт 2-го типа.
machine.giveProduct2(1)
# Зайдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Проверим, что метод getCoins2() возвращает int, как этого требует пункт g. 
print(isinstance(machine.getCoins2(), int))
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def giveProduct2(self, number: int):
    ...
    if res % self.__coinval2 == 0:
        self.__coins2 -= res // self.__coinval2
        self.__balance = 0
        self.__num2 -= number
        return VendingMachine.Response.OK
    ...
```











### Ошибка #22

**Код до исправления**  
```python
def giveProduct2(self, number: int):
    ...
    self.__coins1 -= res // self.__coinval2
    self.__coins2 -= 1
    self.__balance = 0
    self.__num2 -= number
    return VendingMachine.Response.OK
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode != VendingMachine.Mode.ADMINISTERING and number == 1 and res >= 0 and res <= self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2 and res <= self.__coins2 * self.__coinval2 and res % self.__coinval2 != 0 and self.__coins1 != 0`, то метод `giveProduct2()` уменьшит количество монет 1-го типа на `res // self.__coinval2` и 2-го типа на `1`, что приведет к выдаче неправильной сдачи, что нарушает требование s.

**Шаги для воспроизведения**
```python
machine = VendingMachine()
# Перейдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Заполним автомат продуктами.
machine.fillProducts()
# Установим минимальные цены на продукты.
machine.setPrices(1, 1)
# Выйдем из режима отладки.
machine.exitAdminMode()
# Внесем 3 монеты 2-го типа и 1 монету 1-го типа.
machine.putCoin2()
machine.putCoin2()
machine.putCoin2()
machine.putCoin1()
# Попробуем взять продукт 2 продукта 1-го типа.
# - mode != ADMINISTERING
# - number = 2 (условимся, что max2 > 2)
# - res >= 0 <=> balance - number * price >= 0 <=> 7 - 2 * 1 >= 0 <=> 5 >= 0
# - res <= coins1 * coinval1 + coins2 * coinval2 <=> 5 <= 1 * 1 + 3 * 2 <=> 5 <= 7
# - res <= coins2 * coinval2 <=> 5 > 3 * 2 <=> 5 <= 6
# - res % 2 != 0 <=> 5 % 2 != 0 <=> 1 != 0
# - coins1 != 0
# Таким образом, должен выполнится последний случай, описанный в требовании s. 
machine.giveProduct2(2)
# Перейдем в режим отладки.
machine.enterAdminMode(117345294655382)
# Ожидается, что вернется 1 и 0.
print(machine.getCoins1() == 0 and machine.getCoins2() == 1)
```

**Полученное значение**   
В `stdout` выведется `False`.

**Ожидаемое значение**  
В `stdout` должно вывестись `True`.

**Код после исправления**  
```python
def giveProduct2(self, number: int):
    ...
    self.__coins2 -= res // self.__coinval2
    self.__coins1 -= 1
    self.__balance = 0
    self.__num2 -= number
    return VendingMachine.Response.OK
```








## Недостижимый код

### Недостижимый код #1

```python
def returnMoney(self):
    ...
if self.__balance > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2: 
    return VendingMachine.Response.TOO_BIG_CHANGE # Unreachable.
    ...
```

Условие выше никогда не выполнится. Попробуем набросить доказательство.  
Чтобы условие выполнилось, надо как-то достичь одну из следующих ситуаций:
- увеличить баланс, не увеличивая количество монет 1-го и 2-го типа (1);
- уменьшить количество монет 1-го и 2-го типа, не уменьшая баланс (2).
  
Увеличить баланс можно только через методы `putCoin1()` и `putCoin2()`, но в обоих из них при увеличении баланса увеличивается и соответствующее количество монет, поэтому первая ситуация не выполняется.  
  
Уменьшение количества монеты 1-го или 2-го типа (оператор `-=`) встречается только в методах `returnMoney()`, `giveProduct1()`, `giveProduct2()`, однако там же баланс обнуляется.  
Уменьшения также можно добиться и с помощью оператора присваивания (`=`). К `__coins1` значение присваивается только 1 раз в методе `fillCoins()` (не считая конструктора); к `__coins2` там тоже присваивается значение. Однако, как для `__coins1`, так и `__coins2`, метод `fillCoins()` работает только в режиме отладки, в которой можно перейти только через метод `enterAdminMode()`, который работает только если баланс нулевой. Иными словами, мы не можем внести что-то на баланс через `putCoin1()` или `putCoin2()` и потом уменьшить `__coins1` или `__coins2`, так как не сможем зайти в режим отладки.  
К `__coins2` также можно присвоить значение в методах `returnMoney()`, `giveProduct1()`, `giveProduct2()`. Тем не менее, во всех случаях баланс там же обнуляется.  
  
Итого, не представляется возможным осуществить ситуацию 1 или 2, что говорит о том, что условие никогда не выполнится.











### Недостижимый код #2

```python
def giveProduct1(self, number: int):
    ...
    if res > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2:
        return VendingMachine.Response.TOO_BIG_CHANGE # Unreachable.
    ...
```

`res` вычисляется как `self.__balance - number * self.__price1`, а это означает, что `res < self.__balance` (по условию `number` и `self.__price1` больше нуля).  
Далее доказывается аналогично пункту 1.












### Недостижимый код #3

```python
def giveProduct2(self, number: int):
    ...
    if res > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2:
        return VendingMachine.Response.INSUFFICIENT_MONEY # Unreachable.
    ...
```

Доказывается аналогично пункту 2.  
Замечание. Пункт s. требует возвращать `VendingMachine.Response.TOO_BIG_CHANGE`, а не `VendingMachine.Response.INSUFFICIENT_MONEY`, но т. к. код недостижим, то это не имеет значения.











### Недостижимый код #4

```python
def fillCoins(self, c1: int, c2: int):
    ...
    if c1 <= 0 or c2 > self.__maxc1:
            return VendingMachine.Response.INVALID_PARAM
    if c1 <= 0 or c2 > self.__maxc2:
        return VendingMachine.Response.INVALID_PARAM # Unreachable.
    ...
```

Из оригинальной версии VendingMachine.  
Чтобы попасть во второе условие нужно иметь `c1 <= 0` (отлавливается 1-ым условием) или `c2 > self.__maxc2` (так как `self.__maxc1` равен `self.__maxc2`, то тоже отлавливается 1-ым условием).  
Таким образом, второе условие никогда не выполнится.










### Недостижимый код #5

```python
def returnMoney(self):
    ...
    if self.__balance % self.__coinval2 == 0:
        self.__coins2 -= self.__balance // self.__coinval2
        self.__balance = 0
        return VendingMachine.Response.OK
    if self.__coins1 == 0:
        # using coinval1 == 1
        return VendingMachine.Response.UNSUITABLE_CHANGE # Unreachable.
    ...
```

`UNSUITABLE_CHANGE` недостижим, если `coinval2 == 2`.  
Чтобы попасть в проверку условия `self.__coins1 == 0`, надо сначала не пройти проверку условия `self.__balance % self.__coinval2 == 0`, т. е. баланс должен быть нечетным. Единственный способ сделать баланс нечетным - использовать метод `putCoin1()`, но там же увеличивается и `__coins1`. Единственные способы уменьшить `__coins1`: метод `fillCoins()`, но он не сможет сбросить `__coins1` до нуля, и методы `returnMoney()`, `giveProduct1()`, `giveProduct2()`, но там же баланс обнуляется, что возвращает нас в начальное состояние.