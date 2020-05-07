# Thread_OSProject1

1. 使⽤開發環境
  * 作業系統：macOS 10.15.4 Catalina
  * 使⽤軟體：Visual Studio Code
  * 使⽤語⾔：Python

2. 流程
  * 先將input檔讀入⼀個list
  * 再根據檔案開頭選⽤的function去做執⾏
  * 記錄開始時間
  * 第⼀題：直接將讀入資料做Bubble Sort
  * 第⼆題：使⽤者輸入要切的份數（k），切成k份後，以k個thread執⾏Bubble Sort，再以 k-1個thread進⾏Merge Sort
  * 第三題：使⽤者輸入要切的份數（k），切成k份後，以k個process執⾏Bubble Sort，再 以k-1個process進⾏Merge Sort
  * 第四題：使⽤者輸入要切的份數（k），切成k份後，以⼀個process執⾏Bubble Sort， 再以同⼀個process進⾏Merge Sort
  * 記錄結尾時間並印出執⾏時間
  * 將function排序完的資料跟執⾏時間output到⼀個新的檔案
3. 使⽤的資料結構
  * list
  * threading.Thread()
  * queue.Queue()
  * multiprocessing.Process()
  * multiprocessing.Manager().list()
  * multiprocessing.Queue()
4. 完成的功能
  * 全數完成
5. 分析（統一切成1000份）

|          	|       第⼀題 	|     第⼆題 	|     第三題 	|     第四題 	|
|---------:	|-------------:	|-----------:	|-----------:	|-----------:	|
|   ⼀萬筆 	|     7.83 sec 	|   0.17 sec 	|  97.21 sec 	|   0.06 sec 	|
|   ⼗萬筆 	|   990.51 sec 	|   1.59 sec 	| 104.63 sec 	|   1.66 sec 	|
| 五⼗萬筆 	| 30191.67 sec 	|  39.38 sec 	| 133.21 sec 	|  37.31 sec 	|
| ⼀百萬筆 	| 61408.25 sec 	| 151.41 sec 	| 255.05 sec 	| 169.69 sec 	|

![alt text](https://github.com/popshia/Thread_OSProject1/blob/master/chart.png)
