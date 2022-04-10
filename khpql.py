import sys
import re
# import numpy

from rapidfuzz import process, fuzz, utils
from rapidfuzz.string_metric import levenshtein, normalized_levenshtein
from rapidfuzz.fuzz import ratio

# Some lines don't even have to be looked at if they are colophons or extremely common phrase that appear everywhere. The following are regular expressions. If they are found in the search buffer, the buffer will be skipped. Perhaps they should eventually be stored in a file and called from the command line.
ignore_list = ["śrīmatparamahaṃsaparivrājak", 
                "śiṣyasya śrīmacchaṃkarabhagavat", 
                "\-\-\-\-\-\-\-*", 
                "____*",
                "=====*",
                "^\%",
                "paramahaṃsaparivrājakācāry",
                "pūjyapādaśiṣya",
                "pratham.*dhyāya",
                "pratham.*pāda",
                "dvitīy.*dhyāy",
                "\. \. \. \. \. \. \. \.",
                "^\<[^>]*\>$",
                "^ *\<rdg.*\<\/rdg\>$",
                "\-\-\{\}\-\-\{\}",
                " \-\- \-\- \-\-"]

# This is the the cutoff ratio between 0 and 100. 0 is "nothing is shared at all" and 100 is "completely identical." Obviously somewhere in between. Currently it is hard coded but different situations call for different numbers. Eventually this should be specified in the command line. At the moment, the value can be changed from inside the executable script in the form of khpql.SCORE.
SCORE = 70

# We skip certain short lines (e.g. len == 0) so that the program does not waste lookign for matches, or they match too many lines. However, sometimes it is good to change the value so that shor phrases can be located.
SHORTEST_LINE = 30

def prepare_buffer_from_file(file_ref):
    sentences = []
    with open(file_ref) as f:
        while a_line := f.readline():
            a_line = a_line.replace('\t', "    ")
            sentences.append(a_line)
        return sentences

def prepare_buffer_from_file_cutting_at_dandas(file_ref):
    sentences = []
    with open(file_ref) as f:
        while a_line := f.readline():
            a_line = a_line.replace('\t', "    ")
            sentences.extend(a_line.split("|"))
        return sentences

def prepare_buffer_from_file_cutting_at_equal_length(file_ref, length):
    sentences = []
    with open(file_ref) as f:
        the_whole = f.read()
        the_whole = the_whole.replace('\n', "¶")
        the_whole = the_whole.replace('\t', "    ")
        sentences = [the_whole[i:i+length] for i in range(0, len(the_whole), length)]
        return sentences

def skip_or_check(a_line):
    if (len(a_line) < SHORTEST_LINE): # arbitrary length; this should be changeable from command line?
        return True # True means that the line is to be skipped
    for pattern in ignore_list:
        if re.search(pattern, a_line):
            return True

# The following function is only useful when comparing a predominatly verse text with another predominantly verse text. It won't find passages where verse lines are quoted in prose, for example. We could make the score_cutoff much smaller but then the script will find lines that are close in length with the subject but will most likely miss a very long line (a paragraph) that contains the verse line in the form of quotation.
def compare_lines(subject, object):
    i = 0
    message1 = "{:.2f} "
    message2 = "{:.2f}\n"
    howmanylines = len(subject)
    for the_line in subject:
        progress = i/howmanylines*100
        if (i % 20 != 0):
            sys.stderr.write(message1.format(progress))
        else:
            sys.stderr.write(message2.format(progress))
        i += 1
        if skip_or_check(the_line):
            continue
        result = process.extractOne(the_line, object, scorer=ratio, 
                        processor=utils.default_process, score_cutoff=SCORE)
        if result:
            print(i, "\t", the_line.rstrip(), "\t", result[2], "\t", result[0].rstrip(), "\t", result[1])

# It is possible to define a function that checks one line with the content of a whole file but it will be the same as agrep or any other kind of grep can do. So, we should already define a function that compares the whole content of a file with that of another file. First, we assume the first file to be mostly verse.
def find_quotes_in_a_text(subject, object):
    i = 0
    lines = len(subject)
    message1 = "{:.2f} "
    message2 = "{:.2f}\n"
    for the_line in subject:
        i = i + 1
        progress = i/lines*100
        if (i % 20 != 0):
            sys.stderr.write(message1.format(progress))
        else:
            sys.stderr.write(message2.format(progress))
        if skip_or_check(the_line): continue
        j = 0
        for the_target_line in object:
            j = j+1
            if skip_or_check(the_target_line):
                continue
            result = fuzz.partial_ratio_alignment(the_line, the_target_line, 
                                    processor=utils.default_process, 
                                    score_cutoff=SCORE)
            if result.score > 0:
                print(i, "\t",
                 the_line.rstrip(), "\t",
                 j, "\t",
                 the_target_line[result.dest_start:result.dest_end], "\t",
                 the_target_line.rstrip(), "\t",
                 result.score)

# I really don't know what this does...
def calc_distances_of_contents_of_two_files(subject, object):
    result = process.cdist(subject, object, workers=-1)
    print(result)
