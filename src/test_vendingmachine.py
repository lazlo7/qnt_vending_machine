from VendingMachine import VendingMachine
import pytest
from typing import Callable
from itertools import product

# For the sake of simplicity, we'll be assuming that we know all the private constants in the VendingMachine class.
# We could've computed them just like we did in the readme.md file anyway.
ADMIN_CODE = 117345294655382
MAX_PRODUCT1_N = 30
MAX_PRODUCT2_N = 40
MAX_COINS1_N = 50
MAX_COINS2_N = 50
COIN1_VALUE = 1
COIN2_VALUE = 2

# Typical edge-casey int values.
NON_POSITIVE_INT_TESTDATA = [-10**100. -10**10, -3489672334, -1, 0]
POSITIVE_INT_TESTDATA = [1, 17368216213, 10**10, 10**100]
INT_TESTDATA = NON_POSITIVE_INT_TESTDATA + POSITIVE_INT_TESTDATA

"""
enterAdminMode() and getCurrentMode() tests.
"""
# Tests correct INVALID_PARAM returning.
@pytest.mark.parametrize("code", INT_TESTDATA + [ADMIN_CODE - 1, ADMIN_CODE + 1])
def test_enterAdminMode_InvalidCode(code: int):
    machine = VendingMachine()
    assert machine.enterAdminMode(code) == VendingMachine.Response.INVALID_PARAM

# Tests correct CANNOT_PERFORM returning (bug 3).
@pytest.mark.parametrize("increaseBalance", 
                         [lambda m: m.putCoin1(), 
                          lambda m: m.putCoin2(),
                          lambda m: [m.putCoin1(), m.putCoin2()], 
                          lambda m: [m.putCoin2(), m.putCoin1()]])
def test_enterAdminMode_NonZeroBalance(increaseBalance: Callable[[VendingMachine], None]):
    machine = VendingMachine()
    increaseBalance(machine)
    assert machine.enterAdminMode(ADMIN_CODE) == VendingMachine.Response.CANNOT_PERFORM

# Tests returning INVALID_PARAM first if codes don't match and balance is non-zero (bug 2).
@pytest.mark.parametrize("code, increaseBalance", 
                         zip(INT_TESTDATA + [ADMIN_CODE - 1, ADMIN_CODE + 1],
                             [lambda m: m.putCoin1(), 
                              lambda m: m.putCoin2(),
                              lambda m: [m.putCoin1(), m.putCoin2()], 
                              lambda m: [m.putCoin2(), m.putCoin1()]]))
def test_enterAdminMode_InvalidCodeWhenNonZeroBalance(code: int, increaseBalance: Callable[[VendingMachine], None]):
    machine = VendingMachine()
    increaseBalance(machine)
    assert machine.enterAdminMode(code) == VendingMachine.Response.INVALID_PARAM

# Tests correct OK returning. 
def test_enterAdminMode_OK():
    machine = VendingMachine()
    assert machine.enterAdminMode(ADMIN_CODE) == VendingMachine.Response.OK

# Tests correct ADMINISTERING mode switching.
def test_enterAdminMode_OKModeSwitching():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    # This tests getCurrentMode() as well.
    assert machine.getCurrentMode() == VendingMachine.Mode.ADMINISTERING

# getNumberOfProduct1: changing.
def test_getNumberOfProduct1():
    machine = VendingMachine()
    # The only way to change the number of product1 is via fillProducts().
    machine.enterAdminMode(1234)





"""
exitAdminMode() and getCurrentMode() tests.
"""
# Tests correct mode switching after being in admin mode.
def test_exitAdminMode_AfterAdminMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.exitAdminMode()
    # This tests getCurrentMode() as well.
    assert machine.getCurrentMode() == VendingMachine.Mode.OPERATION

# Tests correct mode switching after being in operation mode.
def test_exitAdminMode_AfterOperationMode():
    machine = VendingMachine()
    machine.exitAdminMode()
    # This tests getCurrentMode() as well.
    assert machine.getCurrentMode() == VendingMachine.Mode.OPERATION





