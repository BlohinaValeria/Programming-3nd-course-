# Лабораторная работа 2. Ряд Фибоначчи с помощью итераторов

Лабораторная работа состоит из двух подзаданий: 
1. Создание сопрограммы на основе кода, позволяющей по данному n сгенерировать список элементов из ряда Фибоначчи.
2. Создание программы, возвращающей список чисел Фибоначчи с помощью итератора.

Рассмотрим особенности каждого из них. 

## Задание 1
Стартовый борд: 


На основе приложенного кода в файле ```gen_fib.py``` разработать сопрограмму (_корутину_), реализующую возвращение списка элементов ряда Фибоначчи. 

```python
>> gen = my_genn()

>> gen.send(3) 
[0, 1, 1] 

>> gen.send(5) 
[0, 1, 1, 2, 3] 

>> gen.send(8) 
[0, 1, 1, 2, 3, 5, 8, 13] 

```
Требуется написать необходимые тесты в файле ```test_fib.py```.

```
import unittest
from gen_fib import my_genn


class TestFibonacciGenerator(unittest.TestCase):

    def setUp(self):
        self.gen = my_genn()

    def test_zero_elements(self):
        result = self.gen.send(0)
        self.assertEqual(result, [])

    def test_one_element(self):
        result = self.gen.send(1)
        self.assertEqual(result, [0])

    def test_three_elements(self):
        result = self.gen.send(3)
        self.assertEqual(result, [0, 1, 1])

    def test_five_elements(self):
        result = self.gen.send(5)
        self.assertEqual(result, [0, 1, 1, 2, 3])

    def test_eight_elements(self):
        result = self.gen.send(8)
        self.assertEqual(result, [0, 1, 1, 2, 3, 5, 8, 13])

    def test_negative_number(self):
        result = self.gen.send(-5)
        self.assertEqual(result, [])

    def test_multiple_calls(self):
        result1 = self.gen.send(3)
        self.assertEqual(result1, [0, 1, 1])

        result2 = self.gen.send(5)
        self.assertEqual(result2, [0, 1, 1, 2, 3])

        result3 = self.gen.send(2)
        self.assertEqual(result3, [0, 1])


if __name__ == '__main__':
    unittest.main()
```



## Задание 2
Дополните код классом ```FibonacchiLst``` (пример такого класса представлен в even_numbers_iterator.py), который бы позволял перебирать элементы из ряда Фибоначчи по данному ей списку.
Итератор должен вернуть очередное значение, которое принадлежит ряду Фибоначчи, из данного ей списка. Например: 
для lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 1], ```FibonacchiLst``` должен вернуть [0, 1, 2, 3, 5, 8, 1]

Решение может быть выполнено с помощью реализации содержимого методов ```__init__```,```__iter__```, ```__next__``` или с помощью реализации метода ```__getitem__```.

```python

class FibonacchiLst:
    def __init__(self):
        pass
    
    def __iter__(self):
        pass 

    def __next__(self):
        pass

```
Пример реализации итератора, возвращающего четные элементы, из iterable-объекта представлен в файле ```even_numbers_iterator.py```.
