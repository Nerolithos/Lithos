import textwrap

def guess_number():
	print("Please choose a random integer from 1 to 100.")
	print("I'll try to guess it by asking you questions about it.")
	input("When you're ready, hit \"ENTER\".")

	minimum = 1
	maximum = 100
	trial = 0

	while minimum <= maximum:
		trial += 1
		guess = (minimum + maximum) // 2  
# "//" divides the number before it by the number after it and keeps the integral part.
		print(f"I guess it was {guess}.")
		feedback = input(textwrap.dedent("""If I'm right, hit \"=\". 
If the actual number is larger than the guessed one, hit \"+\". 
If the actual number is smaller, hit \"-\". 
>"""))

		if feedback == "=":
			print(f"It's correct! The number was {guess}.") 
			print(f"I tried {trial} times to get it right.")
			print("My method is based on dichotomy, can you find a better approach?")
			break
		elif feedback == "+":
			minimum = guess + 1
		elif feedback == "-":
			maximum = guess - 1
		else:
			print(f"\"{feedback}\" is an invalid input.")
			print("Please describe again using only \"=\", \"+\", or \"-\".")
			trial -= 1

		if minimum > maximum or trial > 7:
			print("Your number is out of range, or contains decimals.")
			print("If not, you have changed the initial number. I don't like cheaters.")
			break

guess_number()
