#
import os
import sys
programe = 'python'
print('Process calling')
arguments = ['called_process.py']
os.execvp(programe, (programe,) + tuple(arguments))
print('Good bye!!')



