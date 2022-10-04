#!/usr/bin/env python3
# encoding: utf-8
from secret import flag
from hashlib import sha256
from Crypto.Util.number import inverse, long_to_bytes, bytes_to_long, getStrongPrime as getPrime
from collections import defaultdict
import signal
import random
import string
from os import urandom
assert flag[:7]=='THUCTF{' and flag[-1]=='}'
flag=flag[7:-1]

class Flag():
    def __init__(self, owner, price, content):
        self.price = price
        self.owner = owner
        self.content = content

    def getOwner(self):
        return self.owner

    def getPrice(self):
        return self.price

    def setOwner(self, owner):
        self.owner = owner
    
    def setPrice(self, price):
        self.price = price


class Market():
    def __init__(self, flag):
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.e = 0x10001
        self.d = inverse(self.e, (self.p-1)*(self.q-1))
        self.dp = self.d % (self.p-1)
        self.dq = self.d % (self.q-1)
        self.user = False
        self.N = self.p*self.q
        self.balance = defaultdict(int)
        self.store = [Flag(b'admin', 0x233333333333333, flag)]
        self.command = [b"r3g1st3r", b"10g1n", b"v13w", b"5311", b"6uy", b"s3tpr1c3", b"l0g0ut", b"3x1t"]
        self.USER_MAX = 10
        self.ITEM_MAX = 100

    def recv(self, prompt):
        ret = input(prompt)
        if len(ret) > 130:
            print("Too long")
            return 
        return ret.encode()

    def recvfromhex(self, prompt):
        rethex = input(prompt)
        try:
            ret = bytes.fromhex(rethex)
            if len(ret) > 130:
                print("Too long")
                return b""
        except:
            print("Format Error")
            return b""
        return ret

    def register(self):
        u = self.recv("Username:")
        if u == b"admin":
            print("Hackeeeeeer")
            return
        if (len(self.balance) < self.USER_MAX) and (u not in self.balance):
            self.balance[u] = 100
            self.user = u
            print(f"sig: {self.sign(self.user, self.command[0])}")

    def login(self):
        u = self.recv("Login: ")
        if (not self.user) and (self.balance[u] > 0):
            self.user = u
            print(f"sig: {self.sign(self.user, self.command[1])}")
        else:
            print("Login Error")
            self.user = False

    def view(self, idx, sig):
        if not self.user:
            return

        if self.user != b'admin':
            print(f"sig: {self.sign(self.user, self.command[2])}")

        if idx >= len(self.store) or idx < 0:
            print("Error")
            return
        
        item = self.store[idx]
        if self.user == item.getOwner() and self.verify(self.user, self.command[2], sig):
            print(item.content)

    def sell(self):
        if (not self.user):
            return
        if len(self.store) > self.ITEM_MAX:
            print("No more space")
            return
        print(f"sig: {self.sign(self.user, self.command[3])}")
        try:
            price = int(self.recv("Price:"))
            flag = self.recv("Flag:")
            if price > 100:
                print("Too Expensive")
                return 
        except:
            print("Sell Error")
            return
        NewFlag = Flag(self.user, price, flag)
        self.store.append(NewFlag)

    def buy(self, idx):
        if not self.user:
            return
        print(f"sig: {self.sign(self.user, self.command[4])}")
        if idx >= len(self.store) or idx < 0:
            print("Error")
            return
        item = self.store[idx]
        if self.balance[self.user] > item.getPrice():
            self.balance[item.getOwner()] += item.getPrice()
            item.setOwner(self.user)
            self.balance[self.user] -= item.getPrice()

    def setprice(self, idx, price, sig):
        if not self.user:
            return
        print(f"sig: {self.sign(self.user, self.command[5])}")
        if idx >= len(self.store) or idx < 0:
            print("Error")
            return
        item = self.store[idx]
        if item.getOwner() == self.user and self.verify(item.getOwner(), f"{price}".encode(), sig):
            item.setPrice(price)

    def logout(self):
        if not self.user:
            return
        print(f"sig: {self.sign(self.user, self.command[6])}")
        self.user = False

    def showmenu(self):
        menu = "="*20 + '\n'
        menu += f"Login: [{self.user.decode() if self.user else self.user}, {self.balance[self.user]}]\n"
        for idx, c in enumerate(self.command):
            menu += f"{idx+1}.{c.decode()}\n"
        menu += "Choice:"
        return menu

    def sign(self, u, message):
        if not self.user:
            return
        mhash = sha256(u+message).digest()
        m = int.from_bytes(mhash, "big")
        sig_p = pow(m, self.dp, self.p)
        sig_q = pow(m, self.dq, self.q)
        alpha = self.q*inverse(self.q, self.p)
        beta = self.p*inverse(self.p, self.q)
        return long_to_bytes((alpha*sig_p+beta*sig_q) % self.N).hex()

    def verify(self, user, message, sig):
        if not self.user:
            return
        return long_to_bytes(pow(bytes_to_long(sig), self.e, self.N)) == sha256(user+message).digest()

    def timeout_handler(self, signum, frame):
        raise TimeoutError

    def proof_of_work(self):
        random.seed(urandom(8))
        proof = ''.join([random.choice(string.ascii_letters + string.digits + '!#$%&*-?') for _ in range(20)])
        digest = sha256(proof.encode()).hexdigest()
        print('sha256(XXXX + {}) == {}'.format(proof[4: ], digest))
        x = self.recv('Give me XXXX:')
        x = (x.strip()).decode('utf-8') 
        if len(x) != 4 or sha256((x + proof[4: ]).encode()).hexdigest() != digest: 
            return False
        return True

    def run(self):
        try:
            signal.signal(signal.SIGALRM, self.timeout_handler)
            signal.alarm(50)
            if not self.proof_of_work():
                print('You must pass the PoW!')
                exit(0)
            signal.alarm(60)
            while True:
                choice = int(self.recv(self.showmenu()))
                if 8 > choice >= 3 and (not self.user):
                    print("Please Login")
                elif choice == 1:
                    self.register()
                elif choice == 2:
                    self.login()
                elif choice == 3:
                    idx = int(self.recv("idx:"))
                    sig = self.recvfromhex("sig:")
                    self.view(idx, sig)
                elif choice == 4:
                    self.sell()
                elif choice == 5:
                    idx = int(self.recv("idx:"))
                    self.buy(idx)
                elif choice == 6:
                    idx = int(self.recv("idx:"))
                    price = int(self.recv("price:"))
                    sig = self.recvfromhex("sig:")
                    self.setprice(idx, price, sig)
                elif choice == 7:
                    self.logout()
                elif choice == 8:
                    exit(0)
                else:
                    print("Error")
        except TimeoutError:
            print("Timeout")
            exit(0)
        except:
            print("Wtf?")
            exit(0)

if __name__ == "__main__":
    market = Market(flag)
    market.run()