import os

from shellwrapper import BaseShellCommand, ArgumentException


class Pdf2HtmlExShellCommand(BaseShellCommand):
    """
    Command to convert a PDF to HTML
    """

    def __init__(self,
                 pdf_file,
                 resolution_dpi=None,
                 zoom=None,
                 viewer_file=None,
                 page_file_format="page%02d.html",
                 embed_css=True,
                 embed_javascript=True,
                 embed_font=True,
                 embed_image=True,
                 embed_outline=True,
                 split_pages=False,
                 no_drm=True,
                 fit_width_px=None,
                 fit_height_px=None,
                 first_page=None,
                 last_page=None,
                 css_filename=None,
                 outline_filename=None,
                 data_directory=None,
                 logger=None):

        if not pdf_file:
            raise ArgumentException("Must specify PDF file to process.")

        self._pdf_file = pdf_file
        self._resolution_dpi = resolution_dpi
        self._zoom = zoom
        self._page_file_format = page_file_format
        self._embed_css = embed_css
        self._embed_javascript = embed_javascript
        self._embed_font = embed_font
        self._embed_image = embed_image
        self._embed_outline = embed_outline
        self._split_pages = split_pages
        self._no_drm = no_drm
        self._fit_width_px = fit_width_px
        self._fit_height_px = fit_height_px
        self._first_page = first_page
        self._last_page = last_page
        self._data_directory = data_directory

        self._viewer_file = None
        if viewer_file:
            head, __ = os.path.split(viewer_file)

            if head:
                raise ArgumentException("Cannot include path in output filename")

            self._viewer_file = viewer_file

        self._css_filename = None
        if css_filename:
            head, __ = os.path.split(css_filename)

            if head:
                raise ArgumentException("Cannot include path in css filename")

            self._css_filename = css_filename

        self._outline_filename = None
        if outline_filename:
            head, __ = os.path.split(outline_filename)

            if head:
                raise ArgumentException("Cannot include path in outline filename")

            self._outline_filename = outline_filename

        super(Pdf2HtmlExShellCommand, self).__init__(["pdf2htmlEX"], logger)

    def execute(self):
        """
        Execute the command.
        """
        cmd = []

        if self._zoom:
            cmd.extend(['--zoom', self._zoom])

        if self._resolution_dpi:
            cmd.extend(['--hdpi', str(self._resolution_dpi), '--vdpi', str(self._resolution_dpi)])

        if self._split_pages:
            cmd.extend(['--split-pages', 1])
        else:
            cmd.extend(['--split-pages', 0])

        if self._embed_css:
            cmd.extend(['--embed-css', 1])
        else:
            cmd.extend(['--embed-css', 0])

        if self._embed_javascript:
            cmd.extend(['--embed-javascript', 1])
        else:
            cmd.extend(['--embed-javascript', 0])

        if self._embed_font:
            cmd.extend(['--embed-font', 1])
        else:
            cmd.extend(['--embed-font', 0])

        if self._embed_image:
            cmd.extend(['--embed-image', 1])
        else:
            cmd.extend(['--embed-image', 0])

        if self._embed_outline:
            cmd.extend(['--embed-outline', 1])
        else:
            cmd.extend(['--embed-outline', 0])

        if self._split_pages and self._page_file_format:
            cmd.extend(['--page-filename', self._page_file_format])

        if self._fit_width_px:
            cmd.extend(['--fit-width', str(self._fit_width_px)])

        if self._fit_height_px:
            cmd.extend(['--fit-height', str(self._fit_height_px)])

        if self._first_page:
            cmd.extend(['--first-page', str(self._first_page)])

        if self._last_page:
            cmd.extend(['--last-page', str(self._last_page)])

        if self._css_filename:
            cmd.extend(['--css-filename', self._css_filename])

        if self._outline_filename:
            cmd.extend(['--outline-filename', self._outline_filename])

        if self._data_directory:
            cmd.extend(['--data-dir', self._data_directory])

        cmd.extend(['--dest-dir', self.temp_directory])

        cmd.append(self._pdf_file)

        if self._viewer_file:
            cmd.append(self._viewer_file)

        return self._execute_command(cmd)

    @property
    def viewer_file(self):
        """
        Retrieves the path to the base HTML file for the processed PDF. If all embeds are set to true, this singular
        HTML file will contain all data for the PDF. If not this file will be the one that brings together all the
        different components of the viewer. The name of this file is influenced by the viewer_file property of
        the constructor.
        """
        if self._viewer_file:
            return os.path.join(self.temp_directory, self._viewer_file)

        filename, extension = os.path.splitext(os.path.split(self._pdf_file)[1])
        return os.path.join(self.temp_directory, filename + ".html")

    @property
    def css_files(self):
        """
        Returns the absolute path to the CSS files generated by processing. Will include both the output CSS file for
        the specific PDF (possibly named by css_filename) and the base CSS files generated by the utility. No CSS files
        will exist if embed_css is True, in which case this will generate an empty list.
        """
        return [os.path.join(self.temp_directory, f) for f in os.listdir(self.temp_directory) if f.endswith(".css")]

    @property
    def javascript_files(self):
        """
        Returns the absolute path to the javascript files generated by processing.
        """
        return [os.path.join(self.temp_directory, f) for f in os.listdir(self.temp_directory) if f.endswith(".js")]

    @property
    def font_files(self):
        """
        Returns the absolute path to the font files generated by processing.
        """
        return [os.path.join(self.temp_directory, f) for f in os.listdir(self.temp_directory) if f.endswith(".ttf") or f.endswith(".ttc") or f.endswith(".otf") or f.endswith(".pfb")]

    @property
    def page_html_files(self):
        """
        Retrieves the list of image files generated by this command in sort order.
        """
        if not self._split_pages:
            return None

        extension = "page"

        if self._page_file_format:
            filename, extension = os.path.splitext(self._page_file_format)

        viewer_file_name = os.path.basename(self.viewer_file)

        page_files = [os.path.join(self.temp_directory, f) for f in os.listdir(self.temp_directory) if f.endswith(extension) and f != viewer_file_name]
        page_files.sort()
        return page_files