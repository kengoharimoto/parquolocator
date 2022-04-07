import sys
import re
# import numpy

from rapidfuzz import process, fuzz, utils
from rapidfuzz.string_metric import levenshtein, normalized_levenshtein
from rapidfuzz.fuzz import ratio

lines1 = [] # the whole content of file 1
lines2 = [] # the whole content of file 2

# Some lines don't even have to be looked at if they are colophons or extremely common phrase that appear everywhere. The following are regular expressions. If they are found in the search buffer, the buffer will be skipped. Perhaps they should eventually be stored in a file and called from the command line.
ignore_list = ["śrīmatparamahaṃsaparivrājak", 
                "śiṣyasya śrīmacchaṃkarabhagavat", 
                "\-\-\-\-\-\-\-*", 
                "____*",
                "=====*",
                "^\%",
                "paramahaṃsaparivrājakācāry",
                "pūjyapādaśiṣya"]

# This is the the cutoff ratio between 0 and 100. 0 is "nothing is shared at all" and 100 is "completely identical." Obviously somewhere in between. Currently it is hard coded but different situations call for different numbers. Eventually this should be specified in the command line. At the moment, the value can be changed from inside the executable script in the form of khpql.SCORE.
SCORE = 70

def prepare_buffer_from_file(file_ref):
    with open(file_ref) as f:
        return f.readlines()

def prepare_buffer_from_file_cutting_at_dandas(file_ref):
    sentences = []
    with open(file_ref) as f:
        while a_line := f.readline():
            sentences.extend(a_line.split("|"))
        return sentences

def prepare_buffer_from_file_cutting_at_equal_length(file_ref, length):
    sentences = []
    with open(file_ref) as f:
        the_whole = f.read()
        the_whole = the_whole.replace('\n', "¶")
        sentences = [the_whole[i:i+length] for i in range(0, len(the_whole), length)]
        return sentences

def skip_or_check(a_line):
    if (len(a_line) < 30): # arbitrary length; this should be changeable from command line?
        return True # True means that the line is to be skipped
    for pattern in ignore_list:
        if re.search(pattern, a_line):
            return True

# The following function is only useful when comparing a predominatly verse text with another predominantly verse text. It won't find passages where verse lines are quoted in prose, for example. We could make the score_cutoff much smaller but then the script will find lines that are close in length with the subject but will most likely miss a very long line (a paragraph) that contains the verse line in the form of quotation.
def compare_lines(subject, object):
    i = 0
    for the_line in subject:
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
    message = "{:.2f}% "
    for the_line in subject:
        i = i + 1
        progress = i/lines*100
        # sys.stderr.write(message.format(progress))
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

# Here is me thinking just loudly...
# let us find a verse (lines) from a certain text quoted in a prose text. In that case, we may expect verse lines are already delimited with new lines in the subject file. Those lines are probably more or less like more than 30 characters and less than 50 characters. Shall we first just try if the line is found in prose paragraphs? By reading a verse text and look for each line in whatever formatted prose text lines/paragraphs, etc.?

# The following is a remanant from the time this file was a standalone script...
# # So, here is the body --------------------------------------------------------
#
# # The script should behave a bit nice
# # So, it exits without doing anything if not enough arguments are not given
# if len(sys.argv) < 3:
#     sys.stderr.write("Give me at least two arguments. Thank you!\n")
#     sys.exit()
#
# # now time to determine what to do.
# lines1 = prepare_buffer_from_file(sys.argv[1]) # these read paragraphs without deviding paragraphs at all
# lines2 = prepare_buffer_from_file(sys.argv[2])
# # lines1 = prepare_buffer_from_file_cutting_at_dandas(sys.argv[1])
# # lines2 = prepare_buffer_from_file_cutting_at_dandas(sys.argv[2])
# # lines1 = prepare_buffer_from_file_cutting_at_equal_length(sys.argv[1], 30)
# # lines2 = prepare_buffer_from_file_cutting_at_equal_length(sys.argv[2], 200)
#
# # for the_line in lines1:
# #     print(the_line)
#
#
# # searchthis = sys.argv[1] # This line was here for experimenting. This read the first argument as the string to search
#
# # choose what you want to do. The last one needs a string for comparison. So, it has to be used with
# compare_lines(lines1, lines2)
# # calc_distances_of_contents_of_two_files(lines1, lines2)
# # find_quotes_in_a_text(lines1, lines2)
