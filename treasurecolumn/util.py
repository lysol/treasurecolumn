import os
import ConfigParser

def get_cur_dir():
    return os.path.dirname(os.path.realpath(__file__))

def get_config():
    local_config = get_cur_dir() + '/config.ini'
    config = ConfigParser.ConfigParser()
    config.read([get_cur_dir() + '/config-defaults.ini', 
        os.path.expanduser('~/.treasurecolumn/config.ini'), 
        local_config])
    return config
