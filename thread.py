import time
import threading
from queue import Queue

def CutArray(array, cut): # cut the array into pieces
	index = 0
	partition = int(len(array)/cut)
	arrays = []
	while index < len(array):
		cutArray = []
		for i in range(partition):
			cutArray.append(array[index+i])
		arrays.append(cutArray)
		index+=partition
	return arrays

def BubbleSort(array, tempQueue): # bubble sort
	arrayLength = len(array)
	for i in range(arrayLength-1):
		for j in range(0, arrayLength-i-1):
			if array[j] > array[j+1]:
				array[j], array[j+1] = array[j+1], array[j]

def BubbleForThread(cutArrays, tempQueue):
	bubbleThreads = []
	for singleCutArray in cutArrays: # create bubble sort threads
		bubbleThread = threading.Thread(target=BubbleSort, args=(singleCutArray, tempQueue))
		bubbleThread.start()
		bubbleThreads.append(bubbleThread)

	for thread in bubbleThreads: # join threads
		thread.join()

def Merge(cutArrays, tempQueue): # merge the cut arrays
	layer = len(cutArrays)
	while layer >= 1:
		increaseIndex = 1

		if layer == 1:
			while len(cutArrays) > 1:
				print(len(cutArrays))
				addArray = cutArrays.pop(0)+cutArrays.pop(1)
				MergeSort(addArray, tempQueue)
				cutArrays.append(addArray)

		while increaseIndex < layer :
			addArray = cutArrays.pop(0)+cutArrays.pop(1)
			MergeSort(addArray, tempQueue)
			cutArrays.append(addArray)
			increaseIndex+=2

		if layer % 2 != 0:
			cutArrays.append(cutArrays.pop(0))

		layer//=2

def MergeForThread(cutArrays, tempQueue): # merge the cut arrays
	mergeThreads = []
	layer = len(cutArrays)
	while layer >= 1:
		increaseIndex = 1

		if layer == 1:
			while len(cutArrays) > 1:
				addArray = cutArrays.pop(0)+cutArrays.pop(1)
				mergeThread = threading.Thread(target=MergeSort, args=(addArray, tempQueue))
				mergeThread.start()
				mergeThreads.append(mergeThread)
				cutArrays.append(addArray)

		while increaseIndex < layer :
			addArray = cutArrays.pop(0)+cutArrays.pop(1)
			mergeThread = threading.Thread(target=MergeSort, args=(addArray, tempQueue))
			mergeThread.start()
			mergeThreads.append(mergeThread)
			cutArrays.append(addArray)
			increaseIndex+=2

		for thread in mergeThreads: # join threads
			thread.join()

		if layer % 2 != 0:
			cutArrays.append(cutArrays.pop(0))

		layer//=2

def MergeSort(array, tempQueue): # merge sort
	if len(array) > 1: 
		mid = len(array) // 2
		left = array[:mid]
		right = array[mid:]
  
		MergeSort(left, tempQueue)
		MergeSort(right, tempQueue)
  
		i = j = k = 0

		while i < len(left) and j < len(right): 
			if left[i] < right[j]: 
				array[k] = left[i] 
				i+=1
			else: 
				array[k] = right[j] 
				j+=1
			k+=1
		
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
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 2...")
		cutArrays = CutArray(array, cut)
		BubbleForThread(cutArrays, tempQueue)
		MergeForThread(cutArrays, tempQueue)
		n = 0
		for arr in cutArrays:
			n+=1
			#print(arr)
		print(n)
		

	elif whichFunctionToUse == 4:
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 4...")
		cutArrays = CutArray(array, cut)
		for arrays in cutArrays: # do bubble sort
			BubbleSort(arrays, tempQueue)

		Merge(cutArrays, tempQueue) # do merge and sort

		for arr in cutArrays:
			print(arr)

	inputFile.close()
	endTime = time.time()
	print("CPU process time: ", endTime-startTime, " sec")

if __name__ == "__main__":
	main()