import os
import django
import sys
import xml.sax

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mitagger.settings")


def mainFunc():
    #analyse code here

if __name__ == '__main__':
    django.setup()
    mainFunc()