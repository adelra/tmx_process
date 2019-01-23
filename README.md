*Simple TMX file reader*

This is a simple TMX file reader. It uses basic Python's built-in libraries so there is no need to install third party libraries.
There are two main functions: file_handler and summary().

*Functions*

file_handler has two arguments: input file of the TMX and the output aligned for each two pair of languages based on the first language.
the summary function has one input, which is the tokenized pickle output from the file_handler(). and it gives some statistics based on the text.

*Arguments*

To run the main.py file you can use 3 arguments:
--input = the input of the file. The function will determine if it is a gzip file or a TMX file and starts processing each in a different way.
--output = the output of the aligned text separated by \t
--tokenize = if this argument is given, the output of the tokenized data will be saved as a list in pickle file format.


You could also use cPickle (C version) to speed up the process.
Codacy Badge
