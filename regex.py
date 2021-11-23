###
# regex.py
# author: Connor Morgan
#
# description:
#   the goal of this program is to write a regex interpreter
#   with the following constraints:
#       - takes in test inputs as \n separated text in a txt file
#       - takes in the regex as a single string in a txt file
#           - The following expressions are supported:
#               * + [] ()
#       - outputs each string and whether it is accepted to the command line
###

def main():

    # initilizing our file variables
    inputs = open("inputs.txt","r")
    expr = open("ex.txt", "r")

    # reading the strings from the files to local variables
    regex = expr.readline()

    

    inputstrs = []
    for line in inputs:
        inputstrs.append(line.strip())
    
    # TODO: check the input strings and regex to make sure they are valid

    # running our regex against all of the strings
    for input in inputstrs:
        #run each input on the regex
        #print the output
        if run(regex,input):
            # TODO: adjust the print statements
            print(input, "\t\t\tis in the regex:", regex)
        else:
            print(input, "\t\t\tis not the regex:", regex)
    
    # cleaning up
    inputs.close()
    expr.close()
    return 0

###
# run
# parameters:
#   regex - the regex to run the comparison against
#   str - the string to compare to the regex
#
# description:
#   compares the supplied string against the supplied regex
#
# return:
#   returns true if the the string satisfies the regex
#   otherwise returns false
def run(regex,str):
    #for every token in the regex we are going to process the string
    # ex: a -> needs to be a
    #     (ab)+ -> needs to be the token ab repeated atleast once
    currstr = str
    passing = True

    parsedreg = parseregex(regex)

    for token in parsedreg:
        print(token)
    '''
    for token in parsedreg:
        
        if token == "(":
            passing = processgroup(token[1:-2] + token[-1],currstr)
            if not passing:
                return False
        elif token[-1] == "*":
            passing, currstr = processstar(token[0:-1],currstr)
            if not passing:
                return False
        elif token[-1] == "+":
            passing, currstr = processplus(token[0:-1],currstr)
            if not passing:
                return False
        else:
            passing, currstr = processtext(token,currstr)
            if not passing:
                return False
    #TODO: Do something about left over chars
    '''
    return passing

def processstar(token,str):
    while str[0:len(token)] == token:
        str = str[len(token):]
    return True, str

def processplus(token,str):
    once = False
    while str[0:len(token)] == token:
        str = str[len(token):]
        once = True
    return once, str

def processtext(token,str):
    if str[0:len(token)] == token:
        return True, str[len(token):]
    else:
        return False, str

def processgroup(token,str):
    print(token)
    return run(token,str)


def parseregex(regex):
    reg = [()]
    buf = ""
    ingroup = False
    cutnext = False
    for letter in regex:
        if ingroup or cutnext:
            if letter == ')':
                ingroup = False
                cutnext = True
                buf += letter
            elif cutnext:
                buf += letter
                reg.append(buf)
                buf = ""
                cutnext = False    
            else:
                buf += letter
        else:
            if letter == "*" or letter == "+":
                if(len(buf) > 1): 
                    reg.append(buf[0:-1],'n')
                reg.append((buf[-1],'*'))
                buf = ""
            elif letter == "(":
                ingroup = True
                if(len(buf) > 0):
                    reg.append((buf,'g'))
                buf = letter
            else:
                buf += letter

    if(len(buf) > 0):
        reg.append(buf)
    return reg

if __name__ == "__main__":
    main()