from VendingMachine import VendingMachine

def test_abc():
    pass

if __name__ == "__main__":
    machine = VendingMachine()
    # Зайдем в режим отладки.
    machine.enterAdminMode(117345294655382)
    # Заполним автомат продуктами.
    machine.fillProducts()
    # Исходя из требования j., теперь в max1 должно находится максимальное количество продуктов 1-го типа.
    max1 = machine.getNumberOfProduct1()
    # Дополнительно проверим, что max1 > 0 (понадобится далее).
    assert max1 > 0
    # Тогда, исходя из требования o., мы можем взять max1 продуктов 1-го типа.
    # Для этого сначала выйдем из режима отладки.
    machine.exitAdminMode()
    # Попробуем взять max1 продуктов 1-го типа 
    # (на самом деле, в giveProduct1() тоже есть баг, но мы не попадем под него, об этом позже).
    # Ожидается, что giveProduct1() не возвратит INVALID_PARAM, т. к. max1 продуктов 1-го типа должно быть и 
    print(machine.giveProduct1(max1) == VendingMachine.Response.INVALID_PARAM)