__author__ = 'rmorlok'
import os
import tempfile
import shutil
import subprocess


class ConfigurationException(Exception):
    pass


class ArgumentException(Exception):
    pass


class DummyLogger(object):
    def debug(self, **vargs):
        pass

    def info(self, **vargs):
        pass

    def warning(self, **vargs):
        pass

    def error(self, **vargs):
        pass

    def critical(self, **vargs):
        pass

    def exception(self, **vargs):
        pass

    def log(self, **vargs):
        pass


class BaseShellCommand(object):

    def __init__(self, possible_command_names, logger=None):
        """
        Initializes a shell command.

        :param possible_command_names:
          An array of strings for possible names this shell command may go by in the system path.
        """
        self._temp_dir = None
        self.__class__._possible_command_names = possible_command_names
        self.__class__._full_path_to_command = None
        self.logger = logger or DummyLogger()

    @property
    def full_path_to_command(self):
        """
        Retrieve the fully qualified path to this command.
        """

        if self.__class__._full_path_to_command:
            return self.__class__._full_path_to_command

        # Attempt to locate the command in the system path via the 'which' command
        for cmd_name in self.__class__._possible_command_names:
            cmd_path = os.popen("which %s" % cmd_name).read().strip()

            if cmd_path:
                self.__class__._full_path_to_command = cmd_path

        if not self.__class__._full_path_to_command:
            raise ConfigurationException("Could not locate %s executable" % self.__class__.__name__)

        return self.__class__._full_path_to_command

    @property
    def temp_directory(self):
        """
        Gets the temporary directory path that can be used with this command.
        """
        self.logger.debug("Creating temporary directory")
        self._temp_dir = self._temp_dir or tempfile.mkdtemp(prefix=self.__class__.__name__)
        self.logger.debug("Created temporary directory '%s'" % self._temp_dir)
        return self._temp_dir

    def _execute_command(self, args):
        """
        Executes the command as represented by an array of arguments. Handles logging etc.

        :param args:
         Array of arguments to execute for the command.
        """
        cmd = [self.full_path_to_command]
        cmd.extend(args)
        cmd = map(lambda x: unicode(x), cmd)

        self.logger.debug('Executing command: ' + ' '.join(cmd))

        # This command has annoying output
        with open(os.devnull, "w") as fnull:
            return_code = subprocess.call(cmd, stderr=fnull, stdout=fnull)
            (self.logger.debug if return_code == 0 else self.logger.error)(' '.join(cmd) + " returned with code: " + str(return_code))

            return return_code == 0

    def cleanup(self):
        """
        Cleanup any resources used by this command.
        """
        if self._temp_dir:
            self.logger.debug("Deleting temporary directory '%s'" % self._temp_dir)
            shutil.rmtree(path=self._temp_dir, ignore_errors=True)
            self._temp_dir = None

    def __enter__(self):
        """
        Make this command usable via the "with" statement.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Cleanup resources used by this command.
        """
        self.cleanup()


# Define exports
from libreoffice import LibreOfficeShellCommand
from mupdf import MuDrawShellCommand
from optipng import OptiPNGShellCommand
from pdf2htmlex import Pdf2HtmlExShellCommand

__all__ = [BaseShellCommand, ConfigurationException, ArgumentException, LibreOfficeShellCommand,
           MuDrawShellCommand, OptiPNGShellCommand, Pdf2HtmlExShellCommand]
