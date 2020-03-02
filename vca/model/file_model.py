class FileModel:
    def __init__(self, input="", output="", cut=None, image_seq=False, force_ext=False, input_fps=0):
        self._input = input
        self._output = output
        self._cut = cut
        self._image_seq = image_seq
        self._force_ext = force_ext
        self._input_fps = input_fps

    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, value):
        self._input = value

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, value):
        self._output = value

    @property
    def cut(self):
        return self._cut

    @property
    def need_cut(self):
        return self._cut is not None

    @cut.setter
    def cut(self, value):
        if not isinstance(value, list) and len(value) != 2:
            raise ValueError('必须是一个含2个元素的列表')
        _cut = value

    @property
    def image_seq(self):
        return self._image_seq

    @image_seq.setter
    def image_seq(self, value):
        self._image_seq = value

    @property
    def force_ext(self):
        return self._force_ext

    @force_ext.setter
    def force_ext(self, value):
        self._force_ext = value

    @property
    def input_fps(self):
        return self._input_fps

    @input_fps.setter
    def input_fps(self, value):
        self._input_fps = value

    def get_input_args(self):
        args = {}
        if self.need_cut:
            cut_to = self.cut[1]
            cut_from = self.cut[0]
            span = cut_to-cut_from
            if cut_from > 0:
                args["ss"] = cut_from
            args["t"] = span

        if self.input_fps>0:
            args["r"] = self.input_fps

        return args
