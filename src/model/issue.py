from .editor import Editor


class Issue(object):

    def __init__(self, pubdate, pages, issue_id, released: bool = False):
        self.issue_id = issue_id
        self.pubdate = pubdate
        self.released: bool = released
        self.editor = None
        self.pages = pages

    def set_editor(self, editor: Editor):
        self.editor = editor
    
    def publish(self):
        self.released = True

