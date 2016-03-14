'''
Loading and dealing with configuration data.
'''

def load_config_file( path ):
    # read default config file
    config = {}
    with open(path,'r') as f:
        for line in f.readlines():
            if line.strip() == '' or line.strip()[0] == '#': # allow comments
                continue
            key,val = line.rstrip('\n').split(',') #... just don't put any commas in the config values, OK?
            try:
                config[key] = int(val)
            except ValueError:
                config[key] = val

    return config


# to be populated later
default_config = {}