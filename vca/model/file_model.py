class FileModel:
    def __init__(self, input="", output="", cut=None, image_seq=False, force_ext=False, input_fps=0):
        self.input = input
        self.output = output
        self.cut = cut
        self.image_seq = image_seq
        self.force_ext = force_ext
        self.input_fps = input_fps

    @property
    def need_cut(self):
        return self.cut is not None

    def get_input_args(self):
        args = {}
        if self.need_cut:
            cut_to = self.cut[1]
            cut_from = self.cut[0]
            span = cut_to-cut_from
            if cut_from > 0:
                args["ss"] = cut_from
            args["t"] = span

        if self.input_fps > 0:
            args["r"] = self.input_fps

        return args
