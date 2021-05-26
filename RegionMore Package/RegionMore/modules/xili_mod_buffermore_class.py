"""xili_mod_buffermore.py"""

import os.path
import sublime

class BufferMore(sublime.View):

    """a view/buffer used for searching !!

    Attributes:
        buffers (list): Catalog of instantiate objets
        file (str): full path of file linked to buffer
        file_extension (str): Extension
        filename (str): Description
        name (str): Description
        path (str): Root of the path
        subpath (str or list): One or more subpath
        view_id (int): Id of linked view

    """

    name = "BufferMore" # can be modified by instantiation !
    buffers = []

    def __init__(self, view_id, view):
        """ init contains a way to increment unique ID
        Args:
            view_id (int): Not used
            view (view): of current view (self.view in container's context)
        print('init PE): Description
        """
        viewtemp = view.window().new_file() # create an empty view but with good ID
        self.view_id = viewtemp.id() # self.view is used by method id
        self.buffers.append(self.view_id) # before above line to avoid erasing
        self = viewtemp

    def __del__(self):
        print("BufferMore ",self.view_id," deleted")
        self.buffers.remove(self.view_id)

    @classmethod
    def buffermores(cls):
        """Set a list of buffer object

        Returns:
            list: of view object
        """
        #if cls.buffers:
        buffer_views=[]
        for buffer_id in cls.buffers:
            buffer_views.append(sublime.View(buffer_id))
        return buffer_views

    @classmethod
    def nameis(cls, iis):
        """Summary

        Args:
            iis (TYPE): Description

        Returns:
            TYPE: Description
        """
        # cls.name = "bernard"
        print('set is', cls.name, iis)
        return 'inside ', cls.name

    def set(self, bufargs):
        """Summary

        Args:
            bufargs (dict): Description
        """
        self.path = bufargs['path']
        self.subpath = bufargs['subpath']
        self.filename = bufargs['filename']
        self.file_extension = bufargs['file_extension']
        # self.thew = self.window()
        # thew_vars = self.thew.extract_variables()
        # print(' Buffer win ',thew_vars, 'sep ',str(os.path.sep))
        ll = []
        if not isinstance(self.subpath, list):
            self.subpath = [self.subpath]
        ll.extend(self.subpath) # add a list
        ll.append(self.filename + '.' + self.file_extension) # add one element
        subpath_file = os.path.sep.join(tuple(ll)) # only tuple !
        self.file = os.path.join(self.path,subpath_file) # parameter and not list
        print(' Buffer file ', self.file)

    # save if object instantiated

    def save(self):
        """ The working buffer is saved somewhere (see set)
        """
        os.makedirs(os.path.join(self.path, str(os.path.sep).join(tuple(self.subpath))), exist_ok=True)
        self.retarget(self.file)
        self.run_command('save')
