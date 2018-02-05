Vulnerable Image Check
-

Overview
-

This project will scan all the images in registries monitored by
Halo and will throw an exception if there are any 
critical vulnerabilities.

It is written to be dropped in a Jenkins job, but can be
run as a stand-alone project as well.

Use
-

It expects API keys to be in environment variables. 
To execute run python app/runner.py

Sample Output
-

python app/runner.py

Image in repository httpd with tag 2.2 from registry DPR has vulnerable package sensible-utils.

Image in repository docker.elastic.co/logstash/logstash-oss with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk-headless.

Image in repository docker.elastic.co/logstash/logstash-oss with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk-devel.

Image in repository docker.elastic.co/logstash/logstash-oss with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk.

Image in repository mysql with tag mysql5.5 from registry DPR has vulnerable package sensible-utils.

Image in repository wordpress with tag 4.9.2-php5.6-apache from registry DPR has vulnerable package sensible-utils.

Image in repository ubuntu with tag ubuntu14.04 from registry DPR has vulnerable package libc6:amd64.

Image in repository php with tag 7.1 from registry DPR has vulnerable package sensible-utils.

Image in repository haproxy with tag 1.5 from registry DPR has vulnerable package sensible-utils.

Image in repository docker.elastic.co/logstash/logstash with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk-headless.

Image in repository docker.elastic.co/logstash/logstash with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk-devel.

Image in repository docker.elastic.co/logstash/logstash with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk.

Image in repository docker.elastic.co/elasticsearch/elasticsearch with tag 6.1.2 from registry DPR has vulnerable package java-1.8.0-openjdk-headless.

Image in repository ecr-dev with tag 2.2 from registry ECR-354855984332 has vulnerable package sensible-utils.  
Traceback (most recent call last):
  File "app/runner.py", line 9, in <module>
    vulnerable_image_check.VulnerableImageCheck(halo)
  File "/Users/jgibbons/PycharmProjects/vulnerable_image_check/app/vulnerable_image_check/vulnerable_image_check.py", line 7, in __init__
    self.vulnerable_image_check(halo)
  File "/Users/jgibbons/PycharmProjects/vulnerable_image_check/app/vulnerable_image_check/vulnerable_image_check.py", line 38, in vulnerable_image_check
    raise ValueError("Critical vulnerabilities in images... "
ValueError: Critical vulnerabilities in images... failing job 