# -*- coding: utf-8 -*-
__docformat__='restructuredtext'
from popserver.model import *
from popserver.tests import *
from fixture import DataTestCase
import aifixtures
from popserver.ai.clustering import *
from numpy import array


class TestClustering(DataTestCase, TestModel):
    fixture = dbfixture
    datasets = [aifixtures.UserData, 
                aifixtures.ServiceTypeData, 
                aifixtures.ServiceData, 
                aifixtures.AccountData,
                aifixtures.ItemGroupData,
                aifixtures.UserItemData,
                aifixtures.VideoData,
                aifixtures.BookmarkData,
                aifixtures.TagData]

    def setUp(self):
        TestModel.setUp(self)
        DataTestCase.setUp(self)

    def tearDown(self):
        DataTestCase.tearDown(self)
        TestModel.tearDown(self)


    def test_interestsSimilarityMatrixDimension(self):
        allInterests, simMatrix = createInterestsSimilarityMatrix()
        assert len(simMatrix) == 3
        assert len(simMatrix[0]) == 3
 
    
    
    def _allElementsTrue(self, M):
        for i in range(len(M)):
            for j in range(len(M[0])):
                if M[i][j] == False:
                    return False

        return True

    def test_interestsSimilarityMatrixContent(self):
        allInterests, simMatrix = createInterestsSimilarityMatrix()
        expected = [[0, 1, 1], [1, 0, 1], [1, 1, 0]] 
        assert simMatrix == expected
