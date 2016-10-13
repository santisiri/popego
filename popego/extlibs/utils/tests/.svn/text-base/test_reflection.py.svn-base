import unittest
import sys 
from os import path
from utils import reflection

class TestReflection(unittest.TestCase):
    def setUp(self):
        testmodulespath = path.join(path.abspath(path.dirname(__file__)) , 'data')
        sys.path.append(testmodulespath)
    def test_importModule(self):
        m = reflection.importModule('samplepackage.samplemodule')
        assert m
        assert getattr(m, 'anInstance')

    def test_findClasses(self):
        classes = reflection.findClasses('samplepackage.samplemodule')
        assert len(classes) == 3
        assert ['NewStyleClass','NewStyleClassAttr', 'OldStyleClass'] \
            == sorted(n for n,v in classes)

    def test_findClasses_withPredicate(self):
        classes = reflection.findClasses('samplepackage.samplemodule',
                                         lambda n,x : n.startswith('NewStyle'))
        assert len(classes) == 2
        assert ['NewStyleClass','NewStyleClassAttr'] \
            == sorted(n for n,v in classes)

    def test_isValidClass_True(self):
        pkg = 'samplepackage.samplemodule'
        assert reflection.isValidClass(pkg + ':NewStyleClass')
        assert reflection.isValidClass(pkg + ':OldStyleClass')
        assert reflection.isValidClass(pkg + ':NewStyleClassAttr')

    def test_isValidClass_Fail(self):
        self.assertRaises(ValueError, reflection.isValidClass, 'samplepackage')
        self.assertRaises(ValueError, reflection.isValidClass, 'a.b.c')

    def test_isValidClass_False(self):
        pkg = 'samplepackage.samplemodule'
        self.assertFalse(reflection.isValidClass(pkg + ':anInstance'))
        self.assertFalse(reflection.isValidClass(pkg + ':someFunction'))
        self.assertFalse(reflection.isValidClass('my.funny.pkg:Bla'))

    def test_findSubModules(self):
        m = reflection.importModule('samplepackage')
        submodules = reflection.findSubModules(m)
        print submodules
        assert len(submodules) == 2
        assert ['apackage', 'samplemodule'] == sorted(submodules)
