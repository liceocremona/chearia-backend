import re 

dataid_regex = re.compile("(example|CO|altitude|humidity|ozone|pressure|temperature)")
timestamp1_regex = re.compile("")

timestamp2_regex = re.compile("^(0[1-9]|[12][0-9]|3[01])[- \/.](0[1-9]|1[012])[- \/.](19|20)\d\d$") #https://www.regular-expressions.info/dates.html