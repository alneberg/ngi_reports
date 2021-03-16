#!/usr/bin/env python

""" Module for producing the project progress report
"""

import os
from datetime import datetime

import ngi_reports.reports

class Report(ngi_reports.reports.BaseReport):
    def __init__(self, LOG, working_dir, **kwargs):
        self.working_dir = working_dir
        self.report_dir = 'reports'
        self.report_fn = 'project_progress.html'

        self.meta = {}
        self.meta['title'] = 'Project Progress'
        self.meta['date'] = datetime.now().strftime("%Y-%m-%d")


    def generate_report(self, proj, template, support_email):
        self.project = proj
        self.meta['subtitle'] = "{}_project_progress".format(self.project.ngi_name)
        self.meta['support_email'] = support_email

        # Make the file basename
        output_bn = os.path.realpath(os.path.join(self.working_dir, self.report_dir, self.report_fn))

        # Parse the template
        html = template.render(project=self.project,
                               meta=self.meta)
        return output_bn, html
