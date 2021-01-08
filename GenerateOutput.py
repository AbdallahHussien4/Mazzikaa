def GenerateOutput(Notes,f):
    for Note in Notes:
        f.write(str(Note))   
    f.write('\n')          
