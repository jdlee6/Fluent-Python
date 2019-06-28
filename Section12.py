'''
Inheritance: for good or for worse 

Overview (inheritance & subclassing):
    -pitfalls of subclassing from built-in types
    -Multiple inheritance and the method resolution order


Subclassing built in types is tricky
    -major caveat: code of the built-in's does NOT call special methods overriden by user-defined classes
'''
# # example - __setitem__ override is ignored by the __init__ and __update__ methods of the built in dict

# class DoppelDict(dict):
#     def __setitem__(self, key, value):
#         # DoppelDict.__setitem__ duplicates values when storing (for no good reason, just to have a visible effect). It works by delegating to the superclass
#         super().__setitem__(key, [value] * 2)
    
# # the __init__ method inherited from dict clearly ignored that __setitem__ was overridden: the value of 'one' is not duplicated
# dd = DoppelDict(one=1)
# print(dd)
# # {'one': 1}

# # the [] operator calls our __setitem__ and works as expected: 'two' maps to the duplicated value of [2, 2]
# dd['two'] = 2
# print(dd)
# # {'one': 1, 'two': [2, 2]}

# # update method from dict does NOT use our version of __setitem__ either: the value of 'three' was NOT duplicated
# dd.update(three=3)
# print(dd)
# # {'one': 1, 'two': [2, 2], 'three': 3}

'''
*the search for methods should ALWAYS start from the class of the target instance(self), even when the call happens inside a method implemented in a superclass

also happens with overriden methods of other classes that should be called by the built in methods
'''
# # example - the __getitem__ of AnswerDict is bypassed by dict.update
# class AnswerDict(dict):
#     # AnswerDict.__getitem__ always returns 42, no matter what the key
#     def __getitem__(self, key):
#         return 42

# # ad is an AnswerDict loaded with the key-value pair ('a', 'foo')
# ad = AnswerDict(a='foo')
# print(ad['a'])
# # ad['a'] returns 42 as expected
# # 42

# d = {}
# # d is an instance of plain dict, which we update with ad
# d.update(ad)
# # the dict.update method ignored our AnswerDict.__getitem__
# print(d['a'])
# # foo

# print(d)
# # {'a': 'foo'}

'''
if you subclass collections.UserDict instead of dict; the issues in the examples above are fixed
'''

# # example - DoppelDict2 and AnswerDict2 work as expected because they extend UserDict and not dict
# import collections

# class DoppelDict2(collections.UserDict):
#     def __setitem__(self, key, value):
#         super().__setitem__(key, [value]*2)

# dd = DoppelDict2(one=1)
# print(dd)
# # {'one': [1, 1]}

# dd['two'] = 2
# print(dd)
# # {'one': [1, 1], 'two': [2, 2]}

# dd.update(three=3)
# print(dd)
# # {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}

# class AnswerDict2(collections.UserDict):
#     def __getitem__(self, key):
#         return 42

# ad = AnswerDict2(a='foo')
# print(ad['a'])
# # 42

# d = {}
# d.update(ad)
# print(d['a'])
# # 42

# print(d)
# # {'a': 42}


'''
problems arise and only affects user defined classes derived directly from those built-in types within the C language (list, str, int)
if you subclass from a class coded in Python (UserDict; MutableMapping), you will not be troubled by this 


Multiple Inheritance and Method Resolution Order

Need to deal with potential naming conflicts when unrelated ancestor classes implement a method by the same name 
    refered to as the "diamond problem"
'''
# example - take a look at diamond.py
'''
both classes B and C implement a pong method; C.pong outputs the word PONG in uppercase

if you call d.pong() on an instance of D, which pong method will run?
'''

# # example - two ways of invoking method pong on an instance class D
# from Sec12_examples.diamond import *

# d = D()
# # simply calling d.pong() causes the B version to run
# d.pong()
# # pong:  <Sec12_examples.diamond.D object at 0x7fcec858bdd8>

# # You can always call a method on a superclass directly, passing the instance as an explicit argument
# C.pong(d)
# # PONG:  <Sec12_examples.diamond.D object at 0x7fd733f7ddd8>

'''
Python follows a specific order when traversing the inheritance graph - MRO: Method Resolution Order

Classes have an attribute called __mro__ which holds a tuple of references to the superclasses in MRO order, from the current class all the way to the object class

The way to delegate method calls to superclasses is the super() built-in function

When calling an instance method directly on a class; you must pass self explicitly because you are accessing an unbound method
'''

# print(D.__mro__)
# # (<class 'Sec12_examples.diamond.D'>, <class 'Sec12_examples.diamond.B'>, <class 'Sec12_examples.diamond.C'>, <class 'Sec12_examples.diamond.A'>, <class 'object'>)

# example - super() follows the MRO when invoking a method - using super() to call ping

