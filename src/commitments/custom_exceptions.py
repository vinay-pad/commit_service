from rest_framework.exceptions import APIException

class RequestProcessed(APIException):
    status_code = 200
    default_detail = 'Request to make message readable successful'
    default_code = 'request_processed'
