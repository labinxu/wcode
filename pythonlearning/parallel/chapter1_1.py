#
import os
import sys
programe = 'python'
print('Process calling')

os.execvp(programe, (programe,) + tuple(arguments))
