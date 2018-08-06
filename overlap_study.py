##### -----      Running Dinner Calculator in Python      ----- #####

# importing libraries
import random
import numpy
import csv

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
    return(clusterStructure)

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

# checking group overlap in cluster matching across courses
# defining global variables
for n in range(7, 40):
    courseCount = 3
    groupCount = n
    groupList = list(range(1, groupCount + 1))
    fileName = './Group Overlap Data/avgdiff_data_' + str(n) + '.csv'
    csv = open(fileName, 'w')

    for k in range(100000):
        finalList, groupWiseMatchList = finalgrouplist(courseCount, groupList, clusterstructure(courseCount, groupCount))
        diffLenSum = 0
        for i in range(groupCount):
            j = i + 1
            flatList = [x for sublist in groupWiseMatchList[i] for x in sublist]
            listLen = len(flatList)
            diffLen = listLen - len(set(flatList)) - 2
            diffLenSum += diffLen

        avgDiff = diffLenSum / groupCount
        csv.write(str(avgDiff) + '\n')

    print('Script done for: ', n)








