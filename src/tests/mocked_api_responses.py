class MockedGetRespose:
    def __init__(self, data, status=200):
        self._data = data
        self.status = status

    async def json(self):
        return self._data

    async def __aexit__(self, exc_type, exc, tb):
        pass

    async def __aenter__(self):
        return self


class MockedSession:
    def __init__(self, get: MockedGetRespose):
        self.get = get
