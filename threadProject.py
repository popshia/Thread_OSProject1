import time
import threading
import multiprocessing
import queue

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

def CutArrayProcess(array, cut): # cut the array into pieces using processs
	index = 0
	partition = int(len(array)/cut)
	arrays = multiprocessing.Manager().list()
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

def BubbleForThread(cutArrays, tempQueue): # bubble sort using threads
	bubbleThreads = []
	for singleCutArray in cutArrays: # create bubble sort threads
		bubbleThread = threading.Thread(target=BubbleSort, args=(singleCutArray, tempQueue))
		bubbleThread.start()
		bubbleThreads.append(bubbleThread)

	for thread in bubbleThreads: # join threads
		thread.join()

def BubbleForProcess(cutArrays, tempQueue): # bubble sort using processs
	bubbleProcessS = []
	for i in range(len(cutArrays)): # create bubble sort processs
		bubbleProcess = multiprocessing.Process(target=BubbleSort, args=(cutArrays[i], tempQueue))
		bubbleProcess.start()
		bubbleProcessS.append(bubbleProcess)
		cutArrays[i] = tempQueue.get()

	for process in bubbleProcessS: # join process
		process.join()

def MergeForThread(cutArrays, tempQueue): # merge the cut arrays using threads
	mergeThreads = []
	for _ in range(len(cutArrays)-1):
		mergeThread = threading.Thread(target=MergeSortForThread, args=(cutArrays, tempQueue))
		mergeThread.start()
		mergeThreads.append(mergeThread)
	
	for thread in mergeThreads:
		thread.join()

	while len(cutArrays)>1:
		MergeSortForThread(cutArrays, tempQueue)

def MergeForProcess(cutArrays, tempQueue): # merge the cut arrays using processs
	mergeProcessS = []

	for _ in range(len(cutArrays)-1):
		mergeProcess = multiprocessing.Process(target=MergeSortForProcess, args=(cutArrays, tempQueue))
		mergeProcess.start()
		mergeProcessS.append(mergeProcess)
		cutArrays.append(tempQueue.get())

	for process in mergeProcessS: # join threads
		process.join()

	while len(cutArrays)>1:
		MergeSortForProcess(cutArrays, tempQueue)
		cutArrays.append(tempQueue.get())

def MergeSortForThread(cutArray, tempQueue): # merge sort the cut arrays using thread
	leftArray = cutArray.pop(0)
	rightArray = cutArray.pop(0)
	mergeArray = []

	while len(leftArray)>0 or len(rightArray)>0:
		if len(leftArray) == 0:
			mergeArray.append(rightArray.pop(0))
		elif len(rightArray) == 0:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] > rightArray[0]:
			mergeArray.append(rightArray.pop(0))
		elif leftArray[0] < rightArray[0]:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] == rightArray[0]:
			mergeArray.append(leftArray.pop(0))

	cutArray.append(mergeArray)

def MergeSortForProcess(cutArray, tempQueue): # merge sort the cut arrays using process
	leftArray = cutArray.pop(0)
	rightArray = cutArray.pop(0)
	mergeArray = []

	while len(leftArray)>0 or len(rightArray)>0:
		if len(leftArray) == 0:
			mergeArray.append(rightArray.pop(0))
		elif len(rightArray) == 0:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] > rightArray[0]:
			mergeArray.append(rightArray.pop(0))
		elif leftArray[0] < rightArray[0]:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] == rightArray[0]:
			mergeArray.append(leftArray.pop(0))

	tempQueue.put(mergeArray)

def Merge(cutArray, tempQueue): # compare & merge two arrays
	leftArray = cutArray.pop(0)
	rightArray = cutArray.pop(0)
	mergeArray = []

	while len(leftArray)>0 or len(rightArray)>0:
		if len(leftArray) == 0:
			mergeArray.append(rightArray.pop(0))
		elif len(rightArray) == 0:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] > rightArray[0]:
			mergeArray.append(rightArray.pop(0))
		elif leftArray[0] < rightArray[0]:
			mergeArray.append(leftArray.pop(0))
		elif leftArray[0] == rightArray[0]:
			mergeArray.append(leftArray.pop(0))

	tempQueue.put(mergeArray)
	return mergeArray

def OutputFile(array, fileNumber, fileName, startTime, endTime): # output to file
	output = open(fileNumber+fileName+"_output.txt", 'w')
	output.write(str(array))
	output.write("\nCPU process time: ")
	output.write(str(endTime-startTime))
	output.write(" sec")
	output.close()

def main():
	fileNumber = input("How much data would you like to test? (1w, 10w, 50w, 100w)\n")
	fileName = input("Which function would you like to run? (1, 2, 3, 4)\n")
	inputFile = open(fileNumber+fileName+".txt", 'r')
	whichFunctionToUse = int(inputFile.readline())
	array = []
	tempQueue = queue.Queue()

	for n in inputFile.read().split():
		array.append(int(n))
	
	if whichFunctionToUse == 1:
		startTime = time.time()
		print("Running function 1...")
		BubbleSort(array, tempQueue)
		endTime = time.time()
		OutputFile(array, fileNumber, fileName, startTime, endTime)

	elif whichFunctionToUse == 2:
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 2...")
		cutArrays = CutArray(array, cut)
		BubbleForThread(cutArrays, tempQueue)
		MergeForThread(cutArrays, tempQueue)
		endTime = time.time()
		OutputFile(cutArrays, fileNumber, fileName, startTime, endTime)

	elif whichFunctionToUse == 3:
		with multiprocessing.Manager() as Manager:
			tempQueue = multiprocessing.Queue()
			cut = int(input("How many patitions would you like to cut?\n"))
			startTime = time.time()
			print("Running function 3...")
			cutArrays = CutArrayProcess(array, cut)
			BubbleForProcess(cutArrays, tempQueue)
			MergeForProcess(cutArrays, tempQueue)
			endTime = time.time()
			OutputFile(cutArrays, fileNumber, fileName, startTime, endTime)

	elif whichFunctionToUse == 4:
		cut = int(input("How many patitions would you like to cut?\n"))
		startTime = time.time()
		print("Running function 4...")
		cutArrays = CutArray(array, cut)
		for arrays in cutArrays: # do bubble sort
			BubbleSort(arrays, tempQueue)
		for _ in range(len(cutArrays)-1):
			cutArrays.append(Merge(cutArrays, tempQueue))
		endTime = time.time()
		OutputFile(cutArrays, fileNumber, fileName, startTime, endTime)

	print("CPU process time:", endTime-startTime, "sec")
	inputFile.close()

if __name__ == "__main__":
	main()