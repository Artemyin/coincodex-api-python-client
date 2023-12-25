class CoincodexAPIException(Exception):
    def __init__(self, response):
        try:
            json_response = response.json()
        except ValueError:
            self.message = f"JSON error message from coincodex: {response.text}"
        else:
            if "error" not in json_response:
                self.message = "Wrong json format from response.textAPI"
            else:
                self.message = json_response["error"]

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, "request", None)

    def __str__(self):
        return f"{self.__class__.__name__}(status_code: {self.status_code}): {self.message}"


class CoincodexRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"CoincodexRequestException: {self.message}"


class CoincodexAPIBadRequestException(CoincodexAPIException):
    status_code = 400


class CoincodexAPIUnauthorizedException(CoincodexAPIException):
    status_code = 401


class CoincodexAPIPaymentRequiredException(CoincodexAPIException):
    status_code = 402


class CoincodexAPIForbiddenException(CoincodexAPIException):
    status_code = 403


class CoincodexAPINotFoundException(CoincodexAPIException):
    status_code = 404


class CoincodexAPITooManyRequestsException(CoincodexAPIException):
    status_code = 429


class CoincodexAPIInternalServerErrorException(CoincodexAPIException):
    status_code = 500


