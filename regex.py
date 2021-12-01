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
#               * + () |
#       - outputs each string and whether it is accepted to the command line
#
# known bugs:
#   -a character followed by a star and then the same character after it will
#       most likely return false
#       A way around this is to refrain from this/rework your regex to make it
#       have the stars as far back as possible
###

KNOWNOPS = '*+()|'
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
    
    if not checkforvalidinput(regex,inputstrs):
        print("Invalid input!")
        return 1
    
    # running our regex against all of the strings
    for input in inputstrs:
        #run each input on the regex
        #print the output
        outcome, rtxt = run(regex,input)
        if len(rtxt) > 0:
            outcome = False
        if outcome:
            # TODO: adjust the print statements
            print("\n"+input+"\tis in the regex:", regex)
        else:
            print("\n"+input+"\tis not the regex:", regex)
    
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
    c = 0
    shouldpass = False
    for token in parsedreg:
        if shouldpass:
            continue
        c += 1
        #print(token)
        #print(currstr)
        if token[1] == 'n':
            tpassing, currstr = processtext(token[0],currstr)
        elif token[1] == 's':
            tpassing, currstr = processstar(token[0],currstr)
        elif token[1] == 'p':
            tpassing, currstr = processplus(token[0],currstr)
        elif token[1] == 'gs':
            tpassing, currstr = processgroupstar(token[0],currstr)
        elif token[1] == 'gp':
            tpassing, currstr = processgroupplus(token[0],currstr)
        elif token[1] == 'gos':
            tpassing, currstr = processorstar( currstr, token[0])
        elif token[1] == 'gop':
            tpassing, currstr = processorplus( token[0],currstr)
        elif token[1] == 'o':
            tpassing, currstr= processor(passing, parsedreg[c:],currstr)
            shouldpass = True
            
        elif token[1] == 'go':
            tpassing, currstr = processgroupor(token[0],currstr)

        if (not passing) or (not tpassing):
            passing = False


    return passing, currstr

##
#processorstar
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processorstar(str,token):
    prevoutputlen = len(str) + 1
    outputlen = len(str)
    output = str
    while prevoutputlen != outputlen :
        outcome, output = run(token,output)
        prevoutputlen = outputlen
        outputlen = len(output)
    return True, output
##
#processorplus
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processorplus(token, str):
    c = 0
    prevoutputlen = len(str) + 1
    outputlen = len(str)
    output = str
    while prevoutputlen != outputlen :
        c += 1
        outcome, output = run(token,output)
        prevoutputlen = outputlen
        outputlen = len(output)
    return c > 1, output

##
#processgroupplus
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processgroupplus(token,str):
    print(token)
    c = 0
    prevoutputlen = len(str) + 1
    outputlen = len(str)
    output = str
    while prevoutputlen != outputlen :
        c += 1
        outcome, output = run(token,output)
        prevoutputlen = outputlen
        outputlen = len(output)
    return c > 1, output

##
#processgroupor
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processgroupor(token,str):
    return run(token, str)

##
#processstar
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processstar(token,str):
    while str[0:len(token)] == token:
        str = str[len(token):]
    return True, str

##
#processplus
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processplus(token,str):
    once = False
    while str[0:len(token)] == token:
        str = str[len(token):]
        once = True
    return once, str

##
#processor
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processor(passing, regex, str):
    print(passing, regex,str,"asd")
    secondpassing, stext = run(regex,str)
    if passing and secondpassing:
        if len(str) > len(stext):
            return True, stext
        else:
            return True, str
    elif passing:
        return True, str
    elif secondpassing:
        return True, stext
    else:
        return False, str

#checks if the given text is at the beginning of the string
def processtext(token,str):
    if str[0:len(token)] == token:
        return True, str[len(token):]
    else:
        return False, str


##
#processgroupstar
#
#description: processes a string given the specified token
#
#Parameters
#   -str    the string to process
#   -token  the token to use
#
#return:
#   -the boolean output of whether or not it was able to be processed
#   -the remaining string to be processed in the next token
def processgroupstar(token,str):
    prevoutputlen = len(str) + 1
    outputlen = len(str)
    output = str
    while prevoutputlen != outputlen :
        outcome, output = run(token,output)
        prevoutputlen = outputlen
        outputlen = len(output)
        
    return True, output


def parseregex(regex):
    if isinstance(regex[0], tuple):
        return regex
    reg = []
    buf = ""
    groupbuf = False
    groupopp = False
    seenor = False
    pcount = 0
    # n -> no opp
    # s -> star  *
    # p -> plus  +
    # g -> group ()
    #print("the regex is: " + regex)
    for letter in regex:
        #print(groupopp, seenor)
        #print(letter + ", " + buf + ", " + str(groupbuf) + ", " + str(groupopp))
        if letter == ")" and pcount == 0:
            groupbuf = False
            groupopp = True
        elif groupbuf:
            buf += letter
            if letter == '|':
                seenor = True
            elif letter == '(':
                pcount += 1
            elif letter == ')':
                pcount -= 1
        elif letter == "*":
            if groupopp:
                if seenor:
                    reg.append((buf,'gos'))
                    seenor = False
                else:
                    reg.append((buf,'gs'))
            else:
                if len(buf) > 1:
                    reg.append((buf[:-1],'n'))
                reg.append((buf[-1],'s'))
            buf = ""
        elif letter == "+":
            if groupopp:
                if seenor:
                    reg.append((buf,'gop'))
                    seenor = False
                else:
                    reg.append((buf,'gp'))
            else:
                if len(buf) > 0:
                    reg.append((buf[:-1],'n'))
                reg.append((buf[-1],'p'))
            buf = ""
        elif letter == "(":
            groupbuf = True
            if len(buf) > 0:
                reg.append((buf,'n'))
            buf = ""
        elif letter == "|":
            if len(buf) > 0:
                reg.append((buf,'n'))
                buf = ""
            reg.append((letter,'o'))
        else:
            if groupopp:
                if seenor:
                    reg.append((buf,'go'))
                else:
                    if len(buf) > 0:
                        reg.append((buf,'n'))
                groupopp = False
                buf = ""
            buf += letter
    
    if len(buf) > 0:
        reg.append((buf,'n'))

    print(reg)
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