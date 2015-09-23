from robot.utils import ConnectionCache


class ApplicationCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current application')
        self._closed = set()

    @property
    def applications(self):
        return self._connections

    def get_open_browsers(self):
        open_applications = []
        for application in self._connections:
            if application not in self._closed:
                open_applications.append(application)
        return open_applications

    def close(self):
        if self.current:
            application = self.current
            application.quit()
            self.current = self._no_current
            self.current_index = None
            self._closed.add(application)

    def close_all(self):
        for application in self._connections:
            if application not in self._closed:
                application.quit()
        self.empty_cache()
        return self.current
