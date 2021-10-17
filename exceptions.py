class RateGuardException(Exception):
    def __init__(self, message):
        super(RateGuardException, self).__init__(message)