"""
setPrices(), getPrice1() and getPrice2() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_setPrices_InvalidMode():
    machine = VendingMachine()
    assert machine.setPrices(1, 1) == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct INVALID_PARAM returning for p1 (bug 11).
@pytest.mark.parametrize("p1", NON_POSITIVE_INT_TESTDATA)
def test_setPrices_InvalidParamP1(p1: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.setPrices(p1, 1) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for p2 (bug 12).
@pytest.mark.parametrize("p2", NON_POSITIVE_INT_TESTDATA)
def test_setPrices_InvalidParamP2(p2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.setPrices(1, p2) == VendingMachine.Response.INVALID_PARAM

# Tests correct OK returning.
@pytest.mark.parametrize("p1, p2", list(product(POSITIVE_INT_TESTDATA, POSITIVE_INT_TESTDATA)))
def test_setPrices_OK(p1: int, p2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.setPrices(p1, p2) == VendingMachine.Response.OK

# Tests correct price1 and price2 setting.
@pytest.mark.parametrize("p1, p2", list(product(POSITIVE_INT_TESTDATA, POSITIVE_INT_TESTDATA)))
def test_setPrices_OKPricesSetting(p1: int, p2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(p1, p2)
    # This tests getPrice1() and getPrice2() as well.
    assert machine.getPrice1() == p1
    assert machine.getPrice2() == p2





"""
fillProducts(), getNumberOfProduct1() and getNumberOfProduct2() tests.
"""
# Tests correct ILLEGAL_OPERATION returning (bug 6).
def test_fillProducts_InvalidMode():
    machine = VendingMachine()
    assert machine.fillProducts() == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct OK returning.
def test_fillProducts_OK():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillProducts() == VendingMachine.Response.OK

# Tests correct number of product1 setting (bug 7).
def test_fillProducts_OKProduct1Setting():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillProducts()
    # This tests getNumberOfProduct1() as well.
    assert machine.getNumberOfProduct1() == MAX_PRODUCT1_N

# Tests correct number of product2 setting.
def test_fillProducts_OKProduct2Setting():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillProducts()
    # This tests getNumberOfProduct2() as well.
    assert machine.getNumberOfProduct2() == MAX_PRODUCT2_N





"""
getCoins1() and getCoins2() admin-only tests.
"""
# Tests correct 0 returning if in OPERATION mode for getCoins1().
def test_getCoins1_OperationMode():
    machine = VendingMachine()
    # Setting coins1 to 1 so that we can differentiate between returning
    # literally 0 coins1 and returning 0 as an error.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.exitAdminMode()
    assert machine.getCoins1() == 0

# Tests correct 0 returning if in OPERATION mode for getCoins2(), also tests for getCoins2() (bug 1) (bug 5).
def test_getCoins2_OperationMode():
    machine = VendingMachine()
    # Setting coins2 to 1 so that we can differentiate between returning
    # literally 0 coins2 and returning 0 as an error.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.exitAdminMode()
    assert machine.getCoins2() == 0





"""
fillCoins(), getCoins1() and getCoins2() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_fillCoins_InvalidMode():
    machine = VendingMachine()
    assert machine.fillCoins(1, 1) == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct INVALID_PARAM returning for c1 <= 0.
