""" Define helper functions for the jinja template
"""
import io
import base64


def include_file(file_path, b64=False):
    """ Function to include file contents in Jinja template
         - Modified version taken from MultiQC: https://github.com/ewels/MultiQC/blob/d89ad61ff704db7c24c5ccce522079e633693440/multiqc/multiqc.py
         - GPL-3.0 License
    """
    if b64:
        with io.open(file_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    else:
        with io.open(file_path, "r", encoding="utf-8") as f:
            return f.read()
