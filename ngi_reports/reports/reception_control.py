#!/usr/bin/env python

""" Module for producing the reception control report
"""

import os

import ngi_reports.reports


class Report(ngi_reports.reports.BaseReport):
    def __init__(self, config, LOG, working_dir, **kwargs):
        self.working_dir = working_dir
        self.config = config
        self.report_dir = 'reports'
        self.report_fn = 'reception_control.html'
        self.project_info = {}
        self.samples_info = {}


    def generate_report_template(self, proj, template):
        self.sample_columns = {'customer_name': 'Sumbitted name',
                               'well_location': 'Well',
                               'concentration': "Conc.<sup>{}</sup> (ng/&micro;L)",
                               'volume_(ul)'  : "Volume<sup>{}</sup> (&micro;L)",
                               'amount_(ng)'  : "Amount<sup>{}</sup> (ng)",
                               'rin'          : "RIN/RQI<sup>{}</sup>"
                              }

        # TODO: Currently not fetching the method to measure with
        superscript_columns = {'concentration':  "<strong>{superscript}. Concentration:</strong> As measured by the {method}.",
                                    'volume_(ul)'  :  "<strong>{superscript}. Volume:</strong> As measured by the {method}.",
                                    'amount_(ng)'  :  "<strong>{superscript}. Amount:</strong> As measured by the {method}.",
                                    'rin'          :  "<strong>{superscript}. RIN/RQI:</strong> As measured by the {method}."}

        # Used to keep track of which columns are undefined for all samples
        # e.g. rin for DNA projects.
        undefined_columns = self.sample_columns.copy()

        for sample_id, sample_d in sorted(test_proj['samples'].items(), key=lambda t: t[0]):
            status = sample_d['initial_qc']['initial_qc_status']
            self.samples_info[status][sample_id] = {}
            for key, val in sample_d['initial_qc'].items():
                self.samples_info[status][sample_id][key] = self.format_value(val, key)
                undefined_columns.pop(key, None)
            self.samples_info[status][sample_id]['well_location'] = sample_d['well_location']
            undefined_columns.pop('well_location', None)
            self.samples_info[status][sample_id]['customer_name'] = sample_d['customer_name']
            undefined_columns.pop('customer_name', None)

        # Don't show columns which are undefined for all samples
        for column in undefined_columns.keys():
            del self.sample_columns[column]

        superscript = 1
        self.table_captions = []
        for column in superscript_columns.keys():
            if column in self.sample_columns:
                self.sample_columns[column] = self.sample_columns[column].format(superscript)
                # TODO: Add the actual method here instead of this dummy value
                self.table_captions.append(superscript_columns[column].format(
                                                            superscript=superscript,
                                                            method="Quant-iT RNA BR assay"
                                                        ))
                superscript += 1


        self.project_info['NR samples'] = len(self.samples_info['FAILED']) \
                                            + len(self.samples_info['PASSED'])

    def format_value(self, value, type):
        if type in ['concentration', 'volume_(ul)', 'amount_(ng)', 'rin']:
            return round(value, 2)
        return value

    def parse_template(self, template):
        # Make the file basename
        output_bn = os.path.realpath(os.path.join(self.working_dir, self.report_dir, self.report_fn))

        # Parse the template
        html = template.render(project=self.project_info,
                               samples=self.samples_info,
                               sample_columns=self.sample_columns,
                               table_captions=self.table_captions,
                               meta=self.meta)
        return output_bn, html
