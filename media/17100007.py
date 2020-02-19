import random
import math

ZERO_POINT = "id element at infinity"

p=0
a=0
def modInverse(a) : 
    m=p
    m0 = m 
    y = 0
    x = 1
  
    if (m == 1) : 
        return 0
  
    while (a > 1) : 
        q = a // m   
        t = m 
        m = a % m 
        a = t 
        t = y 
        y = x - q * y 
        x = t  
    if (x < 0) : 
        x = x + m0
    return x

def add(x1,y1,x2,y2):
    if(x2 == ZERO_POINT):
        return [ x1,y1]
    if(x1== ZERO_POINT):
        return [x2,y2]
    if(x1==x2 and y2 ==(p-y1)%p):
        return [ZERO_POINT, ZERO_POINT]
    if(x1==x2 and y1==y2):
        lamda = (((3*x1**2+a)%p)*modInverse((2*y1)%p))%p
    else:
        lamda = (((y2-y1)%p)* modInverse((x2-x1)%p))%p
    x3 = (lamda**2 - x1 - x2)%p
    y3 = ((lamda*(x1 - x3))%p - y1)%p
    return [x3,y3]

def mult(d: int, point):
    ans = point[:]
    for i in range(d-1):
        ans = add(ans[0], ans[1], point[0], point[1])
    return ans

def inversOf(x, y):
    if(x==ZERO_POINT):
        return [ZERO_POINT, ZERO_POINT]
    return [x, (-y)%p]

def encrypt(plain,e1,e2,r):
    c1 = mult(r, e1)
    c2 = add(*plain, *mult(r,e2))
    return [c1,c2]

def decrypt(c1,c2, d):
    ans = add(*c2, *inversOf(*mult(d,c1)))
    return ans

# def pointGenerator(a, b):
# 	x = 0
# 	while(x < 13):
# 		p = ((x ** 3) + (a * x) + b) % 13
# 		if(math.sqrt(p) % 1 == 0):
# 			return x, int(math.sqrt(p))
# 		x += 1

def findAll(a, b, p):
	x = 0
	l = []
	while(x < p):
		temp = ((x ** 3) + (a * x) + b) % p
		if(math.sqrt(temp) % 1 == 0):
			l.append([x, int(math.sqrt(temp))])
			l.append([x, (p - int(math.sqrt(temp)))%p])
		x += 1
	return l

a, b = list(map(int, input("Enter values of a and b for the elliptical curve: ").split()))
p = int(input("Enter prime for the gallois field: "))
plain_list = findAll(a, b, p)
print("Possible points on curve are: ", plain_list)
# e1x, e1y = pointGenerator(a, b)
ind = int(input("Choose e1 from the list (index: 0 to {}): " .format(len(plain_list) - 1)))
# e1 = [e1x, e1y]
e1 = plain_list[ind]
d = int(input("Enter a random number d as private key: "))
# d=6
ind = input("Choose a plain-text from the list (index: 0 to {}): " .format(len(plain_list) - 1))
plain = plain_list[int(ind)]
print("Key e1 is", e1)
e2x, e2y = mult(d, e1)
e2 = [e2x, e2y]
print("Key e2 is", e2)
print("Plain text is ", plain)
r = random.randint(1, 10)
# r=5
c1, c2 = encrypt(plain, e1,e2, r)
print("The cipher text is ", c1,c2)

plaindash = decrypt(c1,c2, d)
print("Decryption is", plaindash)


