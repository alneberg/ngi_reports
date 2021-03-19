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

        self.meta['RC_columns'] = {
                'customer_name': {'display_title': 'Submitted ID', 'explanation': 'Sample ID submitted by user', 'visible_by_default': True},
                'well_location': {'display_title': 'Well Location', 'explanation': '', 'visible_by_default': True},
                'user_volume': {'display_title': 'User Volume', 'explanation': '', 'visible_by_default': False},
                'sample_type': {'display_title': 'Sample Type', 'explanation': '', 'visible_by_default': False},
                'sample_buffer': {'display_title': 'Sample Buffer', 'explanation': '', 'visible_by_default': False},
                'user_rin': {'display_title': 'User RIN', 'explanation': '', 'visible_by_default': False},
                'user_concentration': {'display_title': 'User Conc.', 'explanation': '', 'visible_by_default': False},
                'user_concentration_method': {'display_title': 'User Conc. Method', 'explanation': '', 'visible_by_default': False},
                'user_amount': {'display_title': 'User Amount (&micro;g)', 'explanation': '', 'visible_by_default': False},
                'initial_qc_concentration': {'display_title': 'Initial QC concentration', 'explanation': '', 'visible_by_default': False},
                'initial_qc_conc_units': {'display_title': 'Concentration Units', 'explanation': '', 'visible_by_default': False},
                'initial_qc_volume_ul': {'display_title': 'Volume (&micro;l)', 'explanation': '', 'visible_by_default': False},
                'initial_qc_amount_ng': {'display_title': 'Amount (ng)', 'explanation': '', 'visible_by_default': False},
                'initial_qc_rin': {'display_title': 'RIN', 'explanation': '', 'visible_by_default': False},
                'initial_qc_status': {'display_title': 'Initial QC Status', 'explanation': '', 'visible_by_default': False},
                'initial_qc_start_date': {'display_title': 'Initial QC Start Date', 'explanation': '', 'custom_classes': 'text_nowrap', 'visible_by_default': False},
                'initial_qc_finish_date': {'display_title': 'Initial QC Finish Date', 'explanation': '', 'custom_classes': 'text_nowrap', 'visible_by_default': False}
            }

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
