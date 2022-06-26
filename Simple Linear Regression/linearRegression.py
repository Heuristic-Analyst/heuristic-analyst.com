import random

x1 = [i+(random.random()*50-25) for i in range(1000)]
x2 = [i+(random.random()*20-10) for i in range(1000)]
x3 = [i+(random.random()*100-50) for i in range(1000)]
x4 = [i+(random.random()*10000-5000) for i in range(1000)]
x5 = [i+(random.random()*10-5) for i in range(1000)]

y = []

for i in range(len(x1)):
    y.append(8+3*x1[i]+(-9)*x2[i]+15*x3[i]+0.25*x4[i]+(+0.5)*x5[i]+(random.random()*10-5))

print(y[10])
print(8+3*x1[10]+(-9)*x2[10]+15*x3[10]+0.25*x4[10]+(+0.5)*x5[10])
