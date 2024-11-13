import copy


class EmptyStackException(Exception):
    pass


class ExpressionSyntaxError(Exception):
    pass


class MissingVariableException(Exception):
    pass


class VariableTypeException(Exception):
    pass


class NotBooleanException(Exception):
    pass


class Stack:

    def __init__(self):
        self.data = []

    def push(self, x):
        self.data.append(x)

    def pop(self):
        if self.data == []:
            raise EmptyStackException
        res = self.data[-1]
        self.data = self.data[0:-1]
        return res

    def __str__(self):
        return " ".join([str(s) for s in self.data])


class Expression:

    def __init__(self):
        self.exprStack = Stack()

    #from_program: prende come input una lista di stringhe (generato con split()) e il dict con le operazioni disponibili,
    #              genera una variabile di tipo Expression() che contiene un solo elemento nello stack.
    #              La funzione controlla se l'elemento della lista "text" è un operatore, una costante o una variabile:
    #                   - Se operatore: crea un oggetto del tipo dell'operatore trovato, fa il pop dello stack attuale e 
    #                     assegna i suoi argomenti, finisce facendo il push nello stack dell'operatore
    #                   - Se numero: crea un oggetto Constant e fa il push nello stack
    #                   - Se stringa di caratteri: crea un oggetto Variable e fa il push nello stack
    #              Se dopo questa serie di operazioni lo stack non ha un solo elemento, suppongo che l'espressione
    #              sia stata scritta in maniera errata
    @classmethod
    def from_program(cls, text, dispatch):
        expr = Expression()
        for item in text:
            if item in dispatch :
                args = []
                classType = dispatch[item]
                for k in range(0,dispatch[item].arity()):
                    args.append(expr.exprStack.pop())
                expr.exprStack.push(classType(args))
            elif item.isdigit():
                expr.exprStack.push(Constant(int(item)))
            else:
                expr.exprStack.push(Variable(item))
        if len(expr.exprStack.data) != 1:
            raise ExpressionSyntaxError
        return expr

    def evaluate(self, env):
        return self.exprStack.data[0].evaluate(env)
    
    def __str__(self):
        return str(self.exprStack.data[0])
        

class Variable(Expression):

    def __init__(self, name):
        self.name = name

    #evaluate: ritorna il valore associato alla variabile usando una oggetto di tipo Constant
    def evaluate(self, env):
        if(self.name in env):
            return Constant(env[self.name])
        else:
            raise MissingVariableException

    def __str__(self):
        return self.name


class Constant(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        return f"{self.value}"


class Operation(Expression):

    def __init__(self, args):
        self.args = args

    def evaluate(self, env):
        pass

    def op(self, *args):
        pass

#    evaluateArgs: funzione che serve per impostare tutti gli args di un Operation ad un oggetto di tipo Constant o Boolean.
#                  Utile nel momento in cui voglio andare a fare dei calcoli o confronti sugli argomenti, così sono sicuro di non avere
#                  altre operazioni intermedie da valutare
    def evaluateArgs(self, env):
        for k in range(0,len(self.args)):
            if(not isinstance(self.args[k],Constant)):
                self.args[k] = self.args[k].evaluate(env)

    def __str__(self):
        pass


class Boolean(Expression):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

    def __str__(self):
        if(self.value):
            return "True"
        return "False"


class NoOp(Operation):

    def arity():
        return 0

    def __str__(self, op):
        return f"({op})"


class UnaryOp(Operation):

    def arity():
        return 1

    def __str__(self, op):
        return f"({op} {str(self.args[0])})"


class BinaryOp(Operation):

    def arity():
        return 2

    def __str__(self, op):
        return f"({op} {str(self.args[0])} {str(self.args[1])})"


class TernaryOp(Operation):
    
    def arity():
        return 3

    def __str__(self, op):
        return f"({op} {str(self.args[0])} {str(self.args[1])} {str(self.args[2])})" 
    

class QuaternaryOp(Operation):
    
    def arity():
        return 4

    def __str__(self, op):
        return f"({op} {str(self.args[0])} {str(self.args[1])} {str(self.args[2])} {str(self.args[3])})" 


class Addition(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() + self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("+")


class Subtraction(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() - self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("-")


class Division(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() / self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("/")


class Multiplication(BinaryOp):
        
    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() * self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("*")


class Power(BinaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() ** self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("**")


class Modulus(BinaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(self.args[0].evaluate() % self.args[1].evaluate())
    
    def __str__(self):
        return super().__str__("%")


class Reciprocal(UnaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(1/self.args[0].evaluate())
    
    def __str__(self):
        return super().__str__("1/")


class AbsoluteValue(UnaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        return Constant(abs(self.args[0].evaluate()))
    
    def __str__(self):
        return super().__str__("abs")


class IsEqual(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 == res2)
    
    def __str__(self):
        return super().__str__("=")


class NotEqual(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 != res2)
    
    def __str__(self):
        return super().__str__("!=")


class GreaterThan(BinaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 > res2)
    
    def __str__(self):
        return super().__str__(">")


class GreaterEqual(BinaryOp):
    
    def evaluate(self, env):
        self.evaluateArgs(env)
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 >= res2)
    
    def __str__(self):
        return super().__str__(">=")


class LesserThan(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)              
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 < res2)
    
    def __str__(self):
        return super().__str__("<")


class LesserEqual(BinaryOp):

    def evaluate(self, env):
        self.evaluateArgs(env)
        res1 = self.args[0].evaluate()
        res2 = self.args[1].evaluate()
        return Boolean(res1 <= res2)
    
    def __str__(self):
        return super().__str__("<=")


class Allocate(UnaryOp):
    
    def evaluate(self, env):
        if(not isinstance(self.args[0],Variable)):
            raise VariableTypeException
        env[str(self.args[0])] = 0

    def __str__(self):
        return super().__str__("alloc")


class VectorAllocate(BinaryOp):
    
    def evaluate(self, env):
        if(not isinstance(self.args[0],Variable)):
            raise VariableTypeException
        env[str(self.args[0])] = [0] * self.args[1].evaluate()

    def __str__(self):
        return super().__str__("valloc")


class SetVariable(BinaryOp):

    #evaluate: salvo il nome della variabile in questione, calcolo gli argomenti (guarda Operation.evaluateArgs)
    #          e controllo se il nome della variabile si trova in env; se si, imposto il nuovo valore, altrimenti Excpetion
    def evaluate(self, env):
        name = str(self.args[0])
        self.evaluateArgs(env)

        if(name in env):
            env[name] = self.args[1].evaluate()
        else:
            raise MissingVariableException

    def __str__(self):
        return super().__str__("setq")


class SetVectorVariable(TernaryOp):

    #evaluate: salvo il nome della variabile in questione, calcolo gli argomenti (guarda Operation.evaluateArgs) e salvo l'index specificato
    #          e controllo se il nome della variabile si trova in env; se si, imposto il nuovo valore all'index specificato, altrimenti Excpetion
    def evaluate(self, env):
        name = str(self.args[0])
        self.evaluateArgs(env)
        index = self.args[1].evaluate()

        if(name in env):
            env[name][index] = self.args[2].evaluate() 
        else:
            raise MissingVariableException
    
    def __str__(self):
        return super().__str__("setv")


class Prog2(BinaryOp):
    
    def evaluate(self, env):
        self.args[0].evaluate(env)
        return self.args[1].evaluate(env)
    
    def __str__(self):
        return super().__str__("prog2")


class Prog3(TernaryOp):
    
    def evaluate(self, env):
        for item in self.args[:2]:
            item.evaluate(env)
        return self.args[2].evaluate(env)
    
    def __str__(self):
        return super().__str__("prog3")


class Prog4(QuaternaryOp):

    def evaluate(self, env):
        for item in self.args[:3]:
            item.evaluate(env)
        return self.args[3].evaluate(env)
    
    def __str__(self):
        return super().__str__("prog4")


class Condition(TernaryOp):

    #evaluate: la funzione controlla se c'è una condizione da calcolare, altrimenti Exception;
    #          cond quindi contiene un Boolean, che uso per scegliere se valutare if-yes oppure if-no 
    def evaluate(self, env):
        if(isinstance(self.args[0],Boolean)):
            raise NotBooleanException
        cond = self.args[0].evaluate(env)
        if(cond.evaluate()):
            return self.args[1].evaluate(env)
        else:
            return self.args[2].evaluate(env)
    
    def __str__(self):
        return super().__str__("if")


class While(BinaryOp):

    #evalutate: la funzione usa deepcopy per creare una copia dell'operazione da eseguire e
    #           la esegue finche la condizione non diventa falsa
    def evaluate(self, env):
        cond = copy.deepcopy(self.args[0]).evaluate(env)
        while(cond.evaluate()):
            copy.deepcopy(self.args[1]).evaluate(env)
            cond = copy.deepcopy(self.args[0]).evaluate(env)

    def __str__(self):
        return super().__str__("while")
    

class For(QuaternaryOp):

    #evaluate: la funzione salva nome della variabile, valuta start e end nel caso in cui non siano già delle costanti e salva expr;
    #          controlla che la variabile inserita è o non è presente in env e imposta il suo valore a quello di start;
    #          crea un operazione incremento, quindi var = var + 1 e come condizione imposto var < end.
    #          la funzione usa deepcopy per creare una copia dell'operazione da eseguire, dell'incremento e condizione, e
    #          la esegue finche la condizione non diventa falsa
    def evaluate(self, env):
        var = self.args[0]

        #Se ci sono delle espressioni, valutale
        if(not isinstance(self.args[1], Constant)):
            self.args[1] = self.args[1].evaluate(env)
        elif(not isinstance(self.args[2], Constant)):
            self.args[2] = self.args[2].evaluate(env)

        start = self.args[1].evaluate()
        end = self.args[2].evaluate()
        expr = self.args[3]
        if(var not in env):
            Allocate([var]).evaluate(env)
        SetVariable([var, Constant(start)]).evaluate(env)
        increment = SetVariable([var,Addition([var,Constant(1)])])
        cond = LesserThan([var, Constant(end)])

        while(copy.deepcopy(cond).evaluate(env).evaluate()):
            copy.deepcopy(expr).evaluate(env)
            copy.deepcopy(increment).evaluate(env)

    def __str__(self):
        return super().__str__("for")


class DefineSubroutine(BinaryOp):
    
    def evaluate(self, env):
        if(not isinstance(self.args[0],Variable)):
            raise VariableTypeException
        env[str(self.args[0])] = self.args[1]

    def __str__(self):
        return super().__str__("defsub")


class CallSubroutine(UnaryOp):

    def evaluate(self, env):
        name = str(self.args[0])
        if(name in env):
            copy.deepcopy(env[name]).evaluate(env)
        else:
            raise MissingVariableException

    def __str__(self):
        return super().__str__("call")


class Print(UnaryOp):

    def evaluate(self, env):
        print(self.args[0].evaluate(env))

    def __str__(self):
        return super().__str__("print")


class NoOperation(NoOp):

    def evaluate(self, env):
        pass

    def __str__(self):
        return super().__str__("nop")


def processExpression(expr):
    return Expression.from_program(expr.split(), env)


def runProfTest():
    example = "2 3 + x * 6 5 - / abs 2 ** y 1/ + 1/"
    e = Expression.from_program(example.split(), env)
    print(e)
    res = e.evaluate({"x": 3, "y": 7})
    print(res)
    # Ouput atteso:
    # (1/ (+ (1/ y) (** 2 (abs (/ (- 5 6) (* x (+ 3 2)))))))
    # 0.84022932953024


def runProf1Test():
    e = "x 1 + x setq x 10 > while x alloc prog2"
    expr = processExpression(e)
    expr.evaluate({})
    print(f"{expr}")


def runProf2Test():
    e = "v print i i * i v setv prog2 10 0 i for 10 v valloc prog2"
    expr = processExpression(e)
    expr.evaluate({})
    print(f"{expr}")


def runProf3Test():
    e = "x print f call x alloc x 4 + x setq f defsub prog4"
    expr = processExpression(e)
    expr.evaluate({})
    print(f"{expr}")


def runProf4Test():
    e = "nop i print i x % 0 = if 1000 2 i for 783 x setq x alloc prog3"
    expr = processExpression(e)
    expr.evaluate({})
    print(f"{expr}")


def runProf5Test():
    e = "nop x print prime if nop 0 0 != prime setq i x % 0 = if 1 x - 2 i for 0 0 = prime setq prime alloc prog4 100 2 x for"
    expr = processExpression(e)
    expr.evaluate({})
    print(f"{expr}")

#Inizio __main__
env = {"+": Addition, "*": Multiplication, "**": Power, "-": Subtraction,
    "/": Division, "1/": Reciprocal, "abs": AbsoluteValue, "%": Modulus,
    "=": IsEqual, "!=": NotEqual, ">": GreaterThan, ">=": GreaterEqual, "<": LesserThan, "<=": LesserEqual,
    "alloc": Allocate, "valloc": VectorAllocate, "setq": SetVariable, "setv": SetVectorVariable,
    "prog2": Prog2, "prog3": Prog3, "prog4": Prog4,
    "if": Condition, "while": While, "for": For, "defsub": DefineSubroutine, "call": CallSubroutine,
    "print": Print, "nop": NoOperation}


runProfTest()
runProf1Test()
runProf2Test()
runProf3Test()
runProf4Test()
runProf5Test()
