class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          
class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        if self.top == None:
            return True
        return False

    def __len__(self): 
        current = self.top
        count = 0
        while current:
            count+=1
            current = current.next
        return count


    def push(self,value):
        nn = Node(value)
        nn.next = self.top
        self.top = nn
     
    def pop(self):
        if self.top:
            tmp = self.top
            self.top = tmp.next
            return tmp.value

    def peek(self):
        return self.top.value

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        try:
            float(txt)
            return True
        except:
            return False

    def _getPostfix(self, txt):
        '''

            >>> x=Calculator()
            >>> x._getPostfix('2 ^ 4')
            '2.0 4.0 ^'
            >>> x._getPostfix('2')
            '2.0'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2 * 5.34 + 3 ^ 2 + 1 + 4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( 2.5 )')
            '2.5'
            >>> x._getPostfix('( 2 { 5.0 } )')
            '2.0 5.0 *'
            >>> x._getPostfix(' 5 ( 2 + { 5 + 3.5 } )')
            '5.0 2.0 5.0 3.5 + + *'
            >>> x._getPostfix ('( { 2 } )')
            '2.0'
            >>> x._getPostfix ('2 * ( [ 5 + -3 ] ^ 2 + { 1 + 4 } )')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('[ 2 * ( < 5 + 3 > ^ 2 + ( 1 + 4 ) ) ]')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('( { 2 * { { 5 + 3 } ^ 2 + ( 1 + 4 ) } } )')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2 * < -5 + 3 > ^ 2 + < 1 + 4 >')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # Invalid expressions

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('2 * 5 + 3 ^ - 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ( 1 + 4 ]')
            >>> x._getPostfix(' ( 2 * { 5 + 3 ) ^ 2 + ( 1 + 4 ] }')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^ 2 + ) 1 + 4 (')
            >>> x._getPostfix('2 * 5% + 3 ^ + -2 + 1 + 4')
        '''

        postfixStack = Stack()
        postfixlst = []
        operators = {'+': 4,'-': 4,'*': 3,'/': 3, '^': 2, '(': 1.1,')': 5.1,'[': 1.2,']': 5.2,'{': 1.3,'}': 5.3, '<': 1.4,'>': 5.4}
        tokens = txt.split()

        for token in tokens:
            if tokens.index(token) == 0:
                if self._isNumber(token):
                    postfixlst.append(float(token))
                    current = float(token)
                elif token in operators:
                    postfixStack.push(token)
                    if operators[token] > 5:
                        return None  

            else:
                if self._isNumber(token) == False and token not in operators:
                    return None
                elif current in operators and token in operators:
                    if operators[current] >=2 and operators[current] < 5 and operators[token] >= 2 and operators[token] < 5:
                        return None
                elif self._isNumber(current) and self._isNumber(token):
                    return None

                if token in operators:
                    if postfixStack.isEmpty():
                        if operators[token] <2 and self._isNumber(current):
                            postfixStack.push('*')
                        elif operators[token] <2 and operators[current] >5:
                            postfixStack.push('*')
                        elif operators[token] > 1 and operators[token] < 5:
                            if tokens.index(token) == (len(tokens)-1):
                                return None
                        postfixStack.push(token)

                    elif operators[token] < 2:
                        if self._isNumber(current) or operators[current] > 5: 
                            postfixStack.push('*')
                        postfixStack.push(token)
                    elif operators[token] > 1 and operators[token] < 5:
                        if tokens.index(token) == (len(tokens)-1):
                            return None
                        out = False
                        while out == False:
                            if operators[postfixStack.peek()] == 2 and operators[token] == 2: 
                                out = True  
                                postfixStack.push(token)   
                            elif operators[postfixStack.peek()] <= operators[token] and operators[postfixStack.peek()] >= 2:  
                                top_value = postfixStack.pop()
                                postfixlst.append(top_value)
                                if postfixStack.isEmpty():
                                    out = True
                                    postfixStack.push(token)
                            else:
                                out = True
                                postfixStack.push(token)
                        
                    elif operators[token] > 5:
                        out = False
                        while out == False:
                            if operators[postfixStack.peek()] >= 2:
                                top_value = postfixStack.pop()
                                postfixlst.append(top_value)
                                if postfixStack.isEmpty():
                                    out = True
                            else:
                                out = True
                        if postfixStack.isEmpty():
                            return None
                        top_value = postfixStack.pop()
                        if operators[top_value] != round((operators[token])-4.0, 2):
                            return None
                elif self._isNumber(token):
                    postfixlst.append(float(token))
                
            current = token
                    
        while len(postfixStack) > 0:
            top_value = postfixStack.pop()
            if operators[top_value] <2:
                return None
            postfixlst.append(top_value)
                    
        postfix = []
        for item in postfixlst:
            postfix.append(str(item))
        postfix = ' '.join(postfix)

        return postfix

    @property
    def calculate(self):
        '''

            >>> x=Calculator()
            >>> x.setExpr('4 + 3 - 2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 + 3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('4 + 3.65 - 2 / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25 * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr(' 2 - 3 * 4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7 ^ 2 ^ 3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ( [ ( 10 - 2 * 3 ) ] )')
            >>> x.calculate
            12.0
            >>> x.setExpr('8 / 4 * { 3 - 2.45 * [ 4 - 2 ^ 3 ] } + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * [ 4 + 2 * < 5 - 3 ^ 2 > + 1 ] + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 + 3 * ( 2 + { 3.0 } * ( 5 ^ 2 - 2 * 3 ^ ( 2 ) ) * < 4 > ) * [ 2 / 8 + 2 * ( 3 - 1 / 3 ) ] - 2 / 3 ^ 2')
            >>> x.calculate
            1442.7777777777778
            >>> x.setExpr('( 3.5 ) [ 15 ]') 
            >>> x.calculate
            52.5
            >>> x.setExpr('3 { 5 } - 15 + 85 [ 12 ]') 
            >>> x.calculate
            1020.0
            >>> x.setExpr("( -2 / 6 ) + ( 5 { ( 9.4 ) } )") 
            >>> x.calculate
            46.666666666666664
            

            # Invalid expressions
            >>> x.setExpr(" 4 + + 3 + 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 + 2")
            >>> x.calculate
            >>> x.setExpr('( ( 2 ) * 10 - 3 * [ 2 - 3 * 2 ) ]')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * ( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( * 10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()
        operators = {'+': 1, '-': 2, '*': 3, '/': 4, '^': 5}
        op1 = self.getExpr
        operation = self._getPostfix(op1)
        if operation == None:
            return
        operation = operation.split()

        for item in operation:
            if self._isNumber(item):
                calcStack.push(float(item))
            else:
                num1 = calcStack.pop()
                num2 = calcStack.pop()
                if operators[item] == 1:    
                    res = num2 + num1
                elif operators[item] == 2: 
                    res = num2 - num1
                elif operators[item] == 3:
                    res = num2 * num1
                elif operators[item] == 4:
                    res = num2 / num1
                elif operators[item] == 5:
                    res = num2 ** num1
                calcStack.push(res)
        return res

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 [ x1 - 1 ];x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 [ x1 - 1 ]': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * { x1 / 2 };x1 = x2 * 7 / x1;return x1 ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * { x1 / 2 }': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        for char in word:
            if char.isalnum() == False:
                return False
        if word[0].isalpha() == False:
            return False
        return True 

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 ( x1 - 1 )')
            '7 ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        operators = {'+': 4,'-': 4,'*': 3,'/': 3, '^': 2, '(': 1.1,')': 5.1,'[': 1.2,']': 5.2,'{': 1.3,'}': 5.3, '<': 1.4,'>': 5.4}
        tokens = expr.split()
        for i in range(len(tokens)):
            if self._isVariable(tokens[i]) == False and tokens[i] not in operators and Calculator._isNumber(self, tokens[i]) == False:
                return None
            elif self._isVariable(tokens[i]) and tokens[i] not in self.states:
                return None
            elif self._isVariable(tokens[i]) and tokens[i] in self.states:
                tokens[i] = str(self.states[tokens[i]])
        return ' '.join(tokens)
    
    def calculateExpressions(self):
        operators = {'+': 4,'-': 4,'*': 3,'/': 3, '^': 2, '(': 1.1,')': 5.1,'[': 1.2,']': 5.2,'{': 1.3,'}': 5.3, '<': 1.4,'>': 5.4}
        self.states = {} 
        calcObj = Calculator()
        finaldict = {}
        expressions1 = self.expressions.split(';') 

        for exp in expressions1:
            newexp = exp.split()
            if newexp[0] == 'return':
                repright = self._replaceVariables(exp[7:])
                is_state = True
                for item in repright:
                    if item in operators:
                        is_state = False
                if is_state == False:
                    calcObj.setExpr(str(repright))
                    repright = calcObj.calculate
                
                finaldict['_return_'] = float(repright)

            elif self._isVariable(newexp[0])== False:
                self.states = {}
                finaldict = {}
                return None
            else:
                eqindex = exp.index('=')
                repright = self._replaceVariables(exp[eqindex+1:])
                is_state = True
                for item in repright:
                    if item in operators:
                        is_state = False
                if is_state == False:
                    calcObj.setExpr(str(repright))
                    repright = calcObj.calculate
                self.states[newexp[0]] = float(repright)
                dict_copy = self.states.copy()
                finaldict[exp] = dict_copy

        return finaldict


def run_tests():
    import doctest

    #- Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    #- Run tests per class - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    #doctest.run_docstring_examples(AdvancedCalculator, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    run_tests()