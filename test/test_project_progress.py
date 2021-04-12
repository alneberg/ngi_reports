import unittest
from unittest import mock
import os
import json

from ngi_reports.reports.project_progress import Report
from ngi_reports.utils.entities import Project
from ngi_reports.log import loggers

LOG = loggers.minimal_logger('NGI Reports')


def mock_statusdb_get_project_no_samples(key, use_id_view=False):
    """Mock project without samples from statusdb

    """
    json_data = mock_statusdb_get_entry(key, use_id_view=use_id_view)

    if key == 'P999':
        json_data.pop('samples')

    return json_data

def mock_statusdb_get_entry(key, use_id_view=False):
    """Mock values for documents from statusdb

    returns json files from the directory 'tests/data/statusdb/'
    """
    json_file = None
    if key == '190828_000000000-J88MX':
        json_file = 'miseq_flowcell_1.json'
    elif key == '190824_000000000-J932Z':
        json_file = 'miseq_flowcell_2.json'
    elif key == 'P999':
        json_file = 'miseq_project.json'

    if json_file is None:
        # Mimicking the .get method of .get_entry
        return None

    with open(os.path.join('data/statusdb/', json_file)) as data:
        return json.loads(data.read())


def mock_statusdb_flowcell():
    project_flowcells = {}

    for flowcell_file in ['miseq_flowcell_1.json', 'miseq_flowcell_2.json']:
        with open(os.path.join('data/statusdb/', flowcell_file)) as flowcell_data:
            fc = json.loads(flowcell_data.read())
            fc_date, fc_name = fc['name'].split('_')
            project_flowcells[fc_name] = {'name': fc_name, 'run_name': fc['name'], 'date': fc_date, 'db': 'x_flowcells'}

    return project_flowcells


@mock.patch('ngi_reports.utils.entities.statusdb.couchdb.Server')
@mock.patch('ngi_reports.utils.entities.statusdb.statusdb_connection.get_project_flowcell')
@mock.patch('ngi_reports.utils.entities.statusdb.statusdb_connection.get_entry')
@mock.patch('ngi_reports.reports.project_progress.Report._render_template')
class TestProjectProgress(unittest.TestCase):

    def test_basic(self, mock_renderer, get_entry, get_project_fc, mock_server):
        '''Asserts the report generation goes through to the rendering without exceptions'''
        LOG = mock.Mock()
        get_entry.side_effect = mock_statusdb_get_entry
        get_project_fc.return_value = mock_statusdb_flowcell()
        report = Report(LOG, os.getcwd())

        small_test_project = Project()
        small_test_project.populate(LOG, {}, "P999", exclude_fc=[])

        report.generate_report(small_test_project, None, 'name@example.com')
        assert mock_renderer.called

    def test_missing_project(self, mock_renderer, get_entry, get_project_fc, mock_server):
        '''Asserts SystemExit is raised if project is not found in database'''
        LOG = mock.Mock()
        get_entry.side_effect = mock_statusdb_get_entry
        get_project_fc.return_value = mock_statusdb_flowcell()

        small_test_project = Project()
        with self.assertRaises(SystemExit):
            small_test_project.populate(LOG, {}, "P998", exclude_fc=[])

    def test_no_samples(self, mock_renderer, get_entry, get_project_fc, mock_server):
        '''Asserts the report generation goes through to the rendering without exceptions
        even though no samples exists'''
        LOG = mock.Mock()
        get_entry.side_effect = mock_statusdb_get_project_no_samples
        get_project_fc.return_value = mock_statusdb_flowcell()
        report = Report(LOG, os.getcwd())

        small_test_project = Project()
        small_test_project.populate(LOG, {}, "P999", exclude_fc=[])

        report.generate_report(small_test_project, None, 'name@example.com')
        assert mock_renderer.called
