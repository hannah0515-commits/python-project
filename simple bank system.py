
import pickle
import os

def loadData():
    # for loading the file in binary mode for existing account information
    dbfile = open('bank_ac.dat', 'rb')
    data_list = pickle.load(dbfile)
    dbfile.close()
    return data_list

def get_balance(ac_num):
    #get the account in the file saved
    if os.path.exists("bank_ac.dat") == False:
        bal = 0
    else:
        bal = loadData()[ac_num][1]
    return bal

def get_cheque_no(ac_num):
    #get the account in the file saved
    if os.path.exists("bank_ac.dat") == False:
        cheque = 0
    else:
        cheque = loadData()[ac_num][2]
    return cheque

#account information dictionary
ac = {"111":["Current account",get_balance("111")] , "222":["Deposit account", get_balance("222")], "333":["Restricted account", get_balance("333")], "444":["Account with Overdraft Facility", get_balance("444")]}

#bank class which contains all basic information and function of accounts
class bank():
    #define account name, account number and balance as initial
    def __init__(self, name, ac_num, bal):
        self.name = name
        self.ac_num = ac_num
        self.bal = bal

    #define the to string method to print the name and the balance
    def __str__(self):
        return "Account name: " + str(self.name) + "\t Account balance: "  + str(self.bal)

    #define the deposit method
    def deposit(self, amount):
        if amount >0:
            self.bal += amount
        else:
            print("cannot deposit negative value")
        return self.bal

    #define the withdraw method
    def withdraw(self, amount):
        if amount > 0:
            self.bal -= amount
        else:
            print("cannot withdraw negative value")
        return self.bal

#current account subclass from bank
class current(bank):
    #account number is 111, the cheque count at the beginning is 0
    def __init__(self):
        super().__init__("Current account", "111", get_balance("111"))
        self.cheque = get_cheque_no(self.ac_num)  #define the number of cheque count

    #current account withdraw method
    def withdraw_from_ac(self, amount):
        if amount<=self.bal:
            self.withdraw(amount)
            #increase the cheque count for every withdrawal
            self.cheque += 1
            print ("no of cheque: "+ str(self.cheque))
        else:
            print("insufficient balance")   #if the balance is insufficient
        return self.bal

#deposit account class as the subclass of bank
class deposit(bank):
    def __init__(self):
        super().__init__("Deposit account", "222", get_balance("222"))
        #define the number if withdraw as 0 at the beginning
        self.counter = get_cheque_no(self.ac_num)

    #withdraw method for deposit account
    def withdraw_from_ac(self, amount):
        max_no_withdraw = 3  #define the maximum number of withdrawl
        if amount>self.bal:   #if the balance is insufficient
            print("insufficient balance")
        elif self.counter < max_no_withdraw:   #if the number of withdrawl does not exceed 3
            self.withdraw(amount)
            self.counter +=1        #increase the count of withdrawl for every withdrawl
            print("The number of withdrawal: "+ str(self.counter))
        else:
            print ("Exceed maximum number of time of withdrawal")
        return self.bal

    def deposit(self, amount):    #overwrite deposit method for saving interests
        interest_rate_pa = 0.02    #assume every amount deposit to this account keep for a month
        if amount >0:
            interest_per_month= round((self.bal+amount)* interest_rate_pa/12, 2)   #calculate the interest per month
            print("interest per month: "+ str(interest_per_month))
            self.bal = self.bal + amount + interest_per_month
        else:
            print("cannot deposit negative value")
        return self.bal

#restricted account class as the subclass of current account
class restricted(current):
    def __init__(self):
        super().__init__()
        #overwrite the initials
        self.name = "Restricted account"
        self.ac_num = "333"
        self.bal = get_balance("333")
        self.cheque = get_cheque_no(self.ac_num)

    #define the withdraw method, inherite from current account
    def withdraw_restricted(self, amount):
        max_withdraw_limit = 10000         #proceed to withdraw if the withdraw amount within limit
        if amount <= max_withdraw_limit:
            self.withdraw_from_ac(amount)     #inherite the withdraw method from current account
        else:
            print("Exceed maximum withdrawal limit")     #if the amount of withdrawl larger than 10000
        return self.bal

#define class overdue as subclass as current account
class overdue(current):
    def __init__(self):   #overwrite the initials
        super().__init__()
        self.name = "Account with Overdraft Facility"
        self.ac_num = "444"
        self.bal = get_balance("444")
        self.cheque = get_cheque_no(self.ac_num)

    #overwrite the withdraw method
    def withdraw_from_ac(self,amount):
        max_overdue_limit = 100
        if amount <= self.bal+max_overdue_limit:      #if the amount is within the balance+ overdue amount
            self.withdraw(amount)       #proceed to withdrawal
            self.cheque += 1        #increase the cheque count
            print("no of cheque: " + str(self.cheque))
        else:
            print("Exceed overdue limit")     #print exceed overdue limit
        return self.bal

