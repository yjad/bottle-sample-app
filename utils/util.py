class Utils():

    @classmethod
    def validate(cls, data):
        errMsg = []
        # noInput = 'が未入力です。'
        noInput = 'is not entered.'
        if not data['name']:
            # errMsg.append('書名' + noInput)
            errMsg.append('book title' + noInput)
        if not data['author']:
            errMsg.append('author' + noInput)
        if not data['publisher']:
            errMsg.append('the publisher' + noInput)
        return errMsg
