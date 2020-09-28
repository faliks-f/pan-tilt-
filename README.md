<!--
 * @Author: your name
 * @Date: 2020-09-28 15:17:10
 * @LastEditTime: 2020-09-28 19:29:51
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \undefinede:\pan-tilt\pan-tilt-\README.md
 -->
# pan-tilt-
功能：  
1.发送开始数组并等待下位机返回一个数组，否则不开始   
2.利用阈值查找最大的色块，根据最大色块的中心点的位置判断  
3.中间区域被确定为图像的中间五分之一处，即横坐标从五分之二到五分之三，纵坐标从五分之二到五分之三
4.控制左右移动的舵机和上下移动的舵机不会同时动  
5.分析状态:  
>>>1.x和y两个坐标都不在中间roi时，让距离roi远的一个方向靠近，另一个不动   
>>>2.x和y只有一个坐标不在中间roi时，动其中一个   
>>>3.以上两个状态在不管动哪一个舵机，都会让另一个舵机停止  
>>>4.用全局变量记录是否处于移动状态，当x和y都在roi中，如果移动状态为True，就发送停止，如果为False，就不做事  
>>>5.不管怎样的移动，都会将移动状态置为True  