@pytest.mark.parametrize("c1", NON_POSITIVE_INT_TESTDATA)
def test_fillCoins_InvalidParamC1(c1: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillCoins(c1, 1) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for c2 <= 0 (bug 9).
@pytest.mark.parametrize("c2", NON_POSITIVE_INT_TESTDATA)
def test_fillCoins_InvalidParamC2(c2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillCoins(1, c2) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for c1 > MAX_COINS1_N (bug 10).
@pytest.mark.parametrize("c1", [MAX_COINS1_N + 1, MAX_COINS1_N + 2, MAX_COINS1_N + 10**10])
def test_fillCoins_InvalidParamC1OverMax(c1: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillCoins(c1, 1) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for c2 > MAX_COINS2_N.
@pytest.mark.parametrize("c2", [MAX_COINS2_N + 1, MAX_COINS2_N + 2, MAX_COINS2_N + 10**10])
def test_fillCoins_InvalidParamC2OverMax(c2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillCoins(1, c2) == VendingMachine.Response.INVALID_PARAM

# Tests correct OK returning.
@pytest.mark.parametrize("c1, c2", list(product([1, MAX_COINS1_N // 2, MAX_COINS1_N],
                                                [1, MAX_COINS2_N // 2, MAX_COINS2_N])))
def test_fillCoins_OK(c1: int, c2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.fillCoins(c1, c2) == VendingMachine.Response.OK

# Tests correct number of coins1 setting.
@pytest.mark.parametrize("c1", [1, MAX_COINS1_N // 2, MAX_COINS1_N])
def test_fillCoins_OKCoins1Setting(c1: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(c1, 1)
    # This tests getCoins1() as well.
    assert machine.getCoins1() == c1

# Tests correct number of coins2 setting.
@pytest.mark.parametrize("c2", [1, MAX_COINS2_N // 2, MAX_COINS2_N])
def test_fillCoins_OKCoins2Setting(c2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, c2)
    # This tests getCoins2() as well.
    assert machine.getCoins2() == c2






"""
putCoin1() and getCurrentBalance() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_putCoin1_InvalidMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.putCoin1() == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct CANNOT_PERFORM returning (bug 14).
def test_putCoin1_CannotPerform():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(MAX_COINS1_N, 1)
    machine.exitAdminMode()
    assert machine.putCoin1() == VendingMachine.Response.CANNOT_PERFORM

# Tests correct OK returning.
def test_putCoin1_OK():
    machine = VendingMachine()
    assert machine.putCoin1() == VendingMachine.Response.OK

# Tests correct coins1 incrementing (bug 4).
def test_putCoin1_OKCoins1Incrementing():
    machine = VendingMachine()
    
    machine.enterAdminMode(ADMIN_CODE)
    old_coins1 = machine.getCoins1()
    machine.exitAdminMode()

    machine.putCoin1()
    # We need direct access to a field here to really check that we incremented coins1,
    # there's no other way to do it.
    assert getattr(machine, "_VendingMachine__coins1") == old_coins1 + 1

# Tests correct balance incrementing (bug 13).
def test_putCoin1_OKBalanceIncrementing():
    machine = VendingMachine()
    old_balance = machine.getCurrentBalance()
    machine.putCoin1()
    assert machine.getCurrentBalance() == old_balance + COIN1_VALUE





"""
putCoin2() and getCurrentBalance() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_putCoin2_InvalidMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.putCoin2() == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct CANNOT_PERFORM returning (bug 17).
def test_putCoin2_CannotPerform():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, MAX_COINS2_N)
    machine.exitAdminMode()
    assert machine.putCoin2() == VendingMachine.Response.CANNOT_PERFORM

# Tests correct OK returning.
def test_putCoin2_OK():
    machine = VendingMachine()
    assert machine.putCoin2() == VendingMachine.Response.OK

# Tests correct coins2 incrementing.
def test_putCoin2_OKCoins2Incrementing():
    machine = VendingMachine()
    
    machine.enterAdminMode(ADMIN_CODE)
    old_coins2 = machine.getCoins2()
    machine.exitAdminMode()

    machine.putCoin2()
    # We need direct access to a field here to really check that we incremented coins2,
    # there's no other way to do it.
    assert getattr(machine, "_VendingMachine__coins2") == old_coins2 + 1

# Tests correct balance incrementing.
def test_putCoin2_OKBalanceIncrementing():
    machine = VendingMachine()
    old_balance = machine.getCurrentBalance()
    machine.putCoin2()
    assert machine.getCurrentBalance() == old_balance + COIN2_VALUE





"""
getCurrentSum() tests.
"""
# Tests returning 0 if in OPERATION mode.
def test_getCurrentSum_OperationMode():
    machine = VendingMachine()
    # Setting coins1 to 1 so that we can differentiate between returning
    # literally 0 sum and returning 0 as an error.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.exitAdminMode()
    assert machine.getCurrentSum() == 0

# Tests correct sum returning.
@pytest.mark.parametrize("c1, c2", list(product([1, MAX_COINS1_N // 2, MAX_COINS1_N],
                                                [1, MAX_COINS2_N // 2, MAX_COINS2_N])))
def test_getCurrentSum_OK(c1: int, c2: int):
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(c1, c2)
    assert machine.getCurrentSum() == c1 * COIN1_VALUE + c2 * COIN2_VALUE





"""
returnMoney() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_returnMoney_InvalidMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.returnMoney() == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct OK returning on zero balance.
def test_returnMoney_OKZeroBalance():
    machine = VendingMachine()
    assert machine.returnMoney() == VendingMachine.Response.OK

# Helper function to reach balance > coins2 * COIN2_VALUE state in returnMoney().
def set_machine_to_returnMoneyAllCoins2(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    return machine.returnMoney()

# Tests coins1 decreasing on balance > coins2 * COIN2_VALUE.
def test_returnMoney_OKAllCoins2_Coins1Decreasing():
    machine = VendingMachine()
    set_machine_to_returnMoneyAllCoins2(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 3

# Tests coins2 setting to zero on balance > coins1 * COIN1_VALUE.
def test_returnMoney_OKAllCoins2_Coins2Zeroed():
    machine = VendingMachine()
    set_machine_to_returnMoneyAllCoins2(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 0

# Tests balance setting to zero on balance > coins1 * COIN1_VALUE.
def test_returnMoney_OKAllCoins2_BalanceZeroed():
    machine = VendingMachine()
    set_machine_to_returnMoneyAllCoins2(machine)
    assert machine.getCurrentBalance() == 0

# Tests correct OK returning on balance > coins1 * COIN1_VALUE.
def test_returnMoney_OKAllCoins2():
    machine = VendingMachine()
    assert set_machine_to_returnMoneyAllCoins2(machine) == VendingMachine.Response.OK

# Helper function to reach balance % COIN2_VALUE == 0 state in returnMoney().
def set_machine_to_returnMoneySomeCoins2(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 2)
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin2()
    return machine.returnMoney()

# Tests coins1 not changing to zero on balance % COIN2_VALUE == 0.
def test_returnMoney_SomeCoins2Coins1NotChanging():
    machine = VendingMachine()
    set_machine_to_returnMoneySomeCoins2(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 3

# Tests coins2 decreasing on balance % COIN2_VALUE == 0.
def test_returnMoney_SomeCoins2Coins2Decreasing():
    machine = VendingMachine()
    set_machine_to_returnMoneySomeCoins2(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 1

# Tests balance setting to zero on balance % COIN2_VALUE == 0.
def test_returnMoney_SomeCoins2BalanceZeroed():
    machine = VendingMachine()
    set_machine_to_returnMoneySomeCoins2(machine)
    assert machine.getCurrentBalance() == 0

# Tests correct OK returning on balance % COIN2_VALUE == 0.
def test_returnMoney_SomeCoins2():
    machine = VendingMachine()
    assert set_machine_to_returnMoneySomeCoins2(machine) == VendingMachine.Response.OK

# Helper function to reach default state in returnMoney().
def set_machine_to_returnMoneyDefault(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.exitAdminMode()
    machine.putCoin1()
    return machine.returnMoney()

# Tests coins2 decreasing on default state (bug 18).
def test_returnMoney_DefaultCoins2Decreasing():
    machine = VendingMachine()
    set_machine_to_returnMoneyDefault(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 1

# Tests coins1 decreasing on default state (bug 18).
def test_returnMoney_DefaultCoins1Decreasing():
    machine = VendingMachine()
    set_machine_to_returnMoneyDefault(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 1

# Tests balance setting to zero on default state.
def test_returnMoney_DefaultBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_returnMoneyDefault(machine)
    assert machine.getCurrentBalance() == 0

# Tests correct OK returning on default state.
def test_returnMoney_DefaultOK():
    machine = VendingMachine()
    assert set_machine_to_returnMoneyDefault(machine) == VendingMachine.Response.OK





"""
giveProduct1() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_giveProduct1_InvalidMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.giveProduct1(1) == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct INVALID_PARAM returning for number <= 0.
@pytest.mark.parametrize("number", NON_POSITIVE_INT_TESTDATA)
def test_giveProduct1_InvalidParamNumberNonPositive(number: int):
    machine = VendingMachine()
    assert machine.giveProduct1(number) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for number > MAX_PRODUCT1_N (bug 8).
@pytest.mark.parametrize("number", [MAX_PRODUCT1_N + 1, MAX_PRODUCT1_N + 2, MAX_PRODUCT1_N + 10**10])
def test_giveProduct1_InvalidParamNumberOverMax(number: int):
    machine = VendingMachine()
    assert machine.giveProduct1(number) == VendingMachine.Response.INVALID_PARAM

# Tests correct INSUFFICIENT_PRODUCT returning.
def test_giveProduct1_InsufficientProduct():
    machine = VendingMachine()
    assert machine.giveProduct1(1) == VendingMachine.Response.INSUFFICIENT_PRODUCT

# Tests correct INSUFFICIENT_MONEY returning on res < 0.
def test_giveProduct1_InsufficientMoney():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(5, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin2()
    assert machine.giveProduct1(2) == VendingMachine.Response.INSUFFICIENT_MONEY

# Helper function to reach res > self.__coins2 * self.__coinval2 state in giveProduct1().
def set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    return machine.giveProduct1(2)

# Tests coins1 decreasing on res > self.__coins2 * self.__coinval2.
def test_giveProduct1_ChangeLargerThanCoins2SumCoins1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 5

# Tests coins2 setting to zero on res > self.__coins2 * self.__coinval2.
def test_giveProduct1_ChangeLargerThanCoins2SumCoins2Zeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 0

# Tests balance setting to zero on res > self.__coins2 * self.__coinval2.
def test_giveProduct1_ChangeLargerThanCoins2SumBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine)
    assert machine.getCurrentBalance() == 0

# Tests num1 decreasing on res > self.__coins2 * self.__coinval2.
def test_giveProduct1_ChangeLargerThanCoins2SumNum1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getNumberOfProduct1() == MAX_PRODUCT1_N - 2

# Tests correct OK returning on res > self.__coins2 * self.__coinval2.
def test_giveProduct1_ChangeLargerThanCoins2SumOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct1ChangeLargerThanCoins2Sum(machine) == VendingMachine.Response.OK

# Helper function to reach res % self.__coinval2 == 0 in giveProduct1().
def set_machine_to_giveProduct1UnsuitableChange(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    return machine.giveProduct1(2)

# Tests coins1 not changing to zero on res % self.__coinval2 == 0.
def test_giveProduct1_ChangeDivisibleByCoin2ValueCoins1NotChanging():
    machine = VendingMachine()
    set_machine_to_giveProduct1UnsuitableChange(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 5

# Tests coins2 not changing type to float on res % self.__coinval2 == 0 (bug 19).
def test_giveProduct1_ChangeDivisibleByCoin2ValueCoins2NotChanging():
    machine = VendingMachine()
    set_machine_to_giveProduct1UnsuitableChange(machine)
    # We need direct access to a field here to really check that we didn't change coins2 to float.
    assert isinstance(getattr(machine, "_VendingMachine__coins2"), int)

# Tests coin2 decreasing on res % self.__coinval2 == 0.
def test_giveProduct1_ChangeDivisibleByCoin2ValueCoins2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1UnsuitableChange(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 0

# Tests balance setting to zero on res % self.__coinval2 == 0.
def test_giveProduct1_ChangeDivisibleByCoin2ValueBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct1UnsuitableChange(machine)
    assert machine.getCurrentBalance() == 0

# Tests num1 decreasing on res % self.__coinval2 == 0.
def test_giveProduct1_ChangeDivisibleByCoin2ValueNum1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1UnsuitableChange(machine)
    assert machine.getNumberOfProduct1() == MAX_PRODUCT1_N - 2

# Tests correct OK returning on res % self.__coinval2 == 0.
def test_giveProduct1_ChangeDivisibleByCoin2ValueOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct1UnsuitableChange(machine) == VendingMachine.Response.OK

# Tests correct UNSUITABLE_CHANGE returning.
def test_giveProduct1_UnsuitableChange():
    # Setting up some generic case.
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin2()
    assert machine.giveProduct1(3) == VendingMachine.Response.UNSUITABLE_CHANGE

# Helper function to reach default state in giveProduct1().
def set_machine_to_giveProduct1Default(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(2, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin1()
    return machine.giveProduct1(1)

# Tests coins1 decreasing on default state.
def test_giveProduct1_DefaultCoins1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1Default(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 0

# Tests coins2 decreasing on default state.
def test_giveProduct1_DefaultCoins2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1Default(machine)
    machine.enterAdminMode(ADMIN_CODE)
    # This also test for getCoins2() (bug 15) 
    assert machine.getCoins2() == 1

# Tests balance setting to zero on default state.
def test_giveProduct1_DefaultBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct1Default(machine)
    assert machine.getCurrentBalance() == 0

# Tests num1 decreasing on default state.
def test_giveProduct1_DefaultNum1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct1Default(machine)
    assert machine.getNumberOfProduct1() == MAX_PRODUCT1_N - 1

# Tests correct OK returning on default state.
def test_giveProduct1_DefaultOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct1Default(machine) == VendingMachine.Response.OK





"""
giveProduct2() tests.
"""
# Tests correct ILLEGAL_OPERATION returning.
def test_giveProduct2_InvalidMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.giveProduct2(1) == VendingMachine.Response.ILLEGAL_OPERATION

# Tests correct INVALID_PARAM returning for number <= 0.
@pytest.mark.parametrize("number", NON_POSITIVE_INT_TESTDATA)
def test_giveProduct2_InvalidParamNumberNonPositive(number: int):
    machine = VendingMachine()
    assert machine.giveProduct2(number) == VendingMachine.Response.INVALID_PARAM

# Tests correct INVALID_PARAM returning for number > MAX_PRODUCT2_N (bug 20).
@pytest.mark.parametrize("number", [MAX_PRODUCT2_N + 1, MAX_PRODUCT2_N + 2, MAX_PRODUCT2_N + 10**10])
def test_giveProduct2_InvalidParamNumberOverMax(number: int):
    machine = VendingMachine()
    assert machine.giveProduct2(number) == VendingMachine.Response.INVALID_PARAM

# Tests correct INSUFFICIENT_PRODUCT returning.
def test_giveProduct2_InsufficientProduct():
    machine = VendingMachine()
    assert machine.giveProduct2(1) == VendingMachine.Response.INSUFFICIENT_PRODUCT

# Tests correct INSUFFICIENT_MONEY returning on res < 0.
def test_giveProduct2_InsufficientMoney():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(1, 5)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin2()
    assert machine.giveProduct2(2) == VendingMachine.Response.INSUFFICIENT_MONEY

# Helper function to reach res > self.__coins2 * self.__coinval2 state in giveProduct2().
def set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    return machine.giveProduct2(2)

# Tests coins1 decreasing on res > self.__coins2 * self.__coinval2.
def test_giveProduct2_ChangeLargerThanCoins2SumCoins1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 5

# Tests coins2 setting to zero on res > self.__coins2 * self.__coinval2.
def test_giveProduct2_ChangeLargerThanCoins2SumCoins2Zeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 0

# Tests balance setting to zero on res > self.__coins2 * self.__coinval2.
def test_giveProduct2_ChangeLargerThanCoins2SumBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine)
    assert machine.getCurrentBalance() == 0

# Tests num2 decreasing on res > self.__coins2 * self.__coinval2.
def test_giveProduct2_ChangeLargerThanCoins2SumNum2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getNumberOfProduct2() == MAX_PRODUCT2_N - 2

# Tests correct OK returning on res > self.__coins2 * self.__coinval2.
def test_giveProduct2_ChangeLargerThanCoins2SumOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct2ChangeLargerThanCoins2Sum(machine) == VendingMachine.Response.OK

# Helper function to reach res % self.__coinval2 == 0 in giveProduct2().
def set_machine_to_giveProduct2UnsuitableChange(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.fillCoins(1, 1)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    machine.putCoin1()
    return machine.giveProduct2(2)

# Tests coins1 not changing to zero on res % self.__coinval2 == 0.
def test_giveProduct2_ChangeDivisibleByCoin2ValueCoins1NotChanging():
    machine = VendingMachine()
    set_machine_to_giveProduct2UnsuitableChange(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 5

# Tests coins2 not changing type to float on res % self.__coinval2 == 0 (bug 21).
def test_giveProduct2_ChangeDivisibleByCoin2ValueCoins2NotChanging():
    machine = VendingMachine()
    set_machine_to_giveProduct2UnsuitableChange(machine)
    # We need direct access to a field here to really check that we didn't change coins2 to float.
    assert isinstance(getattr(machine, "_VendingMachine__coins2"), int)

# Tests coin2 decreasing on res % self.__coinval2 == 0.
def test_giveProduct2_ChangeDivisibleByCoin2ValueCoins2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2UnsuitableChange(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 0

# Tests balance setting to zero on res % self.__coinval2 == 0.
def test_giveProduct2_ChangeDivisibleByCoin2ValueBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct2UnsuitableChange(machine)
    assert machine.getCurrentBalance() == 0

# Tests num2 decreasing on res % self.__coinval2 == 0.
def test_giveProduct2_ChangeDivisibleByCoin2ValueNum2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2UnsuitableChange(machine)
    assert machine.getNumberOfProduct2() == MAX_PRODUCT2_N - 2

# Tests correct OK returning on res % self.__coinval2 == 0.
def test_giveProduct2_ChangeDivisibleByCoin2ValueOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct2UnsuitableChange(machine) == VendingMachine.Response.OK

# Tests correct UNSUITABLE_CHANGE returning.
def test_giveProduct2_UnsuitableChange():
    # Setting up some generic case.
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(1, 1)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin2()
    assert machine.giveProduct2(3) == VendingMachine.Response.UNSUITABLE_CHANGE

# Helper function to reach default state in giveProduct2().
def set_machine_to_giveProduct2Default(machine: VendingMachine):
    # Setting up some generic case.
    machine.enterAdminMode(ADMIN_CODE)
    machine.setPrices(1, 2)
    machine.fillProducts()
    machine.exitAdminMode()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin2()
    machine.putCoin1()
    return machine.giveProduct2(1)

# Tests coins1 decreasing on default state (bug 22).
def test_giveProduct2_DefaultCoins1Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2Default(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins1() == 0

# Tests coins2 decreasing on default state (bug 22).
def test_giveProduct2_DefaultCoins2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2Default(machine)
    machine.enterAdminMode(ADMIN_CODE)
    assert machine.getCoins2() == 1

# Tests balance setting to zero on default state.
def test_giveProduct2_DefaultBalanceZeroed():
    machine = VendingMachine()
    set_machine_to_giveProduct2Default(machine)
    # This also test putCoin2() (bug 16).
    assert machine.getCurrentBalance() == 0

# Tests num2 decreasing on default state.
def test_giveProduct2_DefaultNum2Decreasing():
    machine = VendingMachine()
    set_machine_to_giveProduct2Default(machine)
    assert machine.getNumberOfProduct2() == MAX_PRODUCT2_N - 1

# Tests correct OK returning on default state.
def test_giveProduct2_DefaultOK():
    machine = VendingMachine()
    assert set_machine_to_giveProduct2Default(machine) == VendingMachine.Response.OK
