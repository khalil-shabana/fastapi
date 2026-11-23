import pytest
from calculations import add,divide,multiply,subtract,\
                         BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (2,2,4),
    (7,1,8),
    (9,1,10)
])

def test_add(num1,num2,expected):
    print("testing add function")
    assert add(num1,num2) == expected
    
def test_subtract():
    assert subtract(9,5) == 4
    
def test_multiply():
    assert multiply(9,5) == 45
    
def test_divide():
    assert divide(9,3) == 3
    
def test_set_initial_amount(bank_account):
   assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70
    

def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_interest_collector(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
    
    
@pytest.mark.parametrize("deposit, withdraw, expected", [
    (200,100,100),
    (150,50,100),
    (9,1,8),
    #(100,500,-400) # raise an error
])

def test_bank_transaction(zero_bank_account, deposit, withdraw, expected):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected
    
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)  
    