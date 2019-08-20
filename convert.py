import glob
import os
import subprocess

def main():
    os.chdir('tex/')
    for file in glob.glob('*.tex'):
        baseName = file[:-4]
        if not os.path.exists('{}.pdf'.format(baseName)):
            subprocess.call(['pdflatex',file])
        if not os.path.exists('{}.png'.format(baseName)):
            print('Creating {}.png'.format(baseName))
            subprocess.call(['pdftoppm','-png','-r','600','{}.pdf'.format(baseName)],stdout=open('{}.png'.format(baseName),'w'))
        os.rename('{}.png'.format(baseName),'../png/{}.png'.format(baseName))
    return 0

if __name__ == '__main__':
    main()
