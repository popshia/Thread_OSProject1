import time
import threading
from queue import Queue

def BubbleSort(array, tempQueue): # bubble sort
    arrayLength = len(array)
    for i in range(arrayLength-1):
        for j in range(0, arrayLength-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
    print(array)
    tempQueue.put(array)
    return array


def CutArray(array): # cut the array into pieces
    index = 0
    arrays = []
    while index < len(array):
        cutArray = []
        for i in range(100):
            cutArray.append(array[index+i])
        arrays.append(cutArray)
        index += 100
    for arr in arrays:
        print(arr)
    return arrays

def main():
    startTime = time.time()

    #input = open('input1.txt', 'r')
    input = open('input2.txt', 'r')
    #input = open('input3.txt', 'r')
    #input = open('input4.txt', 'r')

    whichFunctionToUse = int(input.readline())
    array = []
    tempQueue = Queue()

    for n in input.read().split():
        array.append(int(n))
    
    if whichFunctionToUse == 1:
        print("Running function 1...")
        answer = BubbleSort(array, tempQueue)

    elif whichFunctionToUse == 2:
        print("Running function 2...")
        cutArrays = CutArray(array)
        threads = []
        for singleCutArray in cutArrays: # create threads
            singleThread = threading.Thread(target=BubbleSort, args=(singleCutArray, tempQueue))
            singleThread.start()
            threads.append(singleThread)

        for thread in threads: # join threads
            thread.join()

        sortedThreadArrays = [] # array to save thread sorted arrays

        for _ in range( int(len(array)/100) ):
            sortedThreadArrays.append(tempQueue.get())
    '''
    elif whichFunctionToUse == 3:
        
    elif whichFunctionToUse == 4:

    '''
    input.close()
    endTime = time.time()
    print("CPU process time: ", endTime-startTime, " sec")

if __name__ == "__main__":
    main()