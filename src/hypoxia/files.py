from .result import Ok, Err


def open_file(file, *args, **kwargs):
    try:
        return Ok(open(file, *args, **kwargs))
    except Exception as e:
        return Err(e)


class File:
    def __init__(self, file, *args, **kwargs):
        self.file = file
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self._file = open_file(self.file, *self.args, **self.kwargs)

        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.map(lambda f: f.close())
