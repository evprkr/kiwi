# Kiwi
Kiwi is just a pet project of mine that I'm working on while I learn about programming language design. It's a small language written and interpreted into Python code. The goal I have in mind is to make the language extremely simple to read, write, and understand. You can clone the repo to your computer, then run ``shell.py`` to play with Kiwi!

### Features
Kiwi is currently extremely barebones, so below is a list of features that have been implemented:
* Basic lexing, parsing, and interpreting of mathematical functions
* Errors for illegal characters, invalid syntax, and runtime errors (with tracebacks!)

### Code Examples
This is an example of the (future) syntax of Kiwi, which is still subject to change. Since the language is still underdeveloped, this is all just conceptual.

	// Print FizzBuzz sequence
	for i to 100 >>
		if i % 15 is 0 >> say "FizzBuzz"
		elif i % 3 is 0 >> say "Fizz"
		elif i % 5 is 0 >> say "Buzz"
		else >> say i
		
&nbsp;

	// Convert fahrenheit to celsius
	x = ask "What is the temperature today in F?"
	y = (x - 32) * 5/9
	say "That's {y} degrees celsius!"
