

def edit_txt(fname, trainfl, dest_dir):

    f = open(trainfl, 'a')
    f.write(dest_dir+fname + ".wav" + '\n')
    f.close()

def del_txt(trainf1):
    open(trainf1, 'w').close()
