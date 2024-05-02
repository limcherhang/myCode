import subprocess

command = "ls -l"

result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, text=True)

print(result.stdout)