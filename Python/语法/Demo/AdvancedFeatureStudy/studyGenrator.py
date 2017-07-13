#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class StudyYeld(object):
    def thriangles(self,n):
        t = (1,)
        left = 0
        i = 0
        while 1 < n:
            yield t
            temp = []  # 注意这里清空，否则会无限循环，造成内存泄漏
            for i in t:
                temp.append(i + left)
                left = i
            t = (temp)
            temp.append(1)
            left = 0
            i = i + 1
        return

    # 测试
    def testYield(self):
        n = 0
        for t in self.thriangles(10):
            print(t)
            n = n + 1
            if n == 10:
                break

    #迭代器与list
    def testListOrGenerator(self):
        l = [x * x for x in range(10)]
        print(l)
        L = (x * x for x in range(10))
        for i in L:
            print(i)




class StudyYeldFrom(object):
    def inner(self):
        coef = 1
        total = 0
        while True:
            print('---------yield前')
            # 1.yield 语句执行时，yield暂停，input_val没有赋值
            # 2.当send()调用时，yield 从send()的参数得到值 赋值给input_val
            input_val = yield total     #yield表达式可以接收send()发出的参数   http://blog.csdn.net/u014683535/article/details/51757747
            print('---------yield后,input_val:%s' % input_val)
            total = total + coef * input_val
            input_val  = 1 + input_val

    def testInner(self):
        s = StudyYeldFrom()
        f = s.inner()
        f.send(None) #send(None),将生成器至于yield，只有生成器时暂停状态，才能接受send的值
        for i in range(5):
            print(f.send(i))

    def outer(self):
        yield from self.inner()

    def testOuter(self):
        f = self.outer()
        f.send(None)
        for i in range(5):
            print(f.send(i))

def test1():
    c = StudyYeld()
    c.testYield()

def test2():
    c = StudyYeldFrom();
    c.testOuter()



if __name__ == '__main__':
    # test1()
    test2()















