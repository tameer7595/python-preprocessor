import sys
includes = {}
defines = {}
out = open("output.txt","w")
def putcode(file):
    global out
    global includes
    global defines
    if file not in includes:
        fp = open(file,'r')
        # codefile = fp.read()+'\n'
        # out.write(codefile)
        # includes[file] = file
        #
        newfile = ""
        linesfile = fp.readlines()

        for line in linesfile:
            splitline = line.split()
            if line.startswith("#define"):
                defines[splitline[1]] = splitline[2]
            else:
                # check if #define in line and replace it
                if bool(defines):
                    for word in splitline:
                        if word in defines:
                            splitline[splitline.index(word)] = defines[word]
                    newfile += '\n'
                    newfile += " ".join(splitline)

        out.write(newfile)
        includes[file] = file # add file name to includes dictionary

def openAllInclude(file):

    with open(file, 'r') as fp:
        for line in fp:
            if "#include" in line:
                l1 = line.split()
                if l1[1][0] == '"':
                    fileToInclude = l1[1][1:-1]
                    if fileToInclude not in includes:
                        openAllInclude(fileToInclude)
            else:
                if line != '\n':
                    putcode(file)
                    return

def runfiles():
    for arg in sys.argv[1:]:
        if arg not in includes:
            with open(arg,'r') as fp:
                for line in fp:
                    if "#include" in line:
                        l1 = line.split()
                        if l1[1][0] == '"':
                            fileToInclude = l1[1][1:-1]
                            openAllInclude(fileToInclude)
                fp.seek(0,0)
    putcode(arg)

if __name__ == '__main__':
    runfiles()
    out.close()