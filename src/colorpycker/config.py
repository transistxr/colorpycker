import os, yaml
class configManager():
    def __init__(self):
        for loc in os.environ.get("COLORPYCKER_CONF"), os.path.expanduser("~/colorpycker"), "/etc/colorpycker", os.curdir:
            try: 
                with open(os.path.join(loc,"colorpycker.conf")) as config_file:
                    self.yaml_data = yaml.safe_load(config_file)
            except IOError:
                pass
    
    def readConfig(self):
        return self.yaml_data