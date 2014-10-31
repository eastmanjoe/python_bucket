#!/usr/bin/env python

'''
Quiz 6 functions
'''

class BankAccount:
    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self.acct_bal = initial_balance
        self.fees_paid = 0

    def deposit(self, amount):
        """Deposits the amount into the account."""
        self.acct_bal += amount

    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        self.acct_bal -= amount

        if self.acct_bal < 0:
            self.acct_bal -= 5
            self.fees_paid += 5

    def get_balance(self):
        """Returns the current balance in the account."""
        return self.acct_bal

    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self.fees_paid


#my_account = BankAccount(10)
#print my_account.get_balance(), my_account.get_fees()
#my_account.withdraw(15)
#print my_account.get_balance(), my_account.get_fees()
#my_account.deposit(20)
#print my_account.get_balance(), my_account.get_fees()

# my_account = BankAccount(10)
# my_account.withdraw(5)
# my_account.deposit(10)
# my_account.withdraw(5)
# my_account.withdraw(15)
# my_account.deposit(20)
# my_account.withdraw(5)
# my_account.deposit(10)
# my_account.deposit(20)
# my_account.withdraw(15)
# my_account.deposit(30)
# my_account.withdraw(10)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.withdraw(50)
# my_account.deposit(30)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.withdraw(5)
# my_account.deposit(20)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.deposit(30)
# my_account.withdraw(25)
# my_account.withdraw(5)
# my_account.deposit(10)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.withdraw(10)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.deposit(30)
# my_account.withdraw(25)
# my_account.withdraw(10)
# my_account.deposit(20)
# my_account.deposit(10)
# my_account.withdraw(5)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.withdraw(5)
# my_account.withdraw(15)
# my_account.deposit(10)
# my_account.withdraw(5)
# print my_account.get_balance(), my_account.get_fees()
# Answer: -60 75

# account1 = BankAccount(10)
# account1.withdraw(15)
# account2 = BankAccount(15)
# account2.deposit(10)
# account1.deposit(20)
# account2.withdraw(20)
# print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()

account1 = BankAccount(20)
account1.deposit(10)
account2 = BankAccount(10)
account2.deposit(10)
account2.withdraw(50)
account1.withdraw(15)
account1.withdraw(10)
account2.deposit(30)
account2.withdraw(15)
account1.deposit(5)
account1.withdraw(10)
account2.withdraw(10)
account2.deposit(25)
account2.withdraw(15)
account1.deposit(10)
account1.withdraw(50)
account2.deposit(25)
account2.deposit(25)
account1.deposit(30)
account2.deposit(10)
account1.withdraw(15)
account2.withdraw(10)
account1.withdraw(10)
account2.deposit(15)
account2.deposit(10)
account2.withdraw(15)
account1.deposit(15)
account1.withdraw(20)
account2.withdraw(10)
account2.deposit(5)
account2.withdraw(10)
account1.deposit(10)
account1.deposit(20)
account2.withdraw(10)
account2.deposit(5)
account1.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account2.deposit(10)
account2.deposit(15)
account2.deposit(20)
account1.withdraw(15)
account2.deposit(10)
account1.deposit(25)
account1.deposit(15)
account1.deposit(10)
account1.withdraw(10)
account1.deposit(10)
account2.deposit(20)
account2.withdraw(15)
account1.withdraw(20)
account1.deposit(5)
account1.deposit(10)
account2.withdraw(20)
print account1.get_balance(), account1.get_fees(), account2.get_balance(), account2.get_fees()
# Answer: -55 45 45 20


# Quiz 6b

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)

CARD_TO_FIND = (12, 3)

card_pos = (CARD_CENTER[0] + CARD_TO_FIND[0] * CARD_SIZE[0], CARD_CENTER[1] + CARD_TO_FIND[1] * CARD_SIZE[1])

print card_pos

def list_extend_many(lists):
#    result = []
#    while len(lists) > 0:
#        result.extend(lists.pop(0))
#    result = []
#    i = 0
#    while i < len(lists):
#        result.extend(lists[i])
#        i += 1
    result = []
    for i in range(len(lists)):
        result.extend(lists[i])

    return result

print list_extend_many([[1,2], [3], [4, 5, 6], [7]])

n = 1000
numbers = range(2, n)
print numbers

results = []

while len(numbers) > 0:
    results.append(numbers.pop(0))

    for x in numbers:
        if x % results[-1] == 0:
            numbers.remove(x)

print results
print len(results)

# question 8
wumpus_fast = 1
wumpus_slow = 1000
year = 1
print year, wumpus_slow, wumpus_fast

while True:
#while year <= 3:
    wumpus_fast = (wumpus_fast * 2) * 0.7
    wumpus_slow = (wumpus_slow * 2) * 0.6

    if wumpus_fast < wumpus_slow:
        year += 1
    else:
        break
#    print year, wumpus_slow, wumpus_fast

print year, wumpus_slow, wumpus_fast