import ConfigParser


def get_config(section):
    config = ConfigParser.RawConfigParser()
    config.read('./config.txt')
    options = config.options(section)
    dict = {}
    for option in options:
        try:
            dict[option] = config.get(section, option)
            if dict[option] == -1:
                print "skip: %s" % option
        except:
            print("exception on %s!" % option)
            dict[option] = None
    return dict