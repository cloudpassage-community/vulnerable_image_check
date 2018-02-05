class VulnerableImageCheck(object):
    """
       This class will return information for vulnerable images in monitored
       registries
    """
    def __init__(self, halo):
        self.vulnerable_image_check(halo)

    @classmethod
    def vulnerable_image_check(self, halo):

        # get an HTTP helper object to call REST endpionts
        http_helper_ob = halo.get_http_helper_obj()

        # get all the critical active issues
        image_issues_endpoint = "/v1/image_issues?critical=true&status=active"
        image_issues = http_helper_ob.get(image_issues_endpoint)

        count = 0
        NONE = 0
        INCREMENT = 1
        NEWLINE = "\n"

        for image_issue in image_issues["image_issues"]:
            print "%sImage in repository %s with tag %s from registry %s" \
                  " has vulnerable package %s." \
                  % (NEWLINE, image_issue["image"]["repository"]["name"],
                     image_issue["image"]["tag"],
                     image_issue["image"]["registry"]["name"],
                     image_issue["name"])

            count += INCREMENT

        # if there are any critical vulnerabilities then kill job
        if count == NONE:
            print "There are no vulnerable images in the monitored registries"
        else:
            raise ValueError("Critical vulnerabilities in images... "
                             "failing job")
