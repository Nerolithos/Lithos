# 关于“self”的问题

在为《面向对象编程》设计例子时，我观察到终端如下报错：

```shell
Traceback (most recent call last):
  File "car.py", line 11, in <module>
my_car = Car("Toyota", "1980", "Land_Cruiser", "Metallic_Red")
TypeError: Car.__init__() takes 4 positional arguments but 5 were given
```

结果发现是__init__()方法中的第一个参数必须填“self”，也就是说方法中的参数数比传入的参数数要大一位。为什么？

**关于 self** **参数**：
* Python 中，self 是一个约定用于引用当前实例的名称，并且它应该始终是__init__ 方法的第一个参数，尽管调用时不需要传入它的值。因为 self 被遗漏，导致后续对 self.brand 等属性的赋值和方法调用变得不可用。
* **self 是对新创建的实例的引用。**通过 self，可以为实例定义属性，并将初始值赋给这些属性。(比如：year = self.year)
* 当创建类的一个新实例时，Python 会自动调用__init__方法。这个方法使得在实例被创建时为其设置初始状态或执行某些初始化操作。
* 在该程序中__init__ 方法被定义在 Car 类中，并接收四个参数 brand,  year, model 和 color。这些参数用于初始化实例的属性。当创建 Car 类的一个实例 my_car 时__init__ 方法**自动被调用**，并且 self.brand, self.year, self.model 和 self.color 被赋予传入的值。
