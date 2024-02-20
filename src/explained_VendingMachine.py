class VendingMachine:
    class Mode:
        OPERATION = 1
        ADMINISTERING = 2

    class Response:
        OK = 1
        ILLEGAL_OPERATION = 2
        INVALID_PARAM = 3
        CANNOT_PERFORM = 4
        TOO_BIG_CHANGE = 5
        UNSUITABLE_CHANGE = 6
        INSUFFICIENT_PRODUCT = 7
        INSUFFICIENT_MONEY = 8

    __coinval1 = 1
    __coinval2 = 2

    def __init__(self):
        self.__id = 117345294655382
        self.__mode = VendingMachine.Mode.OPERATION
        # max amount of product 1 and 2
        self.__max1 = 30
        self.__max2 = 40
        # current amount of product 1 and 2
        self.__num1 = 0
        self.__num2 = 0
        # price of product 1 and 2
        self.__price1 = 8
        self.__price2 = 5
        # coins storage capacity for coins 1 and 2
        self.__maxc1 = 50
        self.__maxc2 = 50
        # current amount of coins 1 and 2
        self.__coins1 = 0
        self.__coins2 = 0
        self.__balance = 0 # Current balance (during one user-session).

    def getNumberOfProduct1(self): # Simple getter [+].
        return self.__num1

    def getNumberOfProduct2(self): # Simple getter [+].
        return self.__num2

    def getCurrentBalance(self): # Simple getter [+].
        return self.__balance

    def getCurrentMode(self): # Simple getter [+].
        return self.__mode

    def getCurrentSum(self): # [+].
        if self.__mode == VendingMachine.Mode.OPERATION:
            return 0
        return self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2

    def getCoins1(self): # [+].
        if self.__mode == VendingMachine.Mode.OPERATION:
            return 0 
        return self.__coins1

    def getCoins2(self): # [+].
        if self.__mode == VendingMachine.Mode.OPERATION:
            return 0 # [fixed typo] [fixed].
        return self.__coins2

    def getPrice1(self): # Simple getter [+].
        return self.__price1

    def getPrice2(self): # Simple getter [+].
        return self.__price2

    def fillProducts(self):
        if self.__mode != VendingMachine.Mode.ADMINISTERING: # [fixed].
            return VendingMachine.Response.ILLEGAL_OPERATION
        self.__num1 = self.__max1 # [fixed].
        self.__num2 = self.__max2
        return VendingMachine.Response.OK

    def fillCoins(self, c1: int, c2: int):
        if self.__mode == VendingMachine.Mode.OPERATION:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if c1 <= 0 or c1 > self.__maxc1: # [fixed].
            return VendingMachine.Response.INVALID_PARAM
        if c2 <= 0 or c2 > self.__maxc2: # [fixed].
            return VendingMachine.Response.INVALID_PARAM
        self.__coins1 = c1
        self.__coins2 = c2
        return VendingMachine.Response.OK

    def enterAdminMode(self, code: int):
        if code != self.__id:
            return VendingMachine.Response.INVALID_PARAM # [fixed] (first must return invalid_param if codes don't match).
        if self.__balance != 0:
            return VendingMachine.Response.CANNOT_PERFORM # [fixed].
        self.__mode = VendingMachine.Mode.ADMINISTERING
        return VendingMachine.Response.OK

    def exitAdminMode(self):
        self.__mode = VendingMachine.Mode.OPERATION

    def setPrices(self, p1: int, p2: int):
        if self.__mode == VendingMachine.Mode.OPERATION:
            return VendingMachine.Response.ILLEGAL_OPERATION
        self.__price1 = p1
        self.__price2 = p2
        return VendingMachine.Response.OK

    def putCoin1(self):
        if self.__mode == VendingMachine.Mode.ADMINISTERING:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if self.__coins2 == self.__maxc2:
            return VendingMachine.Response.CANNOT_PERFORM
        self.__balance += self.__coinval2
        self.__coins1 += 1 # [fixed].
        return VendingMachine.Response.OK

    def putCoin2(self):
        if self.__mode == VendingMachine.Mode.ADMINISTERING:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if self.__coins1 == self.__maxc1:
            return VendingMachine.Response.CANNOT_PERFORM
        self.__balance += self.__coinval1
        self.__coins1 += 1
        return VendingMachine.Response.OK

    def returnMoney(self):
        if self.__mode == VendingMachine.Mode.ADMINISTERING:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if self.__balance == 0:
            return VendingMachine.Response.OK
        if self.__balance > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2:
            return VendingMachine.Response.TOO_BIG_CHANGE
        if self.__balance > self.__coins2 * self.__coinval2:
            # using coinval1 == 1
            self.__coins1 -= self.__balance - self.__coins2 * self.__coinval2
            self.__coins2 = 0
            self.__balance = 0
            return VendingMachine.Response.OK
        if self.__balance % self.__coinval2 == 0:
            self.__coins2 -= self.__balance // self.__coinval2
            self.__balance = 0
            return VendingMachine.Response.OK
        if self.__coins1 == 0:
            # using coinval1 == 1
            return VendingMachine.Response.UNSUITABLE_CHANGE
        # using coinval1 == 1
        self.__coins1 -= self.__balance // self.__coinval2
        self.__coins2 -= 1
        self.__balance = 0
        return VendingMachine.Response.OK

    def giveProduct1(self, number: int):
        if self.__mode == VendingMachine.Mode.ADMINISTERING:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if number <= 0 or number > self.__max1: # [fixed].
            return VendingMachine.Response.INVALID_PARAM
        if number > self.__num1:
            return VendingMachine.Response.INSUFFICIENT_PRODUCT

        res = self.__balance - number * self.__price1
        if res < 0:
            return VendingMachine.Response.INSUFFICIENT_MONEY
        if res > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2:
            return VendingMachine.Response.TOO_BIG_CHANGE
        if res > self.__coins2 * self.__coinval2:
            # using coinval1 == 1
            self.__coins1 -= res - self.__coins2 * self.__coinval2
            self.__coins2 = 0
            self.__balance = 0
            self.__num1 -= number
            return VendingMachine.Response.OK
        if res % self.__coinval2 == 0:
            self.__coins2 -= res / self.__coinval2
            self.__balance = 0
            self.__num1 -= number
            return VendingMachine.Response.OK
        if self.__coins1 == 0:
            return VendingMachine.Response.UNSUITABLE_CHANGE
        self.__coins1 -= 1
        self.__coins2 -= res // self.__coinval2
        self.__balance = 0
        self.__num1 -= number
        return VendingMachine.Response.OK

    def giveProduct2(self, number: int):
        if self.__mode == VendingMachine.Mode.ADMINISTERING:
            return VendingMachine.Response.ILLEGAL_OPERATION
        if number <= 0 or number >= self.__max2:
            return VendingMachine.Response.INVALID_PARAM
        if number > self.__num2:
            return VendingMachine.Response.INSUFFICIENT_PRODUCT

        res = self.__balance - number * self.__price2
        if res < 0:
            return VendingMachine.Response.INSUFFICIENT_MONEY
        if res > self.__coins1 * self.__coinval1 + self.__coins2 * self.__coinval2:
            return VendingMachine.Response.INSUFFICIENT_MONEY
        if res > self.__coins2 * self.__coinval2:
            # using coinval1 == 1
            self.__coins1 -= res - self.__coins2 * self.__coinval2
            self.__coins2 = 0
            self.__balance = 0
            self.__num2 -= number
            return VendingMachine.Response.OK
        if res % self.__coinval2 == 0:
            self.__coins2 -= res / self.__coinval2
            self.__balance = 0
            self.__num2 -= number
            return VendingMachine.Response.OK
        if self.__coins1 == 0:
            return VendingMachine.Response.UNSUITABLE_CHANGE
        self.__coins1 -= res // self.__coinval2
        self.__coins2 -= 1
        self.__balance = 0
        self.__num2 -= number
        return VendingMachine.Response.OK
