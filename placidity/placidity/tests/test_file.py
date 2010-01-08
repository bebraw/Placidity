import os
import tempfile
from mock import patch
from placidity.file import File

class TestFile:

    @patch('os.path.isdir')
    def test_get_file_name(self, isdir_mock):
        isdir_mock.return_value = False

        def test_func(file):
            assert file.name == 'file'

        self.separators_test(test_func)

    @patch('os.path.isdir')
    def test_get_file_parent(self, isdir_mock):
        isdir_mock.return_value = False

        def test_func(file):
            assert file.parent.name == 'to'
            assert file.parent.parent.name == 'path'

        self.separators_test(test_func)

    @patch('os.path.isdir')
    def test_get_directory_children(self, isdir_mock):
        isdir_mock.return_value = False

        def test_func(file):
            directory = file.parent
            assert directory.children == [file, ]

        self.separators_test(test_func)

    @patch('os.path.isdir')
    def test_find_by_name(self, isdir_mock,):
        isdir_mock.return_value = False

        def test_func(file):
            directory = file.parent
            assert directory.find(name='file') == file

        self.separators_test(test_func)

    @patch('os.path.isdir')
    def test_find_by_name_and_type(self, isdir_mock,):
        isdir_mock.return_value = False

        def test_func(file):
            directory = file.parent
            assert file.name == 'file'
            assert file.type == 'py'
            assert directory.find(name='file', type='py') == file

        self.separators_test(test_func, extension='py')

    @patch('os.path.isdir')
    def test_load_python_file(self, isdir_mock):
        def create_temp_file(code):
            # http://docs.python.org/library/tempfile.html#tempfile.mktemp
            temp_file = tempfile.NamedTemporaryFile(delete=False,
                suffix='.py')
            temp_file.write(python_code)
            temp_file.close()

            return temp_file

        def remove_temp_files(temp_file):
            os.unlink(temp_file.name)

        python_code = '''
class Bar: flag = True
class Foo: flag = False
        '''
        
        isdir_mock.return_value = False

        temp_file = create_temp_file(python_code)
        file = File(temp_file.name)
        remove_temp_files(temp_file)

        assert 'bar' in file.classes
        assert file.classes['bar'].flag == True
        assert 'foo' in file.classes
        assert file.classes['foo'].flag == False

    def test_python_files_in_folder(self):
        file_path = 'path'

        def isdir(path):
            if path is file_path:
                return True

            return False

        os.path.isdir = isdir

        def listdir(path):
            if path is file_path:
                return ['bar', 'baz', 'foo', ]

        os.listdir = listdir

        file = File(file_path)

        assert file.find(name='bar')
        assert file.find(name='baz')
        assert file.find(name='foo')

    def test_no_path(self):
        file = File()

        assert file.name == None

    def separators_test(self, test_func, extension=None):
        extension = '.' + extension if extension else ''

        for sep in ('/', '\\'):
            path = sep + 'path' + sep + 'to' + sep + 'file' + extension
            file = File(path)

            test_func(file)
