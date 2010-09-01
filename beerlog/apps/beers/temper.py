import subprocess as sub

def get_temp():
        p = sub.Popen('temper', stdout=sub.PIPE, stderr=sub.PIPE)
        p.wait()
        temp =  p.stdout.read()
        return temp