# from Sec12_examples.diamond import D
# d = D()
# # The ping of D makes two calls:
# d.ping()
# # The first call is super().ping(); the super delegates the ping call to class A; A.ping outputs this line below
# # ping:  <Sec12_examples.diamond.D object at 0x7f31ed84bdd8>

# # The second call is print('post-ping: ', self) which outputs this line below
# # post-ping:  <Sec12_examples.diamond.D object at 0x7f31ed84bdd8>

# example - the five calls made by pingpong
# from Sec12_examples.diamond import D

# d = D()
# print(D.__mro__)
# d.pingpong()

# # (<class 'Sec12_examples.diamond.D'>, <class 'Sec12_examples.diamond.B'>, <class 'Sec12_examples.diamond.C'>, <class 'Sec12_examples.diamond.A'>, <class 'object'>)

# # Call #1 is 'self.ping()' runs the ping method of D, which outputs this line and the next one
# # ping:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>
# # post-ping:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>

# # Call #2 is super.ping() which bypasses the ping in D and finds the ping method in A
# # A is the only class with the ping method; B and C have pong methods
# # ping:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>

# # Call #3 is self.pong() which finds the B implementation of pong according to the __mro__
# # pong:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>

# # Call #4 is super.pong() which finds the same B.pong implementation, also following the __mro__
# # pong:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>

# # Call #5 is C.pong(self) which finds the C.pong implementation, ignoring the __mro__
# # PONG:  <Sec12_examples.diamond.D object at 0x7f094f7dfdd8>

'''
note: if D class was declared as class D(C, B):, the __mro__ of class D would be different: C would be searched before B
'''

# example - inspecting the __mro__ attribute in several classes

# bool inherits methods and attributes from int and object
# print(bool.__mro__)
# # (<class 'bool'>, <class 'int'>, <class 'object'>)

# print_mro produces more compact displays of the MRO
def print_mro(cls):
    print(', '.join(c.__name__ for c in cls.__mro__))

# print_mro(bool)
# # bool, int, object

# from Sec11_examples.frenchdeck2 import FrenchDeck2
# # ancestors of FrenchDeck2 include several ABCs from the collections.abc module
# print_mro(FrenchDeck2)
# # FrenchDeck2, MutableSequence, Sequence, Reversible, Collection, Sized, Iterable, Container, object

# import numbers
# # These are the numeric ABCs provided by the numbers module
# print_mro(numbers.Integral)
# # Integral, Rational, Real, Complex, Number, object

# import io
# # the io module includes ABCs (those with the ...Base suffix) and concrete classes like BytesIO and TextIOWrapper which are the types of binary and text file objects returned by open(), depending oon the mode argument
# print_mro(io.BytesIO)
# # BytesIO, _BufferedIOBase, _IOBase, object

# print_mro(io.TextIOWrapper)
# # TextIOWrapper, _TextIOBase, _IOBase, object


# example - part of the complex multiple inheritance graph of the tkinter gui toolkit
# Text class implements full featured, multi-line editable text widget; rich functionality on its own but also inherits many methods from other classes
# take a look at the diagram on page 383

# import tkinter
# print_mro(tkinter.Text)
# # Text, Widget, BaseWidget, Misc, Pack, Place, Grid, XView, YView, object


'''
Multiple Inheritance in the real world

most visibile use of multiple inheritance is the collections.abc package

extreme example of multiple inheritance in the standard library is the Tkinter GUI toolskit
    figure on pg 384 shows all of it

classes:
    1. Toplevel: the class of a top-level window in a Tkinter application
    2. Widget: the superclass of every visible object that can be placed on a window
    3. Button: A plain button widget
    4. Entry: A single line editable text field
    5. Text: A multiline editable text field


Things to note from the example below:
    Toplevel is the only graphical class that does NOT inherit from Widget, because it is the top-level window and does not behave like a widget
        inherits from Wm, which provideds direct access functions of the host window manager like setting the window title and configuring its borders
    
    Widget inherits directly from BaseWidget and from Pack, Place, and Grid. These last three classes are geometry managers: they are responsible for arranging widgets inside a window or frame. Each encapsulates a different layout strategy and widget placement API

    Button, like most widgets, descend only from Widget, but indirectly from Misc, which provides dozens of methods to every widget

    Entry subclasses Widget and XView, the class that implements horizontal scrolling

    Text subclasses from Widget, XView and YView which provides vertical scrolling functionality
'''

# # example - MROs of those classes - displayed by the print_mro function from above
# import tkinter
# print_mro(tkinter.Toplevel)
# # Toplevel, BaseWidget, Misc, Wm, object

# print_mro(tkinter.Widget)
# # Widget, BaseWidget, Misc, Pack, Place, Grid, object

# print_mro(tkinter.Button)
# # Button, Widget, BaseWidget, Misc, Pack, Place, Grid, object

# print_mro(tkinter.Entry)
# # Entry, Widget, BaseWidget, Misc, Pack, Place, Grid, XView, object

# print_mro(tkinter.Text)
# # Text, Widget, BaseWidget, Misc, Pack, Place, Grid, XView, YView, object


'''
Coping with multiple inheritance

*Mixins are a sort of class that is used to "mix in" extra properties and methods into a class
    1. want to provide a lot of optional features
    2. want to use one particular feature in a lot of different classes

Tips to avoid a mess with multiple inheritance:
    1. Distinguish interface inheritance from implementation inheritance
        i. Inheritance of interface (description of how the object behaves): creates a sub type, implying an "is-a" relationship
            -backbone of a framework
        ii. Inheritance of implementation: avoids code duplication by reuse
            -implementation detail

    2. Make interfaces explicit with ABCs
        i. if a class is designed to define an interface, it should be an explicit ABC
            -this means subclass abc.ABC or another ABC

    3. Use mixins for code reuse
        i. if a class is designed to provide method implementations for reuse by multiple UNRELATED subclasses, without implying an "is-a" relationship, it should be an explicit MIXIN class
            -mixin does NOT define a new type - bundles methods for reuse; mixin should NEVER be instantiated; concrete classes should NOT inherit only from a mix
            -Each mixin should provide a single specific behavior, implementing few and very close related methods

    4. Make mixins explicit by naming
        i. There is no formal way in Python to state that a class is a mixin, so it is highly recommended that they are named with ...Mixin suffix. 
            *Tkinter does NOT follow this; ie. XView is not XViewMixin

    5. An ABC may also be a mixin; the reverse is NOT true
        i. Since an ABC can implement concrete methods, it works as a mixin as well. An ABC defines a type, which a mixin does NOT; an ABC can be sole base class of any other class, while a mixin should NEVER be subclassed alone except by another, more specialized mixin
        **Concrete methods implemented in an ABC should ONLY collaborate with methods of the same ABC and its superclasses

    6. Don't subclass from more than one concrete class
        i. Concrete classes should have zero or at most one concrete superclass. All but one of the superclasses of a concrete class should be ABCs or mixins. 
            if Alpha is a concrete class, then Beta and Gamma must be ABCs or mixins
            ie. class MyConcreteClass(Alpha, Beta, Gamma):
                    # this is a concrete class: it can instantiated #

    7. Provide aggregate classes to users
        i. If some combination of ABCs and mixins is particularly useful to client code, provide a class that brings them together in a sensible way. This is referred to as an aggregate class.

            ie. class Widget(BaseWidget, Pack, Place, Grid):
                    # Internal class
                    # Base class for a widget which can be positioned with the geometry managers Pack, Place, or Grid
                    pass

                a. body is empty but the class brings together FOUR superclasses so that anyone who needs to create a new widget does not need to remember all of those mixins, or wonder if they need to be declared in a certain order in a class statement

    8. "Favor object composition over class inheritance"
        i. Favoring composition leads to more flexible designs. 
        Composition and delegation can replace the use of mixins to make behaviors available to different classes, but CANNOT replace the use of interface inheritance to define a hierarchy of types


Tkinter: the good, the bad, and the ugly
    *Tkinter is an exception because it existed since Python 1.1 so it doesn't follow the rules above (except #7)
    ie. Misc has more than 100 methods and ALL widgets inherit from it
        *not necessary -> it SHOULD be split into several specialized Mixin classes and not all widgets should inherit from every one of those mixins
        **headache b/c dir(tkinter.Button) will return 200+ attributes listed


A modern example: mixins in Django generic views
*Don't need to know Django - just a couple snippets of the framework*
http://ccbv.co.uk/

list view: renders search results
detail view: produces pages for individual items

Look at the figure on page 391:
    View is the base class of all views (could be an ABC); RedirectView class inherits ONLY from View

    Subclasses are free to implement just handlers they want to support; 
    a TemplateView is used only to display content so it only implements GET
        -if a POST request is sent; the inherited View.dispatch method checks there is no POST handler and sends a 405 error message
    
    TemplateResponseMixin provides functionality that is of interest only to views that need to use a template
        provides behaviors to TemplateView and other template-rendering views
        ie. RedirectView has NO content body so it doesn't need a template and does NOT inherit from a mixin

    ListView is an aggregate class (no code at all; just a docstring in the body)
        when instantiated, a ListView has an object_list instance attribute which the template can iterate to show the page contents (usually a database query returning multiple objects)
        *MultipleObjectMixin - provides pagination logic to display results on page and links to more pages

    BaseListView is for producing a list of objects in JSON format instead of rendering a template - easy to use extension point that brings together View and MultipleObjectMixin 

    Better than Tkinter in terms of multiple inheritance because it is EASY to make sense of its mixin classes: well defined purpose along with the Mixin suffix
'''
