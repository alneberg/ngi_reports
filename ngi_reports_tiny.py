#!/usr/bin/env python

""" This is the entry point for ngi_reports.
"""

from __future__ import print_function

import argparse
import jinja2
import json
import os
import markdown
from datetime import datetime

from ngi_reports.log import loggers
from ngi_reports.utils import config as report_config
from ngi_reports.utils import statusdb

LOG = loggers.minimal_logger('NGI Reports')

## CONSTANTS
# create choices for report type based on available report template
ALLOWED_REPORT_TYPES = ["project_summary", "reception_control"]


class Report():
    def __init__(self, config, LOG, working_dir, **kwargs):
        self.working_dir = working_dir
        self.config = config
        self.report_dir = 'reports'
        self.report_fn = 'reception_control.html'
        self.project_info = {}
        self.samples_info = {}


    def mock_values(self):
        self.project_info["Sample type"] = "Total RNA"
        self.project_info["Library method"] = "TruSeq Stranded Total RNA"
        self.project_info["Open date"] = "2019-01-14"
        self.project_info["Project name"] = "P.Projectsson_20_01"

        self.meta = {}
        self.meta['title'] = 'Reception Control'
        self.meta['subtitle'] = "{}_reception_control".format(self.project_info['Project name'])
        self.meta['date'] = datetime.now().strftime("%Y-%m-%d")
        self.meta['support_email'] = self.config.get('ngi_reports', 'support_email')

        pcon = statusdb.ProjectSummaryConnection()
        #test_proj = pcon.db.get('4fc14f5f7ec25d620b1ad584a429259d')
        #test_proj = pcon.db.get('91666263d86b8febf033226606010f89')
        test_proj = pcon.db.get('695d8af0948c6c68b33747f21306dbc5')
        self.samples_info['FAILED'] = {}
        self.samples_info['PASSED'] = {}

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


def make_reports(report_type, working_dir=os.getcwd(), config_file=None, **kwargs):

    # Setup
    LOG.info('Report type: {}'.format(report_type))

    # use default config or override it if file is specified
    config = report_config.load_config(config_file)

    # Make the report object
    report = Report(config, LOG, working_dir, **kwargs)
    report.mock_values()

    # Work out all of the directory names
    output_dir = os.path.realpath(os.path.join(working_dir, report.report_dir))
    reports_dir = os.path.realpath(os.path.join(os.path.dirname(__file__), 'data', 'report_templates'))

    # Create the directory if we don't already have it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Print the markdown output file
    # Load the Jinja2 template
    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(reports_dir))
        template = env.get_template('{}.html'.format(report_type))
    except:
        LOG.error('Could not load the Jinja report template')
        raise

    # Change to the reports directory
    old_cwd = os.getcwd()
    os.chdir(report.report_dir)

    # Get parsed markdown and print to file(s)
    LOG.debug('Converting markdown to HTML...')
    output_bn, content = report.parse_template(template)

    with open('{}'.format(output_bn), 'w', encoding='utf-8') as fh:
        print(content, file=fh)


def main():
    parser = argparse.ArgumentParser("Make an NGI Report")
    parser.add_argument('report_type', choices=ALLOWED_REPORT_TYPES, metavar='<report type>',
        help="Type of report to generate. Choose from: {}".format(', '.join(ALLOWED_REPORT_TYPES)))
    parser.add_argument("-d", "--dir", dest="working_dir", default=os.getcwd(),
        help="Working Directory. Default: cwd when script is executed.")
    parser.add_argument('-c', '--config_file', default=None, action="store", help="Configuration file to use instead of default (~/.ngi_config/ngi_reports.conf)")
    parser.add_argument('-p', '--project', default=None, action="store", help="Project name to generate 'project_summary' report")

    kwargs = vars(parser.parse_args())

    make_reports(**kwargs)

# calling main method to generate report
if __name__ == "__main__":
    main()
