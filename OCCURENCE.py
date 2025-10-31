# Python 3 Program to find the occurrence
# of the most frequent number within
# a given range
from collections import defaultdict
import math

# A utility function to get the middle index
# from corner indexes.
def getMid(s,  e):
    return s + (e - s) // 2

''' A recursive function to get the maximum value in
    a given range of array indexes. The following
    are parameters for this function.

    st --> Pointer to segment tree
    index --> Index of current node in the segment
            tree. Initially 0 is passed as root is
            always at index 0
    ss & se --> Starting and ending indexes of the
                segment represented by current node,
                i.e., st[index]
    qs & qe --> Starting and ending indexes of query
                range '''
def RMQUtil(st,  ss,  se,  qs,  qe, index):
  
    # If segment of this node is a part of given range
    # then return the min of the segment
    if (qs <= ss and qe >= se):
        return st[index]
      
    # If segment of this node is outside the
    # given range
    if (se < qs or ss > qe):
        return 0

    # If a part of this segment overlaps
    # with the given range
    mid = getMid(ss, se)
    return max(RMQUtil(st, ss, mid, qs, qe, 2 * index + 1),
               RMQUtil(st, mid + 1, se, qs, qe, 2 * index + 2))


# Return minimum of elements in range from
# index qs (query start) to
# qe (query end). It mainly uses RMQUtil()
def RMQ(st,  n,  qs,  qe):

    # Check for erroneous input values
    if (qs < 0 or qe > n - 1 or qs > qe):
        prf("Invalid Input")
        return -1

    return RMQUtil(st, 0, n - 1, qs, qe, 0)

# A recursive function that constructs Segment Tree
# for array[ss..se]. si is index of current node in
# segment tree st
def constructSTUtil(arr,  ss,  se,  st,
                    si):
  
    # If there is one element in array, store it in
    # current node of segment tree and return
    if (ss == se):
        st[si] = arr[ss]
        return arr[ss]
      
    # If there are more than one elements, then
    # recur for left and right subtrees and store
    # the minimum of two values in this node
    mid = getMid(ss, se)
    st[si] = max(constructSTUtil(arr, ss, mid, st, si * 2 + 1),
                 constructSTUtil(arr, mid + 1, se, st, si * 2 + 2))
    return st[si]

''' Function to construct segment tree from given
array. This function allocates memory for segment
tree and calls constructSTUtil() to fill the
allocated memory '''
def constructST(arr, n):

    # Allocate memory for segment tree
    # Height of segment tree
    x = (math.ceil(math.log2(n)))
    
    # Maximum size of segment tree
    max_size = 2 * pow(2, x) - 1
    st = [0]*max_size

    # Fill the allocated memory st
    constructSTUtil(arr, 0, n - 1, st, 0)
    
    # Return the constructed segment tree
    return st

def maximumOccurrence(arr,  n,  qs,  qe):

    # Declaring a frequency array
    freq_arr = [0]*(n + 1)
    
    # Counting frequencies of all array elements.
    cnt = defaultdict(int)
    for i in range(n):
        cnt[arr[i]] += 1

    # Creating frequency array by replacing the
    # number in array to the number of times it
    # has appeared in the array
    for i in range(n):
        freq_arr[i] = cnt[arr[i]]

    # Build segment tree from this frequency array
    st = constructST(freq_arr, n)
    maxOcc = 0  # to store the answer
    # Case 1: numbers are same at the starting
    # and ending index of the query
    if (arr[qs] == arr[qe]):
        maxOcc = (qe - qs + 1)
        
    # Case 2: numbers are different
    else:
        leftmost_same = 0
        righmost_same = 0
        
        # Partial Overlap Case of a number with some
        # occurrences lying inside the leftmost
        # part of the range and some just before the
        # range starts
        while (qs > 0 and qs <= qe and arr[qs] == arr[qs - 1]):
            qs += 1
            leftmost_same += 1

        # Partial Overlap Case of a number with some
    # occurrences lying inside the rightmost part of
        # the range and some just after the range ends
        while (qe >= qs and qe < n - 1 and arr[qe] == arr[qe + 1]):
            qe -= 1
            righmost_same += 1

        # Taking maximum of all three
        maxOcc = max([leftmost_same, righmost_same,
                      RMQ(st, n, qs, qe)])

        return maxOcc

# Driver Code
if __name__ == "__main__":

    arr = [-5, -5, 2, 2, 2, 2, 3, 7, 7, 7]
    n = len(arr)

    qs = 0  # Starting index of query range
    qe = 9  # Ending index of query range

    # Print occurrence of most frequent number
    # within given range
    print("Maximum Occurrence in range is = ",
          maximumOccurrence(arr, n, qs, qe))

    qs = 4  # Starting index of query range
    qe = 9  # Ending index of query range

    # Print occurrence of most frequent number
    # within given range
    print("Maximum Occurrence in range is = ",
          maximumOccurrence(arr, n, qs, qe))

    # This code is contributed by ukasp.
