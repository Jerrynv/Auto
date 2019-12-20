def test():    
    sudoPassword = 'test'
    command = '/opt/lampp/lampp stopmysql'
    str = os.system('echo %s|sudo -S %s' % (sudoPassword, command))   
    print str