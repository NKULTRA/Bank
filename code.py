from random import sample
import sqlite3


class Bank:

    def __init__(self):
        self.number = None
        self.pin = None
        self.id = None
        self.balance = None
        self.db = None
        self.conn = None
        self.database()

    def database(self):
        self.db = sqlite3.connect('card.s3db')
        self.conn = self.db.cursor()
        self.conn.execute(
            'CREATE TABLE if not exists card (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            number TEXT, 
            pin TEXT, 
            balance INTEGER default 0)'
        )

    def select_task(self, number):
        self.conn.execute(
            'select number, pin, balance from card where number =:numb',{'numb':number}
        )
        data = self.conn.fetchone()
        return data

    def add_inc(self):
        try:
            add = int(input('\nEnter income:\n'))
        except ValueError:
            print('\nYou could only add money in form of numbers!\n')
            self.log_in_menu()
        else:
            if add < 0:
                print('\nonly positive value can be added!\n')
                self.log_in_menu()
            self.conn.execute(
                'update card set balance = balance + ? where number = ?', (add, self.number)
            )
            self.db.commit()
            self.balance += add
            print('Income was added!')
            self.log_in_menu()

    def transfer(self):
        print('\nTransfer')
        other = input('Enter card number:\n')
        data = self.select_task(other)
        if data and data[0] == self.number:
            print("You can't transfer money to the same account!")
        elif self.check(other[:len(other) - 1]) != other[-1]:
            print('Probably you made a mistake in the card number.')
            print('Please try again!\n')
        elif not data:
            print('Such a card does not exist')
        else:
            add = int(input('Enter how much money you want to transfer:\n'))
            if add > self.balance:
                print('Not enough money!')
            else:
                self.conn.execute(
                    'update card set balance = balance - ? where number = ?', (add, self.number)
                )
                self.conn.execute(
                    'update card set balance = balance + ? where number = ?', (add, other)
                )
                self.db.commit()
                self.balance -= add
                print('Success!\n')
        self.log_in_menu()

    def close_acc(self):
        self.conn.execute(
            'delete from card where number = ?', (self.number,)
        )
        self.db.commit()
        self.number = None
        self.pin = None
        print('The account has been closed!\n')
        self.start_menu()

    def start_menu(self):
        print('1. Create an account')
        print('2. Log into account')
        print('0. Exit')
        try:
            election = int(input())
        except ValueError:
            print('\nYou could only choose numbers 1, 2, 0!\n')
            self.start_menu()
        else:
            if election not in (1, 2, 0):
                print('\nYou could only choose numbers 1, 2, 0!\n')
                self.start_menu()
            else:
                if election == 1:
                    self.get_account()
                    self.start_menu()
                elif election == 2:
                    self.log_in()
                elif election == 0:
                    print('\nBye!')
                    self.db.close()
                    exit()

    def log_in(self):
        print('\nEnter your card number:')
        self.number = input()
        print('Enter your PIN:')
        self.pin = input()

        if self.select_task(self.number):
            number, pin, balance = self.select_task(self.number)
        else:
            number, pin, balance = None, None, None

        if number and pin == self.pin:
            print('\nYou have successfully logged in!')
            self.number, self.pin, self.balance = number, pin, balance
            self.log_in_menu()
        else:
            print('\nWrong card number or PIN!\n')
            self.number = None
            self.pin = None
            self.start_menu()

    def log_in_menu(self):
        print('\n1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

        try:
            election = int(input())
        except ValueError:
            print('\nYou could only choose numbers 1, 2, 3, 4, 5, 0!\n')
            self.log_in_menu()
        else:
            if election not in (1, 2, 3, 4, 5, 0):
                print('\nYou could only choose numbers 1, 2, 3, 4, 5, 0!\n')
                self.log_in_menu()
            else:
                if election == 1:
                    print('\nBalance: ' + str(self.balance))
                    self.log_in_menu()
                elif election == 2:
                    self.add_inc()
                elif election == 3:
                    self.transfer()
                elif election == 4:
                    self.close_acc()
                elif election == 5:
                    print('\nYou have successfully logged out!\n')
                    self.number = None
                    self.pin = None
                    self.balance = None
                    self.start_menu()
                elif election == 0:
                    print('\nBye!')
                    self.db.close()
                    exit()

    def get_account(self):
        previous = '400000' + ''.join(str(x) for x in sample(list(range(10)), 9))
        card_number = previous + self.check(previous)
        pin = ''.join(str(x) for x in sample(list(range(10)), 4))
        print('\nYour card has been created')
        print('Your card number:')
        print(card_number)
        print('Your card PIN:')
        print(pin + '\n')
        self.conn.execute(
            'INSERT INTO card (number, pin, balance) values (?,?,?)',(card_number, pin, 0)
        )
        self.db.commit()

    @staticmethod
    def check(number):
        first = [
            int(number[x]) * 2 if (x + 1) % 2 == 1 else int(number[x]) for x in range(len(number))
        ]
        second = [x - 9 if x > 9 else x for x in first]
        last = sum(second)

        return str(10 - last % 10) if last % 10 != 0 else '0'


if __name__ == '__main__':
    customer = Bank()
    customer.start_menu()

