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

KNOWNOPS = '*+()'
LOWERALPHABET = 'abcdefghijklmnopqrstuvwxyz'
UPPERALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

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
    if not checkforvalidinput(regex,inputstrs):
        print("Invalid input!")
        return 1
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
        if token[1] == 'n':
            passing, currstr = processtext(token[0],currstr)
        elif token[1] == 's':
            passing, currstr = processstar(token[0],currstr)
        elif token[1] == 'p':
            passing, currstr = processplus(token[0],currstr)
        elif token[1] == 'gs':
            passing, currstr = processgroup(token[0],currstr)
    
    if len(currstr) > 0:
        passing = False
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

#checks if the given text is in the string
def processtext(token,str):
    if str[0:len(token)] == token:
        return True, str[len(token):]
    else:
        return False, str

#def processgroupstar(token,str):
#    str = processstar()

def processgroup(token,str):
    print(token)
    return run(token,str)


def parseregex(regex):
    reg = []
    buf = ""
    groupbuf = False
    groupopp = False
    # n -> no opp
    # s -> star  *
    # p -> plus  +
    # g -> group ()
    for letter in regex:
        #print(letter + ", " + buf + ", " + str(groupbuf) + ", " + str(groupopp))
        if letter == ")":
            groupbuf = False
            groupopp = True
        elif groupbuf:
            buf += letter
        elif letter == "*":
            if groupopp:
                reg.append((buf,'gs'))
            else:
                if len(buf) > 1:
                    reg.append((buf[:-1],'n'))
                reg.append((buf[-1],'s'))
            buf = ""
        elif letter == "+":
            if groupopp:
                reg.append((buf,'gp'))
            else:
                if len(buf) > 1:
                    reg.append((buf[:-1],'n'))
                reg.append((buf[-1],'p'))
            buf = ""
        elif letter == "(":
            groupbuf = True
            reg.append((buf,'n'))
            buf = ""
        else:
            if groupopp:
                reg.append((buf,'n'))
            buf += letter
    
    if len(buf) > 0:
        reg.append((buf,'n'))

    return reg

def checkforvalidinput(regex,inputstrs):
    #first check the regex
    #can have any letter from all three of our alphabets
    pcount = 0
    for letter in regex:
        if letter not in KNOWNOPS and\
            letter not in LOWERALPHABET and\
            letter not in UPPERALPHABET:
            return False
        #also make sure there are an even number of parenthesis
        if letter == ')':
            pcount -=1
        elif letter == '(':
            pcount +=1
        if pcount < 0:
            return False
    if pcount != 0:
        return False

    #then check all of the input strings
    #can only have letters from our 2 alphabets
    for str in inputstrs:
        for letter in str:
            if letter not in LOWERALPHABET and\
                letter not in UPPERALPHABET:

                return False

    return True

if __name__ == "__main__":
    main()