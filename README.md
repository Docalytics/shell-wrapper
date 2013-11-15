shell-wrapper
=============

shell-wrapper is a base class and template commands to wrap interactions with the shell.

When invoking shell commands there are a variety of concerns to deal with. Command line flags might not be overly
descriptive about what they do. In many cases there are rules for which arguments may be called together, and it is best
if these rules are evaluated before getting to the actual shell command so that more descriptive errors can be given.
Often, input and output files must be managed and properly cleaned up even in the event of failure. It's possible that
the name of the executable of interest may have different names on different operating system distributions.

shell-wrapper attempts to abstract these challenges away by providing a base class that can be extended for specific
shell commands. By providing some simple details about possible names of the command and how your arguments to the
execute method map to command line arguments, you can cleanly wrap your shell commands in a Python class that makes
the rest of your code much more readable.

Example excuting a shell command:

```python
with Pdf2HtmlExShellCommand('foo.pdf',
                            resolution_dpi=72,
                            split_pages=True,
                            page_file_format='page%d.html') as cmd:
    if not cmd.execute():
        # Flag that it didn't work
        return False

    # The shell command puts output in a temporary directory and cleans up after you leave the block
    for html_file in cmd.page_html_files:
        # Do something
```