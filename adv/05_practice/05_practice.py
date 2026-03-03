def parametrized_func(a, b):
    def circle(x, y):
        return a*x**2 + b* y**2
    return circle


summ_x_y = parametrized_func(2, 3)
print(summ_x_y(1, 2))

summ2=parametrized_func(5, 6)
print(summ2(1,2))