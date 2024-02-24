from VendingMachine import VendingMachine
import pytest
from typing import Callable

# Assuming we know the admin code.
ADMIN_CODE = 117345294655382

# Typical edge-case int values.
INT_TESTDATA = [-10**100, -10**10, -3489672334, -1, 0, 1, 17368216213, 10**10, 10**100]

"""
enterAdminMode() tests.
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
    assert machine.getCurrentMode() == VendingMachine.Mode.ADMINISTERING

# getNumberOfProduct1: changing.
def test_getNumberOfProduct1():
    machine = VendingMachine()
    # The only way to change the number of product1 is via fillProducts().
    machine.enterAdminMode(1234)





"""
exitAdminMode() tests.
"""
def test_exitAdminMode_AfterAdminMode():
    machine = VendingMachine()
    machine.enterAdminMode(ADMIN_CODE)
    machine.exitAdminMode()
    assert machine.getCurrentMode() == VendingMachine.Mode.OPERATION

def test_exitAdminMode_AfterOperationMode():
    machine = VendingMachine()
    machine.exitAdminMode()
    assert machine.getCurrentMode() == VendingMachine.Mode.OPERATION
