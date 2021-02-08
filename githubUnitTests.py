import unittest
from githubFlask import backgroundColours, interogateGit, repoThreadBuilder
from github import Github


class TestFlask(unittest.TestCase):

    def test_backgroundColour(self):
        testList1 = [1, 4, 3, 5, 10]
        testList2 = [84, 212, 885, 37, 234, 71, 5492]

        self.assertEqual(backgroundColours([]), [])
        self.assertEqual(backgroundColours([-1, 6, 3, -4]), [])
        self.assertEqual(backgroundColours(testList1), ['#4b0000', '#870000', '#730000', '#9b0000', '#ff0000'])
        self.assertEqual(backgroundColours(testList2), ['#3a0000', '#3f0000', '#570000', '#380000', '#400000', '#3a0000', '#ff0000'])
        self.assertEqual(backgroundColours(testList1 + testList2), ['#370000', '#370000', '#370000', '#370000', '#370000', '#3a0000', '#3f0000', '#570000', '#380000', '#400000', '#3a0000', '#ff0000'])

    def test_interogateGit(self):
        git = Github("b00ba8aef217cb2f87d1f8d668a168d0c9890acc")
        self.assertEqual(interogateGit(git.get_user("RedmondC"), "public", True),
                         ['RedmondC',
                          sorted(['FractalTrees', 'SortingAlgorithms', 'Sorting-Algorithm-Visualiser', 'frogs', 'TicTacToePython', 'LCMPython', 'CalcPiWithBlocks', 'VHDL', 'LowestCommonAnscestor']),
                          sorted(['#580000', '#ee0000', '#480000', '#7a0000', '#580000', '#8a0000', '#690000', '#ff0000', '#580000']),
                          sorted(['#390000', '#3c0000', '#390000', '#3c0000', '#390000', '#400000', '#400000', '#ff0000', '#6a0000']),
                          sorted(['#3b0000', '#4d0000', '#400000', '#ff0000', '#3a0000']),
                          sorted([1, 2, 1, 2, 1, 4, 4, 87, 22]),
                          sorted([2, 11, 1, 4, 2, 5, 3, 12, 2]),
                          9,
                          124,
                          42,
                          13.78,
                          4.67,
                          5,
                          sorted(['Processing', 'Java', 'Python', 'VHDL', 'Haskell']),
                          sorted([2059, 12012, 4809, 108244, 1589]),
                          'public'])

    def test_repoThreadBuilder(self):
        git = Github("b00ba8aef217cb2f87d1f8d668a168d0c9890acc")
        repo = git.get_user("RedmondC").get_repo("SortingAlgorithms")
        self.assertEqual(repoThreadBuilder(repo, True), [11, {'Java': 9689}, 2])
        repo = git.get_user("RedmondC").get_repo("LowestCommonAnscestor")
        self.assertEqual(repoThreadBuilder(repo, True), [2, {'Haskell': 1589, 'Java': 2323, 'Python': 1099}, 22])


if __name__ == '__main__':
    unittest.main()
