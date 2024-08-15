import math
import random

def maxsqrt(num):
	return math.ceil(num ** 0.5) + 1

def judge_prime(x):
	if x <= 1:
		return False
	for  divisor in range(2, maxsqrt(x)):
		if x % divisor ==0:
			return False
	return True

prime = []
for num in range(1000, 10000):
	if judge_prime(num):
		prime.append(num)

#print(prime)

random_factor1 = random.choice(prime)
random_factor2 = random.choice(prime)
random_password = random_factor1 * random_factor2
print(f"Your random password is: {random_password}")





