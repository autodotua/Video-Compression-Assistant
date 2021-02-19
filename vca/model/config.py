from vca.model.output_model import OutputModel
from vca.model.file_list_model import FileListModel
import os
import sys
import jsonpickle
import traceback
import simplejson


_config_file_path = "config.json"
app_dir=None

if getattr(sys, 'frozen', False):
    app_dir=os.path.dirname(sys.executable)
    _config_file_path = os.path.join(app_dir, "config.json")
print("config path is "+_config_file_path)


class Config:
    def __init__(self):

        self.files = []
        self.output_args = OutputModel()
        self.presets=dict()
        self.autosave = True

    def restore(path=_config_file_path):
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    json = f.read()
                    config = jsonpickle.decode(json)
                    return config
            except:
                print(traceback.format_exc())
                return Config()
        else:
            return Config()

    def save(self, path=_config_file_path):
        try:
            json = jsonpickle.encode(self)
            #print("json is "+json)
            with open(path, "w", encoding="utf-8") as f:
                f.write(json)
        except Exception as ex:
            print(traceback.format_exc())
            pass
