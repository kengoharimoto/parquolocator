#!/usr/local/bin/python3
# /usr/bin/python3 does not work; it appearst to be an older version. Alternatively python3 points to the one in local so that works, too...

import sys
import re
import khpql

# The script should behave a bit nice
# So, it exits without doing anything if not enough arguments are not given
if len(sys.argv) < 3:
    sys.stderr.write("Give me at least two arguments. Thank you!\n")
    sys.exit()

khpql.SCORE=60

# now time to determine what to do.
lines1 = khpql.prepare_buffer_from_file(sys.argv[1]) # these read paragraphs without deviding paragraphs at all

## a few other possible ways of preparing the buffer whose content is checked against other files
# lines1 = khpql.prepare_buffer_from_file_cutting_at_dandas(sys.argv[1])
# be careful not to specify lower than 30!
# lines1 = khpql.prepare_buffer_from_file_cutting_at_equal_length(sys.argv[1], 50)

for i in sys.argv[2:]: # note that we start from the second argument
    lines2 = khpql.prepare_buffer_from_file_cutting_at_equal_length(i, 500)
    # lines2 = khpql.prepare_buffer_from_file(i)
    # lines2 = khpql.prepare_buffer_from_file_cutting_at_dandas(i)
    # choose what you want to do. The last one needs a string for comparison. So, it has to be used with 
    # compare_lines(lines1, lines2)
    
    khpql.find_quotes_in_a_text(lines1, lines2)
    
