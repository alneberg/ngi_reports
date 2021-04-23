#!/usr/bin/env python

""" Module for producing the project progress report
"""

import os
from datetime import datetime

import ngi_reports.reports

class TableField():
    """Convenience class to represent a table field"""
    def __init__(self, display_title, explanation, visible_by_default, custom_classes=''):
        self.display_title = display_title
        self.explanation = explanation
        self.visible_by_default = visible_by_default
        self.custom_classes = custom_classes

class Report(ngi_reports.reports.BaseReport):
    def __init__(self, LOG, working_dir, **kwargs):
        self.working_dir = working_dir
        self.report_dir = 'reports'
        self.report_fn = 'project_progress.html'

        self.meta = {}
        self.meta['title'] = 'Project Progress'
        self.meta['date'] = datetime.now().strftime("%Y-%m-%d")



        self.meta['RC_columns'] = {
                'customer_name': TableField('Submitted ID', 'Sample ID submitted by user', True),
                'well_location': TableField('Well Location', '', True),
                'user_volume': TableField('User Volume', '', False),
                'sample_type': TableField('Sample Type', '', False),
                'sample_buffer': TableField('Sample Buffer', '', False),
                'user_rin': TableField('User RIN', '', False),
                'user_concentration': TableField('User Conc.', '', False),
                'user_concentration_method': TableField('User Conc. Method', '', False),
                'user_amount': TableField('User Amount (&micro;g)', '', False),
                'initial_qc_concentration': TableField('Initial QC concentration', '', False),
                'initial_qc_conc_units': TableField('Concentration Units', '', False),
                'initial_qc_volume_ul': TableField('Volume (&micro;l)', '', True),
                'initial_qc_amount_ng': TableField('Amount (ng)', '', True),
                'initial_qc_rin': TableField('RIN', '', False),
                'initial_qc_status': TableField('Initial QC Status', '', True),
                'initial_qc_start_date': TableField('Initial QC Start Date', '', False, custom_classes='text_nowrap'),
                'initial_qc_finish_date': TableField('Initial QC Finish Date', '', True, custom_classes='text_nowrap')
            }
        self.meta['nr_samples'] = 0
        self.meta['RC_passed'] = 0
        self.meta['RC_status_width'] = 0
        self.meta['RC_status_column'] = 'initial_qc_status'

    def generate_report(self, proj, template, support_email):
        self.project = proj
        self.meta['subtitle'] = "{}_project_progress".format(self.project.ngi_name)
        self.meta['support_email'] = support_email

        # Figure out nr of passed samples for each step
        self.meta['nr_samples'] = len(self.project.samples)
        for sample_id, sample in self.project.samples.items():
            if sample.initial_qc_status == 'PASSED':
                self.meta['RC_passed'] += 1

        if self.meta['nr_samples'] != 0:
            self.meta['RC_progress_width'] = round(100 * self.meta['RC_passed'] / float(self.meta['nr_samples']))
        else:
            self.meta['RC_progress_width'] = 0

        if self.meta['RC_progress_width'] == 100:
            self.meta['RC_progress_class'] = 'bg-success'
        else:
            self.meta['RC_progress_class'] = ''

        # Make the file basename
        output_bn = os.path.realpath(os.path.join(self.working_dir, self.report_dir, self.report_fn))

        # Parse and render the template
        html = self._render_template(template, self.project, self.meta)

        return output_bn, html

    def _render_template(self, template, project, meta):
        """Convenience function to simplify mocking in tests"""
        return template.render(project=project, meta=meta)
