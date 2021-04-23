---
title: Project Report
subtitle: {{ project.ngi_name }}_project_summary
date: {{ report_info.report_date }}
support_email: {{ report_info.support_email }}
---

# Project Information

User Project Name
:   {{ project.user_ID }}

NGI Project Name
:   {{ project.ngi_name }}

NGI Project ID
:   {{ project.ngi_id }}

{% if project.ngi_facility -%}
NGI Facility
:   {{ project.ngi_facility }}
{%- endif %}

User Contact
:   [{{ project.contact }}](mailto:{{ project.contact }})

NGI Application Type
:   {{ project.application }} _({% if project.best_practice %}including best practice analysis{% else %}no best practice analysis{% endif %})_

{% if project.num_samples -%}
Submitted samples
:   {{ project.num_samples }} sample{% if project.num_samples > 1 %}s{% endif %}
{%- endif %}

{% if project.num_lanes -%}
Ordered lanes
:   {{ project.num_lanes }} lane{% if project.num_lanes > 1 %}s{% endif %}
{%- endif %}

Order Dates
:   {{ report_info.dates }}

{% if project.reference.genome -%}
Reference Genome
:   {% if project.reference.organism -%}{{ project.reference.organism}} - {% endif %}{{ project.reference.genome }}
{%- endif %}

Report generated by
:   {{ report_info.signature }}, {{ report_info.report_date }}

[swedac]

# Methods

{% if project.library_construction -%}
### Library construction
{{ project.library_construction }}
{%- endif %}

{% if report_info.sequencing_methods -%}
### Sequencing
{{ report_info.sequencing_methods }}
{%- endif %}

### Data Flow
Raw sequencing data is demultiplexed and converted to FastQ on site before
being transferred securely to [UPPMAX](http://www.uppmax.uu.se/) for delivery.

### Data Processing
To ensure that all sequenced data meets our guarantee of data quality and quantity,
a number of standardised bioinformatics quality control checks are performed before
delivery. These include checking the yield, sequence read quality and cross-sample contamination.

### Accredited workflow

Library preparation
:   {{ report_info.accredit.library_preparation }}

Sequencing
:   {{ report_info.accredit.sequencing }}

Data Processing
:   {{ report_info.accredit.data_processing }}

Data Analysis
:   {{ report_info.accredit.data_analysis }}

# Sample Information
{% if not project.samples %}
No sample information to be displayed.
{% else %}
NGI ID | User ID | {{ project.samples_unit }} | >=Q30(%)
-------|---------|--------|----------
{% for sample in project.samples.values()|sort(attribute='ngi_id') -%}
{{ sample.ngi_id }} | `{{ sample.customer_name }}` | {{ sample.total_reads }} | {{ sample.qscore }}
{% endfor %}

Below you can find an explanation of the header column used in the table.

{{ tables.sample_info }}
{% endif %}


# Library Information
{% if not project.samples %}
No library information to be displayed.
{% else %}
NGI ID | Index | Lib Prep | Avg. FS | Lib QC
-------|-------|----------|---------|--------
{% for sample in project.samples.values()|sort(attribute='ngi_id') -%}
{% if sample.preps -%}
{% for prep in sample.preps.values() -%}
{{ sample.ngi_id }} | `{{ prep.barcode }}` | {{ prep.label }} | {{ prep.avg_size }} | {{ prep.qc_status }}
{% endfor -%}
{% endif -%}
{%- endfor %}

Below you can find an explanation of the header column used in the table.

{{ tables.library_info }}
{% endif %}


# Lanes Information
{% if project.missing_fc %}
No lanes information to be displayed.
{% else %}
Date | Flowcell | Lane | Clusters(M) | PhiX | >=Q30(%) | Method
-----|----------|------|-------------|------|----------|--------
{% for fc in project.flowcells.values()|sort(attribute='date') -%}
{% for lane in fc.lanes.values() -%}
{{ fc.date }} | `{{ fc.name }}` | {{ lane.id }} | {{ lane.cluster }} | {{ lane.phix }} | {{ lane.avg_qval }} | {{ fc.seq_meth }}
{% endfor -%}
{%- endfor %}

Below you can find an explanation of the header column used in the table.

{{ tables.lanes_info }}
{% endif %}

{% if project.aborted_samples %}
# Aborted/Not Sequenced samples

NGI ID | User ID | Status
-------|---------|-------
{% for sample, info in project.aborted_samples.items() -%}
{{ sample }} | {{ info.user_id }} | {{ info.status }}
{% endfor -%}
{% endif %}

# General Information

## Samples and/or libraries that have failed reception control QC

In cases where samples and/or libraries have failed the QC, the user is always consulted regarding how to proceed. If the user wishes to proceed to sequence the failed samples and/or libraries, NGI bears no responsibility regarding the quality and number of reads of the sequenced sample data.

{% if not project.skip_fastq -%}
## Naming conventions

The data is delivered in FastQ format using Illumina 1.8 quality scores.
There will be one file for the forward reads and one file for the
reverse reads (if the run was a paired-end run).

The naming of the files follow the convention:

```
[NGI-NAME]_[BCL-CONVERSION-ID]_[LANE]_[READ]_[VOLUME].fastq.gz
```

* _NGI-NAME:_ Internal NGI sample indentifier
* _BCL-CONVERSION-ID:_ Indentifier set by bcl2fastq tool while demultiplexing
* _LANE:_ Sequencing lane that the file originates from
* _READ:_ Forward(1) or reverse(2) read indentifier
* _VOLUME:_ Volume index when file is large enough to be split into volumes
{%- endif %}


{% if project.cluster == 'grus' -%}
## Data access at UPPMAX

Data from the sequencing have been be uploaded to the UPPNEX (UPPMAX Next
Generation sequence Cluster Storage, [uppmax.uu.se](http://www.uppmax.uu.se)) called **GRUS**. More details can be found on the following links

- [NGI data delivery note](https://ngisweden.scilifelab.se/info/Data%20delivery)
- [UPPMAX GRUS user guide](https://www.uppmax.uu.se/support/user-guides/grus-user-guide/)

{%- endif %}

## Acknowledgements

Services provided by NGI must be acknowledged in all scientific dissemination activities,
such as publications, presentations, posters, etc., using the following statement:

> The authors acknowledge support from the National Genomics Infrastructure in {% if project.ngi_facility -%} {{ project.ngi_facility }} {%- endif %}
> funded by Science for Life Laboratory, the Knut and Alice Wallenberg Foundation and the Swedish Research Council,
> and SNIC/Uppsala Multidisciplinary Center for Advanced Computational Science for assistance with massively parallel sequencing
> and access to the UPPMAX computational infrastructure

This acknowledgement is used for reporting purposes by the NGI and is critical for the future funding of the facility.

# Further Help
If you have any queries, please get in touch at
[{{ report_info.support_email }}](mailto:{{ report_info.support_email }}).