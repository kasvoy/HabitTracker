import sys, subprocess

os = sys.platform

if os == 'win32':
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'test':
        subprocess.run("python -m src.main test", shell = True)
    else:
        subprocess.run("python -m src.main", shell = True)

elif os == 'linux' or os == 'darwin':
    if len(sys.argv) == 2 and sys.argv[1].lower() == 'test':
        subprocess.run("python3 -m src.main test", shell = True)
    else:
        subprocess.run("python3 -m src.main", shell = True)    