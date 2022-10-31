import os


class FsRepository:
    def __init__(self, fs_root: str, extension: str):
        self.fs_root = fs_root
        self.extension = extension

    def list(self):
        result = []

        for (dir_path, dir_names, file_names) in os.walk(self.fs_root):
            for fn in file_names:
                if fn.endswith(self.extension):
                    result.append(os.path.join(dir_path, fn))

        return result

    def remove(self, path: str):
        """Remove file and empty folders."""
        assert os.path.exists(path)

        os.remove(path)

        rel_path = os.path.relpath(path, self.fs_root)

        paths = rel_path.split(os.sep)
        for i in range(len(paths) - 1, 0, -1):
            dir_path = os.path.join(self.fs_root, os.sep.join(paths[:i]))

            if os.path.isdir(dir_path):
                with os.scandir(dir_path) as it:
                    if any(it):
                        break

                os.rmdir(dir_path)
