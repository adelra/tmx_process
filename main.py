#
# Copyright 2018 Auther: Adel Rahimi
#
'''
This is a simple implementation for reading, aligning, tokenizing and outputting summary for TMX files.
'''

# imports
import argparse
import binascii
import gzip
import pickle
import re
import xml.etree.ElementTree as ET

# arguments available
parser = argparse.ArgumentParser(description='TMX Processor.')
parser.add_argument('--input',
                    help='The input file', type=str, default='en-fr.tmx.gz')
parser.add_argument('--output',
                    help='The outpu of the aligned texts', type=str, default='output-aligned.txt')
parser.add_argument('--tokenize',
                    help='Using this flag will enable the tokenize mode, which will write out the tokenized form of the aligned text',
                    type=str, default=None)
args = parser.parse_args()
input_file = args.__dict__["input"]
output_file = args.__dict__["output"]
tokenize = args.__dict__["tokenize"]


class TmxProcess:
    def file_handler(self, input_file, output_file, tokenize):
        # file handling
        try:
            self.tokenize_output = open(tokenize, "wb")
        except None:
            pass
        with open(input_file, 'rb')as input_file_open:
            if binascii.hexlify(input_file_open.read(2)) == b'1f8b':
                ''' if the input is a gzip file, 1f8b test, it will be extracted. 
                Otherwise the file will be read as a normal
                text file.'''
                input_gzip = gzip.GzipFile(input_file, 'rb')
                gzip_contents = input_gzip.read()
                input_gzip.close()
                out_contents = open("extracted-" + input_file, 'wb')
                out_contents.write(gzip_contents)
                out_contents.close()
                tmx_file = open("extracted-" + input_file)
            else:
                tmx_file = open(input_file)

        # separate files
        root = ET.parse(tmx_file).getroot()
        number_of_languages = len(root.find(".//tu//tuv")) + 1
        languages = [[] for langs in range(number_of_languages)]
        for L in range(number_of_languages):
            for item in root.findall(".//tu//tuv[" + str(L + 1) + "]//seg"):
                languages[L].append(item.text)
        lang = 1
        output = open(output_file, "w")
        while lang < len(languages):
            for line in languages[0]:
                # whitespace normalization
                line = re.sub("[ \t\n]+", " ", line)
                translation = re.sub("[ \t\n]+", " ", languages[lang][languages[0].index(line)])
                output.write(line + "\t" + translation + "\n")
                # tokenizer
                '''
                Since we do not know our target languages we will use simple tokenization based on space. 
                Other sophisticated methods could be language identification and tokenization based on the output of the 
                identification, however since this takes much resources we will be using the simple method.
                '''
                if tokenize is None:
                    pass
                else:
                    self.tokenized_line = line.split(" ")
                    self.tokenized_tranlation = translation.split(" ")
                    pickle.dump(self.tokenized_line, self.tokenize_output)
                    pickle.dump(self.tokenized_tranlation, self.tokenize_output)
            lang += 1

    def summary(self, tokenized_text):
        print("Number of tokens = " + str(len(tokenized_text)))
        print("Number of unique tokens = " + str(len(set(tokenized_text))))
        print("Most frequent token = " + max(set(tokenized_text), key=tokenized_text.count))
        return None


if __name__ == '__main__':
    process = TmxProcess()
    process.file_handler(input_file, output_file, tokenize)
    process.summary(pickle.load(open(tokenize, "rb")))
