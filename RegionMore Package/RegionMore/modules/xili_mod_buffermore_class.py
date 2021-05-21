"""xili_mod_buffermore.py"""

import os.path
import sublime

class BufferMore(sublime.View):

    """ a view/buffer used for searching !!

    Attributes:
        file (TYPE): Description
        file_extension (TYPE): Description
        filename (TYPE): Description
        name (str): Description
        path (TYPE): Description
        subpath (TYPE): Description
        thew (TYPE): Description
    """

    name = "BufferMore" # can be modified by instantiation !

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
            bufargs (TYPE): Description
        """
        self.path = bufargs['path']
        self.subpath = bufargs['subpath']
        self.filename = bufargs['filename']
        self.file_extension = bufargs['file_extension']
        self.thew = self.window()
        thew_vars = self.thew.extract_variables()
        print(' Buffer win ',thew_vars, 'sep ',str(os.path.sep))
        ll = []
        if not isinstance(self.subpath, list):
            self.subpath = [self.subpath]
        ll.extend(self.subpath) # add a list
        ll.append(self.filename + '.' + self.file_extension) # add one element
        subpath_file = os.path.sep.join(tuple(ll)) # only tuple !
        self.file = os.path.join(self.path,subpath_file) # parameter and not list
        print(' Buffer file ', self.file)

    @classmethod # @staticmethod
    def new_buffer(cls, view):
        """Summary

        Args:
            view (TYPE): Description

        Returns:
            TYPE: Description

        Raises:
            "BufferMore: Description
        """
        #print(isinstance(cls, BufferMore))
        print('cls name ', cls.name)
        #if cls.name != "BufferMore":
            #raise "BufferMore : method new_buffer cannot be used with instantiated class"
        viewnew = view.window().new_file()
        buff = BufferMore(viewnew.id()) # a way to create a buffer with newfile view.id
        #now an objet returned
        return buff
    # save if object instantiated

    def save(self):
        """Summary
        """
        os.makedirs(os.path.join(self.path, str(os.path.sep).join(tuple(self.subpath))), exist_ok=True)
        self.retarget(self.file)
        self.run_command('save')
