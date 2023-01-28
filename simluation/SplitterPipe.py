from GenericPipe import GenericPipe


class SplitterPipe(GenericPipe):
    def __init__(self, inputs, outputs, length):
        super().__init__(inputs, outputs, length)

    # ======== override methods ======== #
    def push(self):
        # TODO
        # will push water down all children connections (outputs) split equally between children
        # cascading effect down children
        pass

    def snapshot(self):
        # TODO
        # maybe return a list of tuples [(component, [attributes])] via recursively calling into children
        pass
    # ================================== #