#define the action method after entering and verifying the account number
def further_action(ac_num):
    while True:
        further = input("further action? (y/n): ")
        if further == "y":
            further_input = input("please select action (withdraw(w)/deposit(d)): ")   #let the user choose deposit or withdraw;
            if further_input =="d":
                print(deposit_step(ac_num))
            elif further_input =="w":
                print(withdraw_step(ac_num))
            else:
                print("invalid")
        elif further =="n":
            print("finish")
            storeData()
            break
        else:
            print("invalid")  #print invalid if the user not entering w/d

#define the deposit method procedure according to the account number
def deposit_step(ac_num):
    if ac_num=="111":
        try:
            amount= float(input("Please enter the amount to deposit: "))
            current_ac.deposit(amount)
        except ValueError:
            print("invalid")
        return ("deposit to " + current_ac.name+ " new balance is %.2f" %current_ac.bal)
    elif ac_num=="222":
        try:
            amount= float(input("Please enter the amount to deposit: "))
            deposit_ac.deposit(amount)
        except ValueError:
            print("invalid")
        return ("deposit to " + deposit_ac.name+ " new balance is %.2f" %deposit_ac.bal)
    elif ac_num=="333":
        try:
            amount= float(input("Please enter the amount to deposit: "))
            restricted_ac.deposit(amount)
        except ValueError:
            print("invalid")
        return ("deposit to " + restricted_ac.name+ " new balance is %.2f" %restricted_ac.bal)
    elif ac_num=="444":
        try:
            amount= float(input("Please enter the amount to deposit: "))
            overdue_ac.deposit(amount)
        except ValueError:
            print("invalid")
        return ("deposit to " + overdue_ac.name+ " new balance is %.2f" %overdue_ac.bal)
    else:
        print("invalid")

#define the withdrawl procedure according to the account number
def withdraw_step(ac_num):
    if ac_num == "111":
        try:
            amount = float(input("Please enter the amount to withdraw: "))
            current_ac.withdraw_from_ac(amount)
        except ValueError:
            print("invalid")
        return ("withdraw to " + current_ac.name+ " new balance is %.2f" % current_ac.bal)
    elif ac_num == "222":
        try:
            amount = float(input("Please enter the amount to withdraw: "))
            deposit_ac.withdraw_from_ac(amount)
        except ValueError:
            print("invalid")
        return ("withdraw to " + deposit_ac.name+ " new balance is %.2f" % deposit_ac.bal)
    elif ac_num == "333":
        try:
            amount = float(input("Please enter the amount to withdraw: "))
            restricted_ac.withdraw_restricted(amount)
        except ValueError:
            print("invalid")
        return ("withdraw to " + restricted_ac.name+ " new balance is %.2f" % restricted_ac.bal)
    elif ac_num == "444":
        try:
            amount = float(input("Please enter the amount to withdraw: "))
            overdue_ac.withdraw_from_ac(amount)
        except ValueError:
            print("invalid")
        return ("withdraw to " + overdue_ac.name+ " new balance is %.2f" % overdue_ac.bal)
    else:
        print("invalid")

#store the data into file
def storeData():
    #define the data list
    data_list = {"111":[current_ac.name, current_ac.bal, current_ac.cheque], "222":[deposit_ac.name, deposit_ac.bal, deposit_ac.counter],
                 "333":[restricted_ac.name, restricted_ac.bal, restricted_ac.cheque], "444":[overdue_ac.name, overdue_ac.bal, overdue_ac.cheque]}
    dbfile = open('bank_ac.dat', 'wb')

    # source, destination
    pickle.dump(data_list, dbfile)
    dbfile.close()



#create account objects
current_ac = current()
deposit_ac = deposit()
restricted_ac = restricted()
overdue_ac = overdue()



#define main function
def main():
    #check if the bank information exist
    #if no previous data print no data
    if os.path.exists("bank_ac.dat") == False:
      print("no previous data")
    else:
        #if there is existing file, load file
        loadData()
        #print file content
        for keys in loadData():
            print(keys, '=>', loadData()[keys])
    #ask user to input account number
    ac_num = str(input("please input the account number: "))
    if ac_num in ac:   #check if account number exist in the dictionary, if exists, print account detail
        print("Account name: "+ ac[ac_num][0] +"\n"+ "Account balance: " + str(ac[ac_num][1]))
        further_action(ac_num)  #function action
    else:
        print("no such account")

main()


