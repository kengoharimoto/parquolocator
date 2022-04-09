#!/usr/local/bin/python3
# /usr/bin/python3 does not work; it appearst to be an older version. Alternatively python3 points to the one in local so that works, too...

import sys
import re
import khpql

khpql.SCORE = 70

# The script should behave a bit nice
# So, it exits without doing anything if not enough arguments are not given
if len(sys.argv) < 3:
    sys.stderr.write("Give me at least two arguments. Thank you!\n")
    sys.exit()
    
# now time to determine what to do.
lines1 = khpql.prepare_buffer_from_file(sys.argv[1]) # these read paragraphs without deviding paragraphs at all

## a few other possible ways of preparing the buffer whose content is checked against other files
# lines1 = prepare_buffer_from_file_cutting_at_dandas(sys.argv[1])
# lines1 = prepare_buffer_from_file_cutting_at_equal_length(sys.argv[1], 30)

# Now we go through all the remaining argument (files)

for i in sys.argv[2:]: # note that we start from the second argument
    lines2 = khpql.prepare_buffer_from_file(i)
    ## a few other means to prepare buffers to check if they contain what we look for
    # lines2 = prepare_buffer_from_file_cutting_at_dandas(i)
    # lines2 = prepare_buffer_from_file_cutting_at_equal_length(i, 200)

    ## choose what you want to do. The last one needs a string for comparison. So, it has to be used with 
    khpql.compare_lines(lines1, lines2)
    # find_quotes_in_a_text(lines1, lines2)
