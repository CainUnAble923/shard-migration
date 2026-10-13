exec(open('fit.py').read())
import sys
X0,Y0,X1,Y1=map(int,sys.argv[1:5])
for y in range(Y0,Y1+1):
    row=[]
    for x in range(X0,X1+1):
        s=surfaces(x,y)
        row.append(('/'.join(str(z) for z in s) or '.').rjust(6))
    print(str(y).rjust(4),''.join(row))
print('     '+''.join(str(x).rjust(6) for x in range(X0,X1+1)))
