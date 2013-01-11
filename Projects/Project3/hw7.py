"""61A Homework 7
Name:
Login:
TA:
Section:
"""
from functools import reduce
from ucb import trace
# Q1.

class Square(object):
    def __init__(self, side):
        self.side = side

class Rect(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

def type_tag(s):
    return type_tag.tags[type(s)] #the ,tag is an attribute since
                    #everything is an object and can have attributes

type_tag.tags = {Square: 's', Rect: 'r'}

def apply(operator_name, shape):
    """Apply operator to shape.

    >>> apply('area', Square(10))
    100
    >>> apply('perimeter', Square(5))
    20
    >>> apply('area', Rect(5, 10))
    50
    >>> apply('perimeter', Rect(2, 4))
    12
    """
    "*** YOUR CODE HERE ***"
    types = (type_tag(shape))
    key = (operator_name, types)
    return apply.implementations[key](shape)

def area_square(x):
    return x.side * x.side
def area_rect(x):
    return x.length * x.width
def per_square(x):
    return 4 * x.side
def per_rect(x):
    return 2 * x.length + 2 * x.width
    
apply.implementations = {}
apply.implementations[('area', 's')] = area_square
apply.implementations[('area', 'r')] = area_rect
apply.implementations[('perimeter', 's')] = per_square
apply.implementations[('perimeter', 'r')] = per_rect

# Q2.

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    """
    "*** YOUR CODE HERE ***"
    if n <=3 :
        return n
    return g(n-1) + 2*g(n-2) + 3*g(n-3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.
    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    """
    "*** YOUR CODE HERE ***"
    iter_list = []
    i = 0
    #while i <= n:
    if n <= 3: #increment works better if you have to calculate things beforehand
        return n
        #i+=1
    while i < n-3:
        iter_list[i%3] = iter_list[(i+2)%3] + 2*iter_list[(i+1)%3] + 3*iter_list[i%3]
        i+=1
    return iter_list[(i-1)%3]

    """while n:
        pred, other_pred, curr, current = other_pred, curr, , pred + 2*other_pred + 3*curr"""
    """n > 0:
        if n-1 > 3 and n-2 > 3 and n-3 > 3:
            pred = n-1
            other_pred = n-2
            curr = n-3
            stuff = pred + 2*other_pred + 3*curr
        elif 
        else:
            pred = n
            other_pred = n
            curr = n
            stuff = stuff + pred + 2*other_pred + 3*curr
        n-=1
    return stuff"""
    

# Q3.

def part(n):
    """Return the number of partitions of positive integer n.

    >>> part(5)
    7
    >>> part(10)
    42
    >>> part(15)
    176
    >>> part(20)
    627
    """
    "*** YOUR CODE HERE ***"
    #k=[]
    """for i in range(1, n+1):
        k.append(i)"""
    @trace
    def subset(n, k):
        if n == k:
            return 1
        if n < k: #you want to find how many ways satisfy this
            return 0
        #d = list_x[0]
        return subset(n-k, k) + subset(n, k+1)
    return subset(n, 1)

"""Consider the base cases:
    if you have a minimum, like 5
    you can have any number >= 1
    if n < min, there's no way to partition it
    then if it's the same as min, then you return 1
    But now how many ways are ther eto partition this n, with like, 5 atleast 2
        it's the number of ways to partition 4 with at least the same min, or
        how to partition 5 with at least 3 and so on and so forth"""
            
        

"""if n == 1:
    return 1
#if len(subset(n)) == 0:
 #   return 1
else:
   return part(subset(n)) + part(subset(n-1))"""

# Q4.

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    """
    return YOUR_EXPRESSION_HERE

# Q5.

def has_cycle(s):
    """Return whether Rlist s contains a cycle.

    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle(s)
    True
    >>> t = Rlist(1, Rlist(2, Rlist(3)))
    >>> has_cycle(t)
    False
    """
    "*** YOUR CODE HERE ***"

def has_cycle_constant(s):
    """Return whether Rlist s contains a cycle.

    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> s.rest.rest.rest = s
    >>> has_cycle_constant(s)
    True
    >>> t = Rlist(1, Rlist(2, Rlist(3)))
    >>> has_cycle_constant(t)
    False
    """
    "*** YOUR CODE HERE ***"

class Rlist(object):
    """A recursive list consisting of a first element and the rest."""
    class EmptyList(object):
        def __len__(self):
            return 0

    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        args = repr(self.first)
        if self.rest is not Rlist.empty:
            args += ', {0}'.format(repr(self.rest))
        return 'Rlist({0})'.format(args)

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i-1]
