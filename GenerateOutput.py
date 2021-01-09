def GenerateOutput(Notes, f, last):
    for Note in Notes:
        f.write(str(Note))  
    if last:
        f.write(']\n')
    else:
        f.write('],\n')  
