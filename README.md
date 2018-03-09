Vulnerable Image Check
-

Overview
-

This project will scan all the images in registries monitored by
Halo and return a non-zero status if there are any critical vulnerabilities.  
It is a containerized application that can be dropped in a Jenkins job, or
 used in another application or as a stand-alone project.

Install
-
pip install vulnerable_image_check

Use
-

It expects API keys to be in environment variables. 

Mandatory: 
* HALO_API_KEY - a Halo API key
* HALO_API_SECRET_KEY - a Halo API secret

Optional:
* REGISTRY_NAME - the name of a monitored registry.  If this is empty 
the output will default to all monitored registries.
* REPO_NAME - the name of a repository.  If this is empty the output will 
default to all monitored repositories.
* IMAGE_TAG - the name of an image tag.  If this is empty the output will
 default to all tags.
* OUTPUT_FORMAT - if the output format is anything other than 'csv' the output
 will be formatted text.
* OCTO_BOX - unless this is explicitly set to True, it will not run for 
octo-box.  This means the output will be decoded base64.
  
Default:
* FAIL_ON_CRITICAL = "0" - defaults to success

To build run:

docker build -t vulnerable_image_check:latest .

To execute run:

docker run -it -e HALO_API_KEY=$HALO_API_KEY \
-e HALO_API_SECRET_KEY=$HALO_API_SECRET_KEY \
vulnerable_image_check

Sample Output
-

Registry: DPR    
&nbsp;&nbsp;Repository: robert_rails  
&nbsp;&nbsp;&nbsp;&nbsp;Tag: dev  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Vulnerabilities:  Package: sensible-utils  Package Version: 0.0.9 | CVE List: cve-2017-17512 # NOQA
  Package Version: 2.0.0+dfsg-2ubuntu1.40 | CVE List: cve-2013-4544 cve-2014-0150 cve-2014-2894 # NOQA
    
Project Structure
-

* vulnerable_image_check - base directory  
a) .gitchangelog.rc - configuration file for gitchangelog  
b) .gitignore - gitignore file  
c) .travis.yml - Travis CI configuration for CI testing  
d) Dockerfile - Dockerfile for building a Docker image for running the 
application stand-alone.  There are several
 packages pinned to specific versions to remediate vulnerabilities.  
e) LICENSE - BSD 2-Clause License  
f) README.md - README.md(README_v1)  
g) setup.py - PyPI setup file  

    * app - application directory  
    <t>* lib - support scripts  
    <t>1) \__init\__.py - import and version string  
    <t>2) report.py - reporting tool that outputs base64 encoded csv and 
    formatted text  
    <t>3) utility.py - used by report.py
    <t>* vulnerable_image_check - application code directory  
    <t>1) \__init\__.py - author and version string  
    <t>2) config_helper.py - the application configuration  
    <t>3) vulnerable_image_check.py - teh application
    runner.py
    * test - test directory  
    <t>* style - style tests  
    <t>1) test_style_flake8.py - flake8 tests  
    <t>* unit - unit tests  
    <t>1) test_config_helper.py - tests the application configuration  
    <t>2) test_report.py - test the report output  
    <t>3) test_vulnerable_image_check.py - test application code  


