import time
import threading
from queue import Queue

def BubbleSort(array, tempQueue): # bubble sort
	arrayLength = len(array)
	for i in range(arrayLength-1):
		for j in range(0, arrayLength-i-1):
			if array[j] > array[j+1]:
				array[j], array[j+1] = array[j+1], array[j]


def CutArray(array): # cut the array into pieces
	index = 0
	arrays = []
	while index < len(array):
		cutArray = []
		for i in range(100):
			cutArray.append(array[index+i])
		arrays.append(cutArray)
		index+=100
	return arrays

def MergeSort(array, tempQueue): # merge sort
	if len(array) >1: 
		mid = len(array)//2 #Finding the mid of the array 
		left = array[:mid] # Dividing the array elements  
		right = array[mid:] # into 2 halves 
  
		MergeSort(left, tempQueue) # Sorting the first half 
		MergeSort(right, tempQueue) # Sorting the second half 
  
		i = j = k = 0
		  
		# Copy data to temp arrays L[] and R[] 
		while i < len(left) and j < len(right): 
			if left[i] < right[j]: 
				array[k] = left[i] 
				i+=1
			else: 
				array[k] = right[j] 
				j+=1
			k+=1
		  
		# Checking if any element was left 
		while i < len(left): 
			array[k] = left[i] 
			i+=1
			k+=1
		  
		while j < len(right): 
			array[k] = right[j] 
			j+=1
			k+=1

def main():
	fileNumber = input("Please enter the number of data? (1w, 10w, 50w, 100w)\n")
	fileName = input("Please enter the number of the function? (1, 2, 3, 4)\n")
	inputFile = open(fileNumber+fileName+".txt", 'r')
	whichFunctionToUse = int(inputFile.readline())
	array = []
	tempQueue = Queue()

	for n in inputFile.read().split():
		array.append(int(n))
	
	if whichFunctionToUse == 1:
		startTime = time.time()
		print("Running function 1...")
		BubbleSort(array, tempQueue)
		#print(array)

	elif whichFunctionToUse == 2:
		startTime = time.time()
		print("Running function 2...")
		cutArrays = CutArray(array)
		bubbleThreads = []
		mergeThreads = []
		for singleCutArray in cutArrays: # create bubble sort threads
			bubbleThread = threading.Thread(target=BubbleSort, args=(singleCutArray, tempQueue))
			bubbleThread.start()
			bubbleThreads.append(bubbleThread)

		for thread in bubbleThreads: # join threads
			thread.join()
			
		mergeIndex = 0
		mergeLayer = len(cutArrays) // 2
		while mergeLayer > 1:
			for i in range(mergeLayer):
				twoArray = cutArrays[mergeIndex]+cutArrays[mergeIndex+1]
				mergeThread = threading.Thread(target=MergeSort, args=(twoArray, tempQueue))
				mergeThread.start()
				mergeThreads.append(mergeThread)
				mergeIndex+=2
			mergeLayer //= 2

		for thread in mergeThreads: # join threads
			thread.join()

	elif whichFunctionToUse == 4:
		startTime = time.time()
		print("Running function 4...")
		cutArrays = CutArray(array)
		for arrays in cutArrays:
			BubbleSort(arrays, tempQueue)
		
	inputFile.close()
	endTime = time.time()
	print("CPU process time: ", endTime-startTime, " sec")

if __name__ == "__main__":
	main()