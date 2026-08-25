"""安全数学表达式解析器：递归下降 AST，禁 eval/Function。

支持: + - * / ^ () 一元负号, 函数 sin cos tan log(自然) ln sqrt abs, 常量 pi e, 变量 x。
用法:
    from safe_expr import SafeExpr
    f = SafeExpr("sin(x)^2 + x/2")
    f.eval({"x": 1.5})
"""

import math


class _Tok:
    def __init__(self, kind, val):
        self.kind = kind  # num | id | op | lparen | rparen | comma
        self.val = val


def _tokenize(s):
    toks = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or (ch == "." and i + 1 < len(s) and s[i + 1].isdigit()):
            j = i
            while j < len(s) and (s[j].isdigit() or s[j] == "."):
                j += 1
            toks.append(_Tok("num", float(s[i:j])))
            i = j
        elif ch.isalpha() or ch == "_":
            j = i
            while j < len(s) and (s[j].isalnum() or s[j] == "_"):
                j += 1
            toks.append(_Tok("id", s[i:j]))
            i = j
        elif ch in "+-*/^":
            toks.append(_Tok("op", ch))
            i += 1
        elif ch == "(":
            toks.append(_Tok("lparen", ch))
            i += 1
        elif ch == ")":
            toks.append(_Tok("rparen", ch))
            i += 1
        elif ch == ",":
            toks.append(_Tok("comma", ch))
            i += 1
        else:
            raise ValueError("bad char: %r" % ch)
    return toks


_FUNCS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "log": math.log, "ln": math.log,
    "sqrt": math.sqrt, "abs": abs,
}
_CONSTS = {"pi": math.pi, "e": math.e}


class _Parser:
    def __init__(self, toks):
        self.toks = toks
        self.pos = 0

    def peek(self):
        return self.toks[self.pos] if self.pos < len(self.toks) else None

    def next(self):
        t = self.peek()
        self.pos += 1
        return t

    # expr := term (('+'|'-') term)*
    def expr(self):
        node = self.term()
        while True:
            t = self.peek()
            if t and t.kind == "op" and t.val in "+-":
                self.next()
                rhs = self.term()
                node = ("binop", t.val, node, rhs)
            else:
                return node

    # term := unary (('*'|'/') unary)*
    def term(self):
        node = self.unary()
        while True:
            t = self.peek()
            if t and t.kind == "op" and t.val in "*/":
                self.next()
                rhs = self.unary()
                node = ("binop", t.val, node, rhs)
            else:
                return node

    # unary := '-' unary | power
    def unary(self):
        t = self.peek()
        if t and t.kind == "op" and t.val == "-":
            self.next()
            return ("neg", self.unary())
        if t and t.kind == "op" and t.val == "+":
            self.next()
            return self.unary()
        return self.power()

    # power := atom ('^' unary)?
    def power(self):
        base = self.atom()
        t = self.peek()
        if t and t.kind == "op" and t.val == "^":
            self.next()
            expo = self.unary()  # 右结合
            return ("binop", "^", base, expo)
        return base

    # atom := num | const/var | func '(' expr ')' | '(' expr ')'
    def atom(self):
        t = self.next()
        if t is None:
            raise ValueError("unexpected end")
        if t.kind == "num":
            return ("num", t.val)
        if t.kind == "id":
            nxt = self.peek()
            if nxt and nxt.kind == "lparen" and t.val in _FUNCS:
                self.next()
                arg = self.expr()
                close = self.next()
                if close is None or close.kind != "rparen":
                    raise ValueError("missing ) after %s(" % t.val)
                return ("call", t.val, arg)
            if t.val in _CONSTS:
                return ("num", _CONSTS[t.val])
            if t.val == "x":
                return ("var", "x")
            raise ValueError("unknown symbol: %s" % t.val)
        if t.kind == "lparen":
            node = self.expr()
            close = self.next()
            if close is None or close.kind != "rparen":
                raise ValueError("missing )")
            return node
        raise ValueError("unexpected token: %r" % t.val)


class SafeExpr:
    def __init__(self, text):
        text = text.replace("**", "^")
        toks = _tokenize(text)
        p = _Parser(toks)
        self.ast = p.expr()
        if p.peek() is not None:
            raise ValueError("trailing tokens at %d" % p.pos)

    def eval(self, env=None):
        env = env or {}
        return self._ev(self.ast, env)

    def _ev(self, node, env):
        kind = node[0]
        if kind == "num":
            return node[1]
        if kind == "var":
            return float(env[node[1]])
        if kind == "neg":
            return -self._ev(node[1], env)
        if kind == "binop":
            _, op, l, r = node
            a = self._ev(l, env)
            b = self._ev(r, env)
            if op == "+":
                return a + b
            if op == "-":
                return a - b
            if op == "*":
                return a * b
            if op == "/":
                return a / b
            if op == "^":
                try:
                    r2 = a ** b
                    if isinstance(r2, complex):
                        return float("nan")
                    return r2
                except (ValueError, OverflowError, ZeroDivisionError):
                    return float("nan")
        if kind == "call":
            fname, argnode = node[1], node[2]
            v = self._ev(argnode, env)
            try:
                out = _FUNCS[fname](v)
                return float(out) if not isinstance(out, float) else out
            except (ValueError, OverflowError):
                return float("nan")
        raise ValueError("bad node: %r" % (node,))
