# Kiwi
Kiwi is just a pet project of mine that I'm working on while I learn about programming language design. It's a small language written and interpreted into Python code. The goal I have in mind is to make the language extremely simple to read, write, and understand, even for total beginners. You can clone the repo to your computer, then run ``shell.py`` to test it out!

### Features
Kiwi is currently extremely barebones, so below is a list of features that have been implemented:
* Basic lexing, parsing, and interpreting of mathematical functions
* Variable assignment and referencing of numbers and strings
* Error messages (with tracebacks!) for various wrongdoings

### Code Examples
This is an example of the (future) syntax of Kiwi, which is still subject to change. Since the language is still underdeveloped, this is all just conceptual.

	// Print FizzBuzz sequence
	for i to 100 >>
		if i % 15 is 0 >> say "FizzBuzz"; <<
		elif i % 3 is 0 >> say "Fizz"; <<
		elif i % 5 is 0 >> say "Buzz"; <<
		else >> say i; <<
	<<
		
&nbsp;

	// Convert fahrenheit to celsius
	num x = ask "What is the temperature today in F?";
	num y = (x - 32) * 5/9;
	say "That's {y} degrees celsius!";

&nbsp;

	// Contained for loop
	list whitelist = ["Steve", "Bill", "Linus"];
	str name = ask "What is your name? ";

	if name in whitelist[*] >>
		say "Access Granted!";
	<< else >> say "Access Denied!"; <<
