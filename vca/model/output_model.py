from vca.dicts import *
class OutputModel:
    def __init__(self):
        self.video_filter = OutputModel.VideoFilterModel()
        self.audio_filter = OutputModel.AudioFilterModel()
        self.extra_args=""
        self.manual=False
        self.manual_args=""
        self.output_format=None

    class VideoFilterModel:
        def __init__(self):
            self.encoder = "H.265"
            self.preset = 1
            self.crf = 28
            self.size = None
            self.fps = None
            self.bitrate = None
            self.max_bitrate = None
            self.min_bitrate = None

        def get_filter_args(self):
            args = {}
            args["c:v"] = encoder_infos[self.encoder]["lib"]
            args["preset"] = presets[self.preset]["code"]
            if self.crf is not None:
                args["crf"] = self.crf
                if self.encoder == "VP9" and self.crf==0:
                    args["b:v"] = 0
            if self.size is not None:
                args["s"] = self.size
            if self.bitrate is not None:
                args["b:v"] = str(self.bitrate)+"M"
            if self.max_bitrate  is not None:
                args["maxrate"] = str(self.max_bitrate)+"M"
                args["bufsize"] = str(self.max_bitrate*2)+"M"
            if self.min_bitrate is not None:
                args["minrate"] = str(self.min_bitrate)+"M"
            if self.fps is not None:
                args["r"] = self.fps
            return args

    class AudioFilterModel:
        def __init__(self):
            self.mode="copy"#copy/encode/none/aac
            self.bitrate = 128

        def get_filter_args(self):
            args={}
            if self.mode=="default":
                pass
            elif self.mode=="copy":
                args["c:a"] = "copy"
            elif self.mode=="encode":
                args["b:a"] = str(self.bitrate)+"k"
            elif self.mode=="aac":
                args["c:a"] = "aac"
                args["b:a"] = str(self.bitrate)+"k"
            elif self.mode=='none':
                args["an"] = ""
            return args

    def get_filter_args(self):
        if self.manual:
            return self.manual_args
        args={}
        if self.video_filter:
            args=self.video_filter.get_filter_args()
            
        else:
            args["c:v"] = "copy"

        if self.audio_filter:
            args={**args,**self.audio_filter.get_filter_args()}

        if self.extra_args:
            args[""]=self.extra_args
        return args
