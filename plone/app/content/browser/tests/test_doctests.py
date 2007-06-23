from zope.testing import doctest
from unittest import TestSuite

from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

setupPloneSite(extension_profiles=['Products.CMFPlone:testfixture'])

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class FolderTestCase(FunctionalTestCase):
    """base test case with convenience methods for all control panel tests"""

    def afterSetUp(self):
        super(FolderTestCase, self).afterSetUp()
        from Products.Five.testbrowser import Browser
        self.browser = Browser()
        
        self.uf = self.portal.acl_users
        self.uf.userFolderAddUser('root', 'secret', ['Manager'], [])

    def createDocuments(self, amount):
        self.setRoles(['Manager',])
        for i in range(1, amount):
            self.portal.invokeFactory(id='testing-%d' % i, type_name='Document')
            document = getattr(self.portal, 'testing-%d' % i)
            document.setTitle('Testing %d' % i)
            document.setExcludeFromNav(True)
            document.reindexObject()

    def createFolder(self):
        self.setRoles(['Manager',])
        self.portal.invokeFactory(id='new-folder', type_name='Folder')
        folder = getattr(self.portal, 'new-folder')
        folder.setTitle('New Folder')
        folder.setExcludeFromNav(True)
        folder.reindexObject()
        

    def loginAsManager(self):
        """points the browser to the login screen and logs in as user root with Manager role."""
        self.browser.open('http://nohost/plone/')
        self.browser.getLink('Log in').click()
        self.browser.getControl('Login Name').value = 'root'
        self.browser.getControl('Password').value = 'secret'
        self.browser.getControl('Log in').click()

def test_suite():
    tests = ['foldercontents.txt',]
    suite = TestSuite()
    for test in tests:
        suite.addTest(FunctionalDocFileSuite(test,
            optionflags=OPTIONFLAGS,
            package="plone.app.content.browser.tests",
            test_class=FolderTestCase))
    return suite
