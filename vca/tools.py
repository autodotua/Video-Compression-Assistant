import os
def get_unique_file_name(path):
    if not os.path.isfile(path):
        return path
    name,ext=os.path.splitext(path)
    index=1
    while(os.path.isfile(name+"_"+str(index)+ext)):
        index+=1
    return name+"_"+str(index)+ext
    #return name+"_"+str(index)+ext