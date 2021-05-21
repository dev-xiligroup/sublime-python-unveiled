"""xili_regionmore.py
this example contains a new class (in modules) to provide more methods to sublime.Region with only few methods

# v 210521 - first public dev release

"""
# import re

import imp
import sublime
import sublime_plugin
import os.path

import RegionMore.modules.xili_mod_regionmore_class
imp.reload( RegionMore.modules.xili_mod_regionmore_class ) # for dev
from RegionMore.modules.xili_mod_regionmore_class import RegionMore # the new sub class

class TestRegionMoreCommand(sublime_plugin.TextCommand):

    def run(self, edit, **args):

        """
        moreregion = RegionMore( self.view.id())
        moreregion.set(1000,199)
        print(moreregion, moreregion.id(), moreregion.size(), moreregion.begin(),'<<toto', moreregion.sel()[0])
        moreregion.display()
        print(moreregion.string())
        print(moreregion.search(r'scripts'))
        print(moreregion.findall(r'scripts'))
        """
        thew = self.view.window()
        thew_vars = thew.extract_variables()
        print(' active view ', thew.active_view().id())
        fext = thew_vars['file_extension']
        print(' self win ',thew_vars)

        # viewb = thew.open_file('bufffer.php') # create an empty view if not exist !!!

        #if os.path.isfile(thew_vars['packages']+'/User/buffer.php'):
            #viewb = thew.open_file(thew_vars['packages']+'/User/buffer.php') # car asynchorone so path needed 'buffer.php')
            #print('file exists', viewb.id())
            #viewb.close()
        #else:
            #print('not find')
        # new
        #viewn = thew.new_file()

        #print(' new win ', thd)
        #print(' new win ', viewn.id())

        MyBuffer1 = BufferMore.new_buffer(self.view) # not yet class like object but return an object
        thd = MyBuffer1.window().extract_variables()
        print(' new win not saved ', thd)
        buf_args = {
            "path":thd['packages'],
            "subpath":['User','testbuff'], # or not list
            "filename":'filebuff',
            'file_extension': fext # same as target file
        }
        MyBuffer1.set(buf_args)
        # header of buffer
        if fext == 'php':
            len_vn = MyBuffer1.insert(edit,0,'<?php\nfunction too () {\n\t $ = 0;\n}\n')
        # print (viewn.substr(sublime.Region(1, 10)))
            len_vn += MyBuffer1.insert(edit,len_vn,'# below - part inserted for RegionMore\n')
        # print (viewn.substr(sublime.Region(1, 30)))
            selector_test = "meta.function"
            indice = 2
        elif fext == 'py':
            len_vn = MyBuffer1.insert(edit,0,'"""below - part inserted for RegionMore"""\n')
            selector_test = "comment"
            indice = 0
        region = self.view.find_by_selector(selector_test) # only list of function...
        if not isinstance(region, list):
            region = [region]
            # test on 2
        region_test = region[indice]
        if isinstance(region_test, sublime.Region):
            pos_a = len_vn
            len_vn += MyBuffer1.insert(edit,len_vn, self.view.substr(region_test))
            pos_b = len_vn
            # search inside buffer
            Region_Buffer = RegionMore(MyBuffer1.id()) # only in inserted part
            Region_Buffer.set(pos_a, pos_b)
            print('match in more ',Region_Buffer.findall(r'get_.+?_mod', 0 ))

            result = Region_Buffer.more_finditer(r'\$content_width', 0)
            if result:
                print(len(result),'iter in more ',result[0].span(), result[0].group())

        # see results
        MyBuffer1.save()
        thd = MyBuffer1.window().extract_variables()
        print(' new win saved ', thd)
        print(' new win ', MyBuffer1.id())
        if not MyBuffer1.is_loading():
            print('try close')
            if 'close' in args and args['close'] is True:
                MyBuffer1.close() # undocumented why this not work -> run_command('close_file')
        print(' active view ', thew.active_view().id())

        # select in original
        if isinstance(region_test, sublime.Region) and result:
            region_selected = []
            for one_result in result:
                region_selected.append(sublime.Region(region_test.a + one_result.span()[0], region_test.a + one_result.span()[1]))
            # print(region_selected)
            if not isinstance(region_selected, list):
                region_selected = [region_selected]

            # shows in color !
            self.view.add_regions("test", region_selected, "region.greenish", "circle",
            flags=sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL)
        #MyBuffer = BufferMore(viewn.id())

        sublime.active_window().focus_view(self.view) # not documented ! back to target file
        print (self.view.style_for_scope('meta.function'))
        print('----> ',BufferMore.nameis( ' is good' ))
        print('--inst--> ',MyBuffer1.name )
        print('--class--> ',BufferMore.name )
        MyBuffer2 = MyBuffer1.new_buffer(self.view)

class BufferMore(sublime.View):
    name = "BufferMore"

    @classmethod
    def nameis(cls, iis):
        # cls.name = "bernard"
        print('set is', cls.name, iis)
        return 'inside ', cls.name

    def set(self, bufargs):
        self.name = "michel"
        print('set ',self.name)
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
        if not cls.name == "BufferMore":
            raise "method new_buffer cannot be used with instantiated"
        viewnew = view.window().new_file()
        buff = BufferMore(viewnew.id()) # a way to create a buffer with newfile view.id
        #now an objet
        cls.name = buff.id()
        print(cls.name,buff.id())
        return buff
    # save if object instantiated
    def save(self):
        os.makedirs(os.path.join(self.path, str(os.path.sep).join(tuple(self.subpath))), exist_ok=True)
        self.retarget(self.file)
        self.run_command('save')
