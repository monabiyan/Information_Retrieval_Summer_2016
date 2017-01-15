def f(n,x,bahre):
    if n ==1: return x
    saving=(1+float(bahre))*f(n-1,x,bahre)+x
    return(saving)
x=[]
y=[]
sal=30
for i in range(0,sal):
    x.append(i+1)
    y.append(f(i+1,40000,0.15))






import matplotlib.pyplot as plt
plt.plot(x, y, 'ro')
plt.axis([0, 30, 0, 20000000])
plt.show()