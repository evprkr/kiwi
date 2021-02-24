# Kiwi
#### A quick and easy programming language

Kiwi is just a pet project of mine that I'm working on while I learn about programming language design.

### Code Examples
	// FizzBuzz
	for i to 100 >>
		if i % 15 is 0 >> say "FizzBuzz"
		elif i % 3 is 0 >> say "Fizz"
		elif i % 5 is 0 >> say "Buzz"
		else >> say i

	// Temp Conversion
	x = ask "What is the temperature today in F?"
	y = (x - 32) * 5/9
	say "That's {y} degrees celsius!"
