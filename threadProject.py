import time
import threading
import multiprocessing
from queue import Queue

def CutArray(array, cut): # cut the array into pieces
	print("Cutting into", cut, "pieces...")
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

def CutArrayProcess(array, cut): # cut the array into pieces using processs
	print("Cutting into", cut, "pieces...")
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
	tempQueue.put(array)

def BubbleForThread(cutArrays, tempQueue): #bubble sort using threads
	bubbleThreads = []
	for singleCutArray in cutArrays: # create bubble sort threads
		bubbleThread = threading.Thread(target=BubbleSort, args=(singleCutArray, tempQueue))
		bubbleThread.start()
		bubbleThreads.append(bubbleThread)

	for thread in bubbleThreads: # join threads
		thread.join()

def BubbleForProcess(cutArrays, tempQueue): #bubble sort using processs
	bubbleProcessS = []
	for i in range(len(cutArrays)): # create bubble sort processs
		bubbleProcess = multiprocessing.Process(target=BubbleSort, args=(cutArrays[i], tempQueue))
		bubbleProcess.start()
		bubbleProcessS.append(bubbleProcess)
		cutArrays[i] = tempQueue.get()

	for process in bubbleProcessS: # join process
		process.join()

def Merge(cutArrays, tempQueue): # merge the cut arrays
	layer = len(cutArrays)//2
	while layer >= 1:
		for _ in range(layer):
			addArray = cutArrays.pop(0)+cutArrays.pop(0)
			MergeSort(addArray, tempQueue)
			cutArrays.append(addArray)

		if len(cutArrays[0])<len(cutArrays[1]):
			cutArrays.append(cutArrays.pop(0))

		if layer == 1:
			while len(cutArrays) > 1:
				addArray = cutArrays.pop(0)+cutArrays.pop(0)
				MergeSort(addArray, tempQueue)
				cutArrays.append(addArray)

		layer//=2

def MergeForThread(cutArrays, tempQueue): # merge the cut arrays using threads
	mergeThreads = []
	layer = len(cutArrays)//2
	while layer >= 1:
		for _ in range(layer):
			addArray = cutArrays.pop(0)+cutArrays.pop(0)
			mergeThread = threading.Thread(target=MergeSort, args=(addArray, tempQueue))
			mergeThread.start()
			mergeThreads.append(mergeThread)
			cutArrays.append(addArray)

		for thread in mergeThreads: # join threads
			thread.join()

		if len(cutArrays[0])<len(cutArrays[1]):
			cutArrays.append(cutArrays.pop(0))

		if layer == 1:
			while len(cutArrays) > 1:
				addArray = cutArrays.pop(0)+cutArrays.pop(0)
				mergeThread = threading.Thread(target=MergeSort, args=(addArray, tempQueue))
				mergeThread.start()
				mergeThreads.append(mergeThread)
				cutArrays.append(addArray)

			for thread in mergeThreads:
				thread.join()

		layer//=2

def MergeForProcess(cutArrays, tempQueue): # merge the cut arrays using processs
	mergeProcessS = []
	layer = len(cutArrays)//2
	while layer >= 1:
		for _ in range(layer):
			addArray = cutArrays.pop(0)+cutArrays.pop(0)
			mergeProcess = multiprocessing.Process(target=MergeSort, args=(addArray, tempQueue))
			mergeProcess.start()
			mergeProcessS.append(mergeProcess)
			cutArrays.append(addArray)

		for process in mergeProcessS: # join threads
			process.join()

		if len(cutArrays[0])<len(cutArrays[1]):
			cutArrays.append(cutArrays.pop(0))

		if layer == 1:
			while len(cutArrays) > 1:
				addArray = cutArrays.pop(0)+cutArrays.pop(0)
				mergeProcess = multiprocessing.Process(target=MergeSort, args=(addArray, tempQueue))
				mergeProcess.start()
				mergeProcessS.append(mergeProcess)
				cutArrays.append(addArray)

			for process in mergeProcessS:
				process.join()

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
	fileNumber = input("How much data would you like to test? (1w, 10w, 50w, 100w)\n")
	fileName = input("Which function would you like to run? (1, 2, 3, 4)\n")
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

	elif whichFunctionToUse == 2:
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 2...")
		cutArrays = CutArray(array, cut)
		BubbleForThread(cutArrays, tempQueue)
		MergeForThread(cutArrays, tempQueue)

	elif whichFunctionToUse == 3:
		with multiprocessing.Manager() as Manager:
			tempQueue = Manager.Queue()
			cutArrays = []
			cut = int(input("How many patitions would you like to cut?\n"))
			startTime = time.time()
			print("Running function 3...")
			cutArrays = CutArrayProcess(array, cut)
			BubbleForProcess(cutArrays, tempQueue)
			MergeForProcess(cutArrays, tempQueue)
			for elements in cutArrays:
				print(elements)


	elif whichFunctionToUse == 4:
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 4...")
		cutArrays = CutArray(array, cut)
		for arrays in cutArrays: # do bubble sort
			BubbleSort(arrays, tempQueue)
		Merge(cutArrays, tempQueue) # do merge and sort

	inputFile.close()
	endTime = time.time()
	print("CPU process time: ", endTime-startTime, " sec")

if __name__ == "__main__":
	main()