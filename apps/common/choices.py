class DRFActions:
    LIST = "list"
    CREATE = "create"
    RETRIEVE = "retrieve"
    UPDATE = "update"
    PARTIAL_UPDATE = "partial_update"
    DESTROY = "destroy"
    DOWNLOAD = "download"

    ACTIONS = [LIST, CREATE, RETRIEVE, UPDATE, PARTIAL_UPDATE, DESTROY, DOWNLOAD]


class RESTMethods:
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"
    PUT = "PUT"

    METHODS = [GET, POST, PATCH, DELETE, PUT]
