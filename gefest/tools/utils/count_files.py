import os
#function that work little like a "grep"
#need to place 'path', where u search something
#and 'like' is string - part of name files, that u need to colculate
def count_files(path = '.',like = None):
    ls = os.listdir(path=path)
    lenght = 0
    for i in ls:
        if like in i:
            lenght += 1
    return lenght