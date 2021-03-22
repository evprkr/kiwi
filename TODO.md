This is a rough list of things I am planning to add to Kiwi, in no particular order.

For function usage descriptions, I'm using * to denote an optional argument

* User function definitions and calls
* Arrays
	- lists ``[item]`` - store any data type in a specific order
	- sets ``(item)`` - store one data type in a specific order
	- tables ``{key : item}`` - store any data type with indices and keys, can be modified
* List functions
	- ``list.add(x)`` - appends x to the end of a list
	- ``list.rem(n, x*)`` - removes the last n items in a list, or removes n instances of x starting from the end of a list
	- ``list.empty(x*)`` - removes all items from a list, excluding x
 	- ``list.shuffle(seed*)`` - returns the list/set in a random order, default seed is the current system time
	- ``list.index(x, n*)`` - returns the index (int) of item x in a list, or returns the index of the nth instance of x in a list
* Contained loops
	- ``if x in list[*]`` is a quick way to loop through and compare x to each item in a list, in order, returns True at the first match, returns False if no matches
* Built-in functions
	- ``ask`` and ``say`` for input and output
	- ``len(x)`` - returns the length (int) of items in an object
* Modules
	- Random - returning random numbers and other related functions
	- Math - more complex math functions (mod, sqrt, exp, etc.)
* Strings
	- Support for escape characters in strings
	- ``string.split(x*)`` - splits a string into an array of characters, or splits a string into an array at every instance of x
