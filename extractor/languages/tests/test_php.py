import unittest
import re, os
from languages import php
from binder import readSingleLine,readMultiLineDiff,contSingleLines

class PHPTest(unittest.TestCase):
    
    def test_output(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.php")
        regex = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        sign = '//'
        comment_single = php.readSingleLine(path,regex,sign)
        comment_multiline = php.readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        comment_contSingleline = php.contSingleLines(comment_single)
        self.assertTrue(comment_single)
        self.assertTrue(comment_multiline)
        self.assertTrue(comment_contSingleline)



    def test_outputFormat(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.php")
        regex = r'''(\/\/\s*[\w #\.()@+-_*\d]*)'''
        self.syntax_start = "/*"
        self.syntax_end ='*/'
        sign = '//'
        expected = php.phpExtractor(path)
        comment_single = readSingleLine(path,regex,sign)
        comment_multiline = readMultiLineDiff(path,self.syntax_start,self.syntax_end)
        comment_contSingleline = contSingleLines(comment_single)
        file = path.split("/")
        output = {
        "metadata": [{
        "filename": file[-1],
        "lang": "PHP",
        "total_lines": comment_single[1],
        "total_lines_of_comments": comment_single[3]+comment_multiline[3],
        "blank_lines": comment_single[2],
        "sloc": comment_single[1]-(comment_single[3]+comment_multiline[3]+comment_single[2])
        }],
        "single_line_comment": [],
        "cont_single_line_comment": [],
        "multi_line_comment": []
        }

        if comment_contSingleline:
            comment_single = comment_contSingleline[0]

        if comment_single:
            for i in comment_single[0]:
                output['single_line_comment'].append({"line_number" :i[0],"comment": i[1]})

        if comment_contSingleline:
            for idx,i in enumerate(comment_contSingleline[1]):
                output['cont_single_line_comment'].append({"start_line": comment_contSingleline[1][idx], "end_line": comment_contSingleline[2][idx], "comment": comment_contSingleline[3][idx]})

        if comment_multiline:
            for idx,i in enumerate(comment_multiline[0]):
                output['multi_line_comment'].append({"start_line": comment_multiline[0][idx], "end_line": comment_multiline[1][idx], "comment": comment_multiline[2][idx]})

        self.assertEqual(output,expected)

    def test_Source(self):
        path = os.path.join(os.getcwd(),"languages/tests/TestFiles/textcomment.php")
        name = "source.txt"
        newfile = php.phpSource(path,name)

        self.assertTrue(newfile)  