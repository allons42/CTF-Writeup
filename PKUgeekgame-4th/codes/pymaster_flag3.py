import random
import base64

# flag1 = "flag{you_Ar3_tHE_MaSTer_OF_PY7h0n}"


class node:
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.father = None
        self.lchild = None
        self.rchild = None


class tree:
    def __init__(self):
        self.I = None

    def tree(self, tmp):
        while tmp.father != None:
            if tmp.father.father == None:
                if tmp == tmp.father.lchild:
                    self.func2(tmp.father)
                else:
                    self.func1(tmp.father)
            elif (
                tmp == tmp.father.lchild
                and tmp.father == tmp.father.father.lchild
            ):
                self.func2(tmp.father.father)
                self.func2(tmp.father)
            elif (
                tmp == tmp.father.rchild
                and tmp.father == tmp.father.father.rchild
            ):
                self.func1(tmp.father.father)
                self.func1(tmp.father)
            elif (
                tmp == tmp.father.rchild
                and tmp.father == tmp.father.father.lchild
            ):
                self.func1(tmp.father)
                self.func2(tmp.father)
            else:
                self.func2(tmp.father)
                self.func1(tmp.father)

    # 在节点x处左旋
    def func1(self, x):
        y = x.rchild
        x.rchild = y.lchild
        if y.lchild != None:
            y.lchild.father = x
        y.father = x.father
        if x.father == None:
            self.I = y
        elif x == x.father.lchild:
            x.father.lchild = y
        else:
            x.father.rchild = y
        y.lchild = x
        x.father = y

    # 在节点x处右旋
    def func2(self, x):
        y = x.lchild
        x.lchild = y.rchild
        if y.rchild != None:
            y.rchild.father = x
        y.father = x.father
        if x.father == None:
            self.I = y
        elif x == x.father.rchild:
            x.father.rchild = y
        else:
            x.father.lchild = y
        y.rchild = x
        x.father = y

    # 在二叉搜索树上插入一个新节点    
    def func3(self, v1, v2):
        tmp = node(v1, v2)
        root = self.I
        father = None
        while root != None:
            father = root
            if v1 < root.v1:
                root = root.lchild
            else:
                root = root.rchild
        tmp.father = father
        if father == None:
            self.I = tmp
        elif v1 < father.v1:
            father.lchild = tmp
        else:
            father.rchild = tmp
        self.tree(tmp)


# 中序层次遍历整棵树的v2
def func4(tmp):
    s = b""
    if tmp != None:
        s += bytes([random.randint(0, 0xFF)])
        s += func4(tmp.lchild)
        s += func4(tmp.rchild)
    return s


# 随机选择一个叶子节点，把它旋转到根节点
def func5(var1):
    root = var1.I
    father = None
    while root != None:
        father = root
        if random.randint(0, 1) == 0:
            root = root.lchild
        else:
            root = root.rchild
    var1.tree(father)


def main():
    var1 = tree()

    var2 = [0] * 36 # [i for i in range(36)]

    if len(var2) != 36:
        print("Try again!")
        return

    for i in var2:
        var1.func3(random.random(), i)

    for _ in range(0x100):
        func5(var1)

    aaa = func4(var1.I)
    bbb = base64.b64decode("7EclRYPIOsDvLuYKDPLPZi0JbLYB9bQo8CZDlFvwBY07cs6I")
    for i in range(36):
        print(chr(aaa[i] ^ bbb[i]), end=",")
    
if __name__=="__main__":
    main()