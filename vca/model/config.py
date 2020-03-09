from vca.model.output_model import OutputModel
from vca.model.file_list_model import FileListModel
import os
import jsonpickle


_config_file_path = "config.json"


class Config:
    def __init__(self):

        self.files = []
        self.output_args = OutputModel()
        self.autosave = True

    def restore(path=_config_file_path):
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8") as f:
                    json = f.read()
                    config = jsonpickle.decode(json)
                    return config
            except:
                return Config()
        else:
            return Config()

    def save(self,path=_config_file_path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                json = jsonpickle.encode(self)
                f.write(json)
        except Exception as ex:
            pass
