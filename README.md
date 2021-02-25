# Kiwi
Kiwi is just a pet project of mine that I'm working on while I learn about programming language design. You can clone the repo to your computer, then run ``shell.py`` to play with Kiwi!

### Features
Kiwi is currently extremely barebones, so below is a list of features that have been implemented:
* Basic lexing for numbers and mathematical operators
* Number conversion to floats or integers

### Code Examples
FizzBuzz sequence
	for i to 100 >>
		if i % 15 is 0 >> say "FizzBuzz"
		elif i % 3 is 0 >> say "Fizz"
		elif i % 5 is 0 >> say "Buzz"
		else >> say i

Convert fahrenheit to celsius
	x = ask "What is the temperature today in F?"
	y = (x - 32) * 5/9
	say "That's {y} degrees celsius!"
