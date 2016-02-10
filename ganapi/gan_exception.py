class GanException(Exception):
    def __init__(self, error_type, error_message, *args, **kwargs):
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return u'({error_type}) {error_message}'.format(error_type=self.error_type,
                                                        error_message=self.error_message)