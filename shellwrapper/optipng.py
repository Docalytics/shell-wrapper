from shellwrapper import BaseShellCommand

class OptiPNGShellCommand(BaseShellCommand):
    """
    Command to optimize PNG files. Files will be optimized in place.
    """

    def __init__(self, files=None, file=None, optimization_level=2, logger=None):
        if files is None and file is None:
            raise ValueError("Either files or file must be specified")

        if files is not None and file is not None:
            raise ValueError("Can only specify either file or files")

        if files is None:
            self.files = [file]
        else:
            self.files = files

        self.optimization_level = optimization_level

        super(OptiPNGShellCommand, self).__init__(["optipng"], logger)

    def execute(self):
        """
        Execute the command.
        """
        args = [
            "-o", self.optimization_level]

        args = args + self.files

        return self._execute_command(args)