
def list2file(alist,filename):
    with open(filename, 'w') as output:
        for row in alist:
            output.write(str(row) + '\n')