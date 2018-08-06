##### -----      Running Dinner Calculator in Python      ----- #####

# importing libraries
import random
import numpy
import csv
import xlwt


courseCount = 3
groupCount = 11
noko_on = 1
kitchenList = ['St. Syd', 'St. Syd', '1. Syd', '2. Syd', '3. Nord',
               '4. Nord', 'St. Nord', '5. Syd', '4. Syd', '3. Nord',
               '2. Nord']


# recalculating raw input: creating group list and numerated kitchen list
groupList = list(range(1, groupCount + 1))
if noko_on == 1:
    kitDict = dict([(y, x + 1) for x, y in enumerate(sorted(set(kitchenList)))])
    kitchenListNum = [kitDict[x] for x in kitchenList]

##### -----      building overall structure      ----- #####

## function #1
## function arguments:  Number of courses (scalar), number of groups (scalar)
## function output:     Cluster structure (list)
def clusterstructure(n_courses, n_groups):
    
    # calculating variables
    superClusterBase = n_groups // n_courses 
    superClusterRemain = n_groups % n_courses - 1
    superCourseClusters = []
    clusterStructure = []

    # generating list of cluster structure. looping over courses and adding number of required clusters per course
    for i in range(n_courses):
        if i <= superClusterRemain:
            superCourseClusters.append(superClusterBase + 1)
        else:
            superCourseClusters.append(superClusterBase)

    # shuffling list for random cluster sizes across courses
    random.shuffle(superCourseClusters)

    # looping over courses to create n_courses number of lists with number of groups per cluster
    for j in range(n_courses):
        
        # calculating variables
        subCourseClusters = []
        subClusterBase = n_groups // superCourseClusters[j]
        subClusterRemain = n_groups % superCourseClusters[j] - 1
        
        # looping over list of clusters per course
        for i in range(superCourseClusters[j]):
            if i <= subClusterRemain:
                subCourseClusters.append(subClusterBase + 1)
            else:
                subCourseClusters.append(subClusterBase)
        
        # shuffling group count per cluster for random allocation
        random.shuffle(subCourseClusters)
        clusterStructure.append(subCourseClusters)

    # returning final cluster structure as list
    return clusterStructure

## function #2
## function arguments:  [1] Number of courses (integer), [2] list of groups (list), [3] cluster structure (list)
## fucntion output:     [1] List of clustered groups (list), [2] Clusters per group (list)
def finalgrouplist(n_courses, group_list, cluster_structure):

    # defining empty variables
    tempList = []
    finalGroupList = []

    # looping over courses to generate a list of groups for each
    for j in range(n_courses):
        
        # generating counters and empty lists
        clusterId = 0
        groupsCounter = 0
        subIndexList = []
        tempCourseList = []
        groupWiseIndexList = []

        # shuffling group list and copying static image
        shuffleList = group_list[:]
        random.shuffle(shuffleList)
        staticShuffleList = shuffleList[:]

        # looping over each cluster within courses
        for cluster in cluster_structure[j]:
            tempCluster = []

            # looping number of groups within each cluster
            for i in range(cluster):
                tempCluster.append(shuffleList.pop(0))
                subIndexList.append(clusterId)
                groupsCounter += 1
                groupWiseIndexList.append(staticShuffleList.index(groupsCounter))
            tempCourseList.append(tempCluster)
            clusterId += 1
        
        # populating final list of groups within each cluster and course
        tempIndexList = [subIndexList[i] for i in groupWiseIndexList]
        groupWiseClusterList = [tempCourseList[i] for i in tempIndexList]
        finalGroupList.append(tempCourseList)
        tempList.append(groupWiseClusterList)    
        
    # populating group-wise list of assigned cluster
    groupWiseMatchList = [list(i) for i in zip(tempList[0], tempList[1], tempList[2])]

    # collecting final group list and group-wise list of assigned clusters
    return finalGroupList, groupWiseMatchList

##### -----      assigning groups to the structure      ----- #####

## function #3
## function arguments:  [1] number of groups (integer)
## fucntion output:     [1] List of clustered groups (list), [2] Clusters per group (list), [3] coverage matrix (numpy array)
def assigngroups(n_groups):
    diffLenSum = 42
    while diffLenSum != 0:
        
        # running structural functions to get basic structure of lists
        finalList, groupWiseMatchList = finalgrouplist(courseCount, groupList, clusterstructure(courseCount, n_groups))
        diffLenSum = 0
        for i in range(n_groups):
            j = i + 1
            flatList = [x for sublist in groupWiseMatchList[i] for x in sublist]
            listLen = len(flatList)
            diffLen = listLen - len(set(flatList)) - 2
            diffLenSum += diffLen

    # converting final group-cluster list to a matrix
    covMatrix = numpy.zeros((n_groups, n_groups),dtype=int)
    flatFinalList = [x for sublist in finalList for x in sublist]
    for i in range(len(flatFinalList)):
        for group in flatFinalList[i]:
            covMatrix[i, group - 1] = 1

    # returning three outputs: final list of assigned groups, group-wise list and coverage matrix
    return finalList, groupWiseMatchList, covMatrix, flatFinalList

##### -----      assigning hosts and kitchens to the groups      ----- #####

## function #4
## assigning hosts while making sure that all groups are hosting exactly 1 course and that no kitchen is used more than
## once per course
def assignhosts(n_groups):
    totalKitchenOverlap = 42
    while totalKitchenOverlap != 0:

        hostMatchSum = 42
        while hostMatchSum != n_groups:

            # defining empty lists for host clusters and groups
            hostClusterList = []
            hostGroupList = []
            rowArray = numpy.arange(1, n_groups + 1)
            colArray = numpy.arange(1, n_groups + 1)
            finalList, groupWiseList, covMatrix, flatFinalList = assigngroups(n_groups)

            for i in range(n_groups):

                # searching next row for host flagging
                sumVector = numpy.sum(covMatrix, axis = 1)
                minRow = numpy.argmin(sumVector)
                corrVector = covMatrix[minRow, :]
                maxCol = numpy.argmax(corrVector)

                # getting cluster and group numbers from arrays before slicing
                hostCluster = rowArray[minRow]
                hostGroup = colArray[maxCol]
                hostClusterList.append(hostCluster)
                hostGroupList.append(hostGroup)

                # removing flagged row and column and slicing coverage matrix
                rowArray = numpy.delete(rowArray, minRow, 0)
                colArray = numpy.delete(colArray, maxCol, 0)
                covMatrix = numpy.delete(covMatrix, minRow, 0)
                covMatrix = numpy.delete(covMatrix, maxCol, 1)

            # checking if assigned hosts match their clusters
            hostMatchSum = 0
            for i in range(len(hostGroupList)):
                hostMatch = (hostGroupList[i] in flatFinalList[hostClusterList[i] - 1]) * 1
                hostMatchSum += hostMatch

        i = 1
        totalKitchenOverlap = 0
        finalKitchenList = []
        for course in finalList:
            courseKitchenList = []
            for cluster in course:
                courseKitchenList.append(kitchenListNum[hostGroupList[hostClusterList.index(i)] - 1])
                i += 1
            finalKitchenList.append(courseKitchenList)
            courseKitchenSet = set(courseKitchenList)
            hostOverlap = len(courseKitchenList) - len(courseKitchenSet)
            totalKitchenOverlap += hostOverlap

    return finalList, groupWiseList, hostClusterList, hostGroupList, finalKitchenList

# Running final function: assigning groupds, clusters, hosts, and kitchens
finalList, groupWiseList, hostClusterList, hostGroupList, finalKitchenList = assignhosts(groupCount)

# Printing Calculated dinner plan
print('Course List: ', finalList)
print('Host Cluster: ', hostClusterList)
print('Host Group: ', hostGroupList)
print('Final Kitchen List: ', finalKitchenList)
print('Kitchen Numbers: ', kitDict)




