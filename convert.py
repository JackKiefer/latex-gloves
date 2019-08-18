import glob
import os
import subprocess

def main():
    os.chdir('tex/')
    for file in glob.glob('*.tex'):
        subprocess.call(['pdflatex',file])
    for file in glob.glob('*.pdf'):
        os.rename(file, '../pdf/{}'.format(file))
    os.chdir('../pdf/')
    return 0

if __name__ == '__main__':
    main()


