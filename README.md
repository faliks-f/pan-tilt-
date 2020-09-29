<!--
 * @Author: your name
 * @Date: 2020-09-28 15:17:10
 * @LastEditTime: 2020-09-29 17:10:40
 * @LastEditors: Please set LastEditors
 * @Description: In User Settings Edit
 * @FilePath: \undefinede:\pan-tilt\pan-tilt-\README.md
 -->
# pan-tilt-
功能：  
1.发送开始数组并等待下位机返回一个数组，否则不开始，开始后openmv的led会显示红色     
2.利用阈值查找最大的色块，根据最大色块的中心点的位置判断  
3.中间区域被确定为图像的中间五分之一处，即横坐标从五分之二到五分之三，纵坐标从五分之二到五分之三
4.现在舵机可以同时动  
5.分析状态:  
>>>1.x和y两个坐标都不在中间roi时，现在可以同时动     
>>>2.x和y只有一个坐标不在中间roi时，动其中一个   
>>>3.以上两个状态在不管动哪一个舵机，都会让另一个舵机停止（现在可以同时动）     
>>>4.用全局变量记录是否处于移动状态，当x和y都在roi中，如果移动状态为True，就发送停止，如果为False，就不做事  
>>>5.不管怎样的移动，都会将移动状态置为True  
>>>6.判重并没有完成，串口通讯协议并没有写 (串口协议已完成)  