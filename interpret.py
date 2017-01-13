__author__ = 'JohnSpinelli'
#####################################################################
#
# CAS CS 320, Fall 2015
# Assignment 4 (skeleton code)
# interpret.py
#

exec(open('parse.py').read())


Node = dict
Leaf = str


def subst(s, a):
    if not s is None:
        replacement = list(s.keys())
        if type(a) == Node:
            for label in a:
                children = a[label]
                if label == "Variable":
                    for x in replacement:
                        if x == children[0]:
                            sub = s[x]
                            return sub

                else:
                    lenAbs = len(children)
                    f = label
                    sub1 = subst(s,children[0])
                    if lenAbs == 1 and sub1 is not None:
                        a = ({f: [sub1]})
                        return a
                    elif lenAbs > 1 and sub1 is not None:
                        sub2 = subst(s,children[1])
                        a = ({f: [sub1,sub2]})
                        return a
                    elif lenAbs > 1 and sub1 is None:
                        sub2 = subst(s,children[1])
                        if sub2 is not None:
                            a = ({f: [children[0],sub2]})
                        else:
                            a = ({f: [children[0],children[1]]})
                        return a

def testUnify(x, y):
    if type(x) == dict and type(y) == dict: # Testing abstract syntax trees.
        return unify(x, y)
    elif type(x) == str and type(y) == str: # Testing concrete syntax strings.
        return unify(parser(grammar, 'expression')(x), parser(grammar, 'expression')(y))


def unify(a, b):

    if type(a) == Leaf and type(b) == Leaf:
        if a == b:
            return None


    if type(a) == Node:
        for label in a:
            children = a[label]
            if label == "Variable":
                f = children[0]
                abs = {f: b}
                return abs

    if type(b) == Node:
        for label in b:
            children = b[label]
            if label == "Variable":
                f = children[0]
                abs = {f: a}
                return abs

    if type(a) == Node and type(b) == Node:
        for label in a:
            for label2 in b:
                if label == label2 and len(a) == len(b):
                    children1 = a[label]
                    children2 = b[label2]
                    unifiedDict = {}
                    uni = unify(children1[0],children[0])
                    if uni is not None:
                        unifiedDict= uni.copy()
                    i = 1
                    while i < len(children1):
                        uni = unify(children1[i],children[i])
                        if uni is not None:
                            unifiedDict.update(uni)
                        i += 1
                    if a != b and unifiedDict == {}:
                        return None

                    return unifiedDict



def testEvaluate(d, e):
    return evaluate(build({}, parser(grammar, 'declaration')(d)), {}, parser(grammar, 'expression')(e))


def build(m, d):
    if type(d) == Node:
        for label in d:
            children = d[label]
            if label == "Function":
                m1 = m
                f1 = children[0]["Variable"][0]
                f2 = children[1]
                f3 = children[2]
                d = children[3]
                if f1 not in m1:
                    m1[f1] = [(f2,f3)]
                    m2 = build(m1,d)
                    return m2
                else:
                    m1[f1].append((f2,f3))
                    m2 = build(m1,d)
                    return m2

    if type(d) == Leaf:
        if d == "End":
            return m



def evaluate(m, env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == "Apply":
                m1 = m
                f = children[0]["Variable"][0]
                e = children[1]
                tuples = m1[f]
                tupleLength = len(tuples)
                v1 = evaluate(m,env,e)
                check = []
                track = "None"
                for x in range(tupleLength):
                    lengthUni = unify(tuples[x][0],v1)
                    if lengthUni is None:
                        check.append("None")
                    else:
                        check.append(len(lengthUni))
                for x in range(len(check)):
                    if check[x] == "None":
                        continue
                    elif track == "None" and check[x] >= 0:
                        track = x
                    elif check[x] < check[track]:
                        track = x
                sub = unify(tuples[track][0],v1)
                if sub is not None:
                    env.update(sub)
                    v2 = evaluate(m1,env,tuples[track][1])
                    return v2

            elif label == "Mult":
                f1 = children[0]
                f2 = children[1]
                x1 = f1["Number"][0]
                x2 = f2["Number"][0]
                x3 = (x1 * x2)
                return ({"Number": x3})

            elif label == "ConInd":
                x = children[0]
                f1 = children[1]
                f2 = children[2]
                v1 = evaluate(m,env,f1)
                v2 = evaluate(m,env,f2)
                return ({"ConInd": [x,v1,v2]})

            elif label == "ConBase":
                return e

            elif label == "Variable":
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound")
                    exit()

            elif label == "Number":
                return e



def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ')
        if s == ':quit':
            break

        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof