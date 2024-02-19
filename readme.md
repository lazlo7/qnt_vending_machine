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
Шаги для воспроизведения:
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
Шаги для воспроизведения:
```python
machine = VendingMachine()
print(machine.getCoins1(), end=" ")
machine.putCoin1()
print(machine.getCoins1())
```
Заметим, что воспроизведение не зависит от начального значения количества монет 1-го вида в автомате, которое по принципу "серого ящика" мы можем и не знать.

**Полученное значение**  
В `stdout` выведется `0 0`.

**Ожидаемое значение**  
В `stdout` должно вывестись `0 1`.

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







### Ошибка #3

**Код до исправления**  
```python
def getCoins2(self):
    if self.__mode == VendingMachine.Mode.OPERATION:
        return self.__coins1
    return self.__coins2
```

**Данные, на которых наблюдается некорректное поведение**  
Если `self.__mode == VendingMachine.Mode.OPERATION`, то метод вернет количество монет 1-го вида, хотя пункт g. требует вернуть `0`.  
Шаги для воспроизведения:
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










### Ошибка #4

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
Шаги для воспроизведения:
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









### Ошибка #5

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
Шаги для воспроизведения:
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
Шаги для воспроизведения:
```python
machine = VendingMachine()
# Удостоверимся, что автомат не в режиме отладки.
machine.exitAdminMode()
# Ожидается, что вернется VendingMachine.Response.ILLEGAL_OPERATION.
print(machine.fillProducts() == VendingMachine.Response.ILLEGAL_OPERATION)
```
Заметим, что мы используем метод `enterAdminMode(code)` для тестирования других методов только после того как нашли в нем все ошибки.

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
Шаги для воспроизведения:
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
Шаги для воспроизведения:
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
