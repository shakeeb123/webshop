# import unittest

# # Here's our "unit".
# def IsOdd(n):
#     return n % 2 == 1

# # Here's our "unit tests".
# class IsOddTests(unittest.TestCase):

#     def testOne(self):
#         self.failUnless(IsOdd(1))

#     def testTwo(self):
#         self.failIf(IsOdd(2))

# def main():
#     unittest.main()

# if __name__ == '__main__':
#     main()

import unittest
import datetime

class DatePattern:

    def __init__(self, year, month, day):
        self.date = datetime.date(year, month, day)

    def matches(self, date):
        return True

class FooTests(unittest.TestCase):

    def testMatches(self):
    	p = DatePattern(2004, 9, 28)
    	d = datetime.date(2004, 9, 28)
    	self.failUnless(p.matches(d))

def main():
    unittest.main()

if __name__ == '__main__':
    main()

