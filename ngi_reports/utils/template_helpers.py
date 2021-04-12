""" Define helper functions for the jinja template
"""
import io
import os
import base64


class FileIncluder(object):

    def __init__(self, base_path):
        self.base_path = base_path

    def include_file(self, file_path, b64=False):
        """ Function to include file contents in Jinja template
             - Modified version taken from MultiQC: https://github.com/ewels/MultiQC/blob/d89ad61ff704db7c24c5ccce522079e633693440/multiqc/multiqc.py
             - GPL-3.0 License
        """
        if b64:
            with io.open(os.path.join(self.base_path, file_path), "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        else:
            with io.open(os.path.join(self.base_path, file_path), "r", encoding="utf-8") as f:
                return f.read()
