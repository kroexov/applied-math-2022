import math


def fib(n):
    a = 0
    b = 1
    for __ in range(n):
        a, b = b, a + b
    return a


def func(x):
    return math.pow(x, math.sin(x))


def dichotomy(a, b, eps):
    # complexity: ln((a0-b0)/Eps)/ln(2)
    relation = 0
    sigma = eps / 4
    iterations = 0
    while b - a > eps:
        iterations += 1
        middle = (b + a) / 2
        left = middle - sigma
        right = middle + sigma
        func_left = func(left)
        func_right = func(right)
        if func_left > func_right:
            relation += ((b - a) / (b - left))
            a = left
        elif func_left < func_right:
            relation += ((b - a) / (right - a))
            b = right
        else:
            relation += ((b - a) / (right - left))
            (a, b) = (left, right)
    print("average relation", relation / iterations)
    print("num of iterations is", iterations)
    print("num of function calls is", iterations * 2)
    return [a, b]


def golden_ratio(a, b, eps):
    # complexity: more than in dichotomy, but only one func() call per iteration
    gr_for_left = 2 / (3 + math.sqrt(5))
    gr_for_right = 2 / (1 + math.sqrt(5))
    left = a + gr_for_left * (b - a)
    right = a + gr_for_right * (b - a)
    func_left = func(left)
    func_right = func(right)
    # in two previous lines we count func from left and right golden ratios, so we will reduce counting time in the
    # future iterations, because we will count it only once
    iterations = 0
    relation = 0
    while b - a > eps:
        iterations += 1
        if func_left > func_right:
            relation += ((b - a) / (b - left))
            (a, left, func_left) = (left, right, func_right)
            right = a + gr_for_right * (b - a)
            func_right = func(right)
        else:
            relation += ((b - a) / (right - a))
            (b, right, func_right) = (right, left, func_left)
            left = a + gr_for_left * (b - a)
            func_left = func(left)
    print("average relation", relation / iterations)
    print("num of iterations is", iterations + 1)
    print("num of function calls is", iterations + 2)
    return [a, b]


def fibonacci(a, b, eps):
    # complexity: precounted num of iterations | only one func() call per iteration
    # theoretically, this is the most optimal method for guaranteed reduce of base segment [a,b]
    # this means that by using this method, we can most optimally find our final segment and use only one func() call!
    # in this function we will find n of iterations before start, because we already know rules of fibonacci functions
    n = 1
    relation = 0
    while 1 / fib(n) > eps:
        n += 1
    n = n - 2
    print("num of iterations is", n)
    print("num of function calls is", n + 2)
    left = a + (b - a) * (fib(n - 1) / fib(n + 1))
    right = a + (b - a) * (fib(n) / fib(n + 1))
    func_left = func(left)
    func_right = func(right)
    for i in range(n):
        fib_for_left = (fib(n - i - 1) / fib(n - i + 1))
        fib_for_right = (fib(n - i) / fib(n - i + 1))
        if func_left > func_right:
            relation += ((b - a) / (b - left))
            (a, left, func_left) = (left, right, func_right)
            right = a + (b - a) * fib_for_right
            func_right = func(right)
        else:
            relation += ((b - a) / (right - a))
            (b, right, func_right) = (right, left, func_left)
            left = a + (b - a) * fib_for_left
            func_left = func(left)
    print("average relation", relation / n)
    return [a, b]


def choose_points(a, b):
    function_calls = 0
    step = (a + b) / 4
    (x1, x2, x3) = (a + step, a + 2 * step, a + 3 * step)

    while func(x1) < func(x2):
        function_calls += 2
        half = (x1 - a) / 2
        x1 -= half
        x2 -= half

    while func(x3) < func(x2):
        function_calls += 2
        half = (b - x3) / 2
        x2 += half
        x3 += half

    return x1, x2, x3, function_calls


def parabola_min(x, f):
    x1, x2, x3 = x
    f1, f2, f3 = f

    a1 = (f2 - f1) / (x2 - x1)
    a2 = 1 / (x3 - x2) * ((f3 - f1) / (x3 - x1) - (f2 - f1) / (x2 - x1))
    return 1 / 2 * (x1 + x2 - a1 / a2)


def parabolas(a, b, eps):
    relation = 0
    x_min = -1
    iterations = 0
    (x1, x2, x3, function_calls) = choose_points(a, b)
    (f1, f2, f3) = map(func, [x1, x2, x3])
    function_calls += 3

    d_cur = b - a
    while True:
        x_min_prev = x_min
        x_min = parabola_min([x1, x2, x3], [f1, f2, f3])

        if abs(x_min - x_min_prev) < eps:
            print("num of iterations is", iterations)
            print("num of function calls is", function_calls)
            print("average relation", relation / iterations)
            return x_min

        f_min = func(x_min)
        function_calls += 1

        if x_min > x2 and f_min > f2:
            (x1, x2, x3) = (x1, x2, x_min)
            (f1, f2, f3) = (f1, f2, f_min)
        elif x_min < x2 and f_min < f2:
            (x1, x2, x3) = (x1, x_min, x2)
            (f1, f2, f3) = (f1, f_min, f2)
        elif x_min > x2 and f_min < f2:
            (x1, x2, x3) = (x2, x_min, x3)
            (f1, f2, f3) = (f2, f_min, f3)
        elif x_min < x2 and f_min > f2:
            (x1, x2, x3) = (x_min, x2, x3)
            (f1, f2, f3) = (f_min, f2, f3)

        d_prev = d_cur
        d_cur = x3 - x1

        relation += (d_prev / d_cur)
        iterations += 1


def pointsDifferent(x, w, v):
    eps = 0.0001
    return (x - w) > eps and (x - v) > eps and (w - v) > eps


def brent(a, b, eps):
    relation = 0
    r = (3 - math.sqrt(5)) / 2
    x = w = v = (a + b) / 2
    f_x, f_w, f_v = map(func, [x, w, v])
    d_cur = d_prev = b - a
    iterations = 0
    function_calls = 3

    while True:
        if max(x - a, b - x) < eps:
            print("num of iterations is", iterations)
            print("num of function calls is", function_calls)
            print("average relation", relation / iterations)
            return x

        g = d_prev / 2
        d_prev = d_cur

        if pointsDifferent(x, w, v):
            u = parabola_min([x, w, v], [f_x, f_w, f_v])

        if not pointsDifferent(x, w, v) or not (a + eps <= u <= b - eps and abs(u - x) < g):
            if 2 * x < a + b:
                u = x + r * (b - x)
                d_prev = b - x
            else:
                u = x - r * (x - a)
                d_prev = x - a

        d_cur = abs(u - x)
        relation += (d_prev / d_cur)
        f_u = func(u)
        function_calls += 1

        if f_u < f_x:
            if u < x:
                b = x
            else:
                a = x

            (x, w, v) = (u, x, w)
            (f_x, f_w, f_v) = (f_u, f_x, f_w)
        else:
            if u < x:
                a = u
            else:
                b = u

            if f_u < f_w:
                (w, v) = (u, w)
                (f_w, f_v) = (f_u, f_w)

        iterations += 1


print("========== DICHOTOMY ==========\n")
print(dichotomy(-3,5, 10 ** -6), "\n")
print("========== GOLDEN RATIOS ==========\n")
print(golden_ratio(-3,5, 10 ** -6), "\n")
print("========== FIBONACCI METHOD ==========\n")
print(fibonacci(0,2, 10 ** -6), "\n")
print("========== PARABOLAS METHOD ==========\n")
print(parabolas(0,2, 10 ** -6), "\n")
print("========== BRENT'S METHOD ==========\n")
print(brent(0,2, 10 ** -6), "\n")
