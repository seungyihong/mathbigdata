#2016111547 수학과 홍승이
#문제1-1,2

import matplotlib.pyplot as plt

salary=[]
tax=[]
x=[]
total=[]
y=0
dtax=0

for i in range (1000,20010,10) :
    salary.append(i)
    if (i<=1200) :
        tax.append(i*0.06)
    elif (i>1200 and i<=4600) :
        tax.append(72+(i-1200)*0.15)
    elif (i > 4600 and i <= 8800):
        tax.append(582 + (i - 4600) * 0.24)
    elif (i>8800 and i<=15000) :
        tax.append(1590+(i-8800)*0.35)
    else :
        tax.append(3760 + (i - 15000) * 0.38)


for i in range ( 1000, 5010 , 10) :
    x.append(i)
    sum=0
    for j in range(0,28):
        y = i*pow((1+0.03),j)
        if (y <= 1200):
            dtax= y * 0.06
        elif (y > 1200 and y <= 4600):
            dtax = 72 + (y - 1200) * 0.15
        elif (y > 4600 and y <= 8800):
            dtax = 582 + (y - 4600) * 0.24
        elif (y > 8800 and y <= 15000):
            dtax= 1590 + (y - 8800) * 0.35
        else:
            dtax = 3760 + (y - 15000) * 0.38
        sum = sum + (y-dtax)*0.1
    total.append(sum)

plt.plot(salary,tax)
plt.show()
plt.plot(x,total)
plt.show()
