**Nigeria Tech Talent Radar**

A Data-Driven Investigation of Technology Industry Skills Demand and Training Alignment in Nigeria

Nigeria Tech Talent Radar

A Data-Driven Investigation of Technology Industry Skills Demand and Training Alignment in Nigeria

**Project Overview**

Nigeria Tech Talent Radar is a data engineering and analytics project designed to investigate the relationship between the skills required by Nigeria's technology industry and the skills being developed through available technology training programmes.

Inspired by remarks made by the CEO of Moniepoint during Platform, the project seeks to examine the extent to which Nigeria's technology talent development efforts align with the actual workforce requirements of the technology industry.

The project adopts a data-driven approach by collecting technology job vacancy information from Nigerian employers and examining the curricula of technology training programmes. Through data collection, processing, skills extraction and analysis, the project aims to identify frequently requested industry skills, assess training programme coverage and highlight potential areas of skills mismatch.

The ultimate goal is to provide insights that can support more relevant technology training, better workforce preparation and improved alignment between talent development and industry needs.

**Background and Problem Statement**

Nigeria's technology sector continues to create opportunities across areas such as software development, data analytics, cybersecurity, cloud computing, product management and other technology-related fields.

However, the availability of technology training programmes does not automatically guarantee that individuals completing these programmes possess the competencies employers require.

The remarks made by the CEO of Moniepoint during Platform raised an important question about the relationship between the skills available in the talent market and the skills required by employers.

This project seeks to investigate that relationship using available job vacancy and training programme data.

Rather than relying solely on assumptions about in-demand skills, Nigeria Tech Talent Radar uses actual job listings and documented training curricula to examine:

The technology roles employers are recruiting for.

The skills and competencies requested in job descriptions.

The technology skills covered by available training programmes.

Areas where training content aligns with industry requirements.

Potential gaps between employer demand and training programme coverage.

**Project Aim**

To develop a data-driven view of Nigeria's technology workforce requirements by analysing job market skill demands and comparing them with the skills covered by available technology training programmes.

Nigeria Tech Talent Radar is a data engineering and analytics project designed to investigate the relationship between the skills required by Nigeria's technology industry and the skills being developed through available technology training programmes.

Inspired by remarks made by the CEO of Moniepoint during Platform, the project seeks to examine the extent to which Nigeria's technology talent development efforts align with the actual workforce requirements of the technology industry.

The project adopts a data-driven approach by collecting technology job vacancy information from Nigerian employers and examining the curricula of technology training programmes. Through data collection, processing, skills extraction and analysis, the project aims to identify frequently requested industry skills, assess training programme coverage and highlight potential areas of skills mismatch.

The ultimate goal is to provide insights that can support more relevant technology training, better workforce preparation and improved alignment between talent development and industry needs.

**Research Questions**

The project seeks to answer the following questions:

What technology roles are Nigerian employers recruiting for?

Which technical and professional skills are most frequently requested in technology job vacancies?

Which technology skills and competencies are covered by existing training programmes?

To what extent do available training programmes align with the skills requested by employers?

Which frequently requested industry skills have limited coverage across the training programmes examined?

What insights can be derived to improve the alignment between technology training and workforce requirements?

**Project Scope**

The project focuses on two major datasets:

A. Technology Job Market Data

This covers job vacancy information collected from selected Nigerian job platforms and company career websites.

Information of interest includes:

Job title

Employer or hiring organisation

Job location

Job function

Industry

Employment type

Job description

Required skills

Date posted

Application information, where available

B. Technology Training Programme Data

This covers information about technology training programmes and their curricula.

Information of interest includes:

Training provider

Programme name

Technology track

Programme duration

Learning format

Modules and topics

Skills acquired

Target audience

Programme information and source links

The project will use these datasets to examine the relationship between industry requirements and training programme content.

**Data Sources and Collection Methods**

Job Vacancy Sources

Data Source

Collection Method

Status

Jobberman

Downloadable CSV dataset

Collected

Moniepoint Careers

Public Greenhouse API

Collected

OPay Careers

Public job-listing API

Collected

Additional Nigerian job platforms

API research and permitted data collection

Pending

Collection approach:

Downloadable datasets are obtained and stored in CSV format.

Public APIs are accessed using Python Requests.

Relevant job fields are extracted and standardised.

Data is stored in structured CSV files for further processing.

Training Programme Sources

Training Provider

Programme Information

Status

3MTT Nigeria

Technology training programmes

Collected

ALX Africa

Data Science programme and curriculum

Collected

Cisco Networking Academy

Technology courses and modules

Collected

IBM SkillsBuild

Learning programmes and modules

Collected

Google

Skilling Africa programme information

Collected

Detailed curriculum records currently cover selected ALX, Cisco and IBM courses. Additional curriculum information will be collected where available.

**Project Methodology**

The project follows a structured data engineering and analytics workflow.

Stage 1: Data Source Identification

Identify relevant Nigerian job platforms, company career websites, available APIs, downloadable datasets and technology training providers.
Stage 2: Data Collection

Extract job vacancy information and collect training programme and curriculum information.

Stage 3: Data Storage

Store collected information in structured CSV datasets organised by data source and category.

Stage 4: Data Cleaning and Preparation

Standardise column names, clean text fields, handle missing values, remove duplicate job records where identifiable and prepare datasets for analysis.

Stage 5: Skills Extraction

Apply keyword-based techniques to identify technology-related vacancies and extract skills mentioned in job descriptions.

Stage 6: Skills Analysis

Examine frequently requested skills, job roles, employers and locations.

Stage 7: Training Curriculum Analysis

Identify skills and competencies covered by collected training programmes.

Stage 8: Skills Alignment Assessment

Compare employer skill requirements with training programme coverage to identify areas of alignment and potential gaps.

Stage 9: Data Visualisation and Reporting

Develop a Power BI dashboard and document findings, limitations and recommendations.
