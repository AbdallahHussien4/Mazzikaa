def GenerateOutput(Notes, f, last):
    for Note in Notes:
        f.write(str(Note))
        if not Note.inChord():
            f.write(' ')
    if last:
        f.write(']\n')
    else:
        f.write('],\n')  
