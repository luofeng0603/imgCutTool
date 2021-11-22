# encoding:utf-8
'''
author: luofeng0603
date: 2021-11-19
desc: 给手绘地图层做的切片小工具，自动切图并进行编号，方便前端使用，做了输入提示，根据提示一步步输入即可，兼容win
dependency: python3+, pillow库
version: 1.1
'''
import os,math,sys,time,shutil
try:
    from PIL import Image
except ImportError:
    print(f"未检测到pillow模块，请先使用 pip install pillow 或者 pip3 install pillow 命令进行安装")

def cut_image(image, cutW, cutH, savePath, startPointArr, endPointArr):
	width,height = image.size
	sPointArr = [0,0] if len(startPointArr) == 0 else startPointArr
	ePointArr = [width,height] if len(endPointArr) == 0 else endPointArr
	startW = int(sPointArr[0])
	endW = int(ePointArr[0])
	startH = int(sPointArr[1])
	endH = int(ePointArr[1])
	count_w_f = math.floor((endW - startW)/cutW)
	count_w_c = math.ceil((endW - startW) / cutW)
	count_h_f = math.floor((endH - startH)/cutH)
	count_h_c = math.ceil((endH - startH) / cutH)
	count_w = count_w_f if count_w_f == count_w_c else count_w_c
	count_h = count_h_f if count_h_f == count_h_c else count_h_c
	last_w_s = startW + (count_w - 1) * cutW
	last_w_e = endW
	last_h_s = startH + (count_h - 1) * cutH
	last_h_e = endH
	print(f"\n"
		  f"######################################################################\n"
		  f"准备进行切片，切片区域：起点[{sPointArr[0]},{sPointArr[1]}],终点：[{ePointArr[0]},{ePointArr[1]}]\n"
		  f"将切分成{count_h}行 * {count_w}列 共{count_h * count_w}个图片\n"
		  f"切片存储路径:{savePath}\n")
	for i in range(count_h):
		for j in range(count_w):
			# 最后一行
			if i == count_h:
				# 最后一列
				if j == count_w:
					box = (last_w_s, last_h_s, last_w_e, last_h_e)
				# 不是最后一列
				else:
					box = (j * cutW, last_h_s, (j+1) * cutW, last_h_e)
			# 不是最后一行
			else:
				# 最后一列
				if j == count_w:
					box = (last_w_s, i * cutH, last_w_e, i * cutH)
				# 不是最后一列
				else:
					box = (j * cutW, i * cutH, (j + 1) * cutW, (i + 1) * cutH)
			
			item = image.crop(box)
			item.save(savePath + str(i) + '_' + str(j) + '.png', 'PNG', quality=100)
			print("\r", end="")
			print("切片任务进度: {:.1f}% ".format((i*count_w + j + 1)/(count_w * count_h)*100), "▋" * int((i*count_w + j + 1)/(count_w * count_h)*100/4), end="")
			sys.stdout.flush()
			time.sleep(0.01)

if __name__ == '__main__':
	filePath = input("请输入你要处理的图片路径(绝对或相对都可以)：")
	if filePath == '':
		print("要处理的图片路径不能为空")
		exit()
	if not os.path.isabs(filePath):
		filePath = os.path.abspath(filePath)
	if not os.path.exists(filePath):
		print("你输入的文件不存在，请检查路径！")
		exit()
	img = Image.open(filePath)
	iw, ih = img.size
	print(f"此图片的宽高为：{iw}px,{ih}px")
	savePath = input("请输入你要存放切片的目录路径(不写自动创建slice目录)：")
	osSep = os.sep
	if savePath == '':
		savePath = os.path.dirname(filePath) + osSep + 'slice' + osSep
	else:
		if not os.path.exists(savePath):
			print("你输入的文件夹不存在！")
			exit()
	savePath =  savePath + osSep if savePath[-1] != os.sep else savePath
	iscleanDir = input("是否需要清空：" + savePath + "这个目标目录？[Y/N]: ")
	if iscleanDir == 'Y' or iscleanDir == 'y':
		shutil.rmtree(savePath)
		os.mkdir(savePath)
		print("目标目录清空完成！")
	sliceW = input("请输入切片的宽度，不写默认225(px)：")
	sliceH = input("请输入切面的高度，不写默认225(px)：")
	if not sliceW:
		sliceW = 225
	if not sliceH:
		sliceH = 225
	if int(sliceW) > iw:
		print(f"切片宽度必须小于{iw}px")
		quit()
	if int(sliceH) > ih:
		print(f"切片高度必须小于{ih}px")
		quit()
	startPoint = input("请输入切片开始的坐标,例:0,0(不写默认切整张图片)：")
	endPoint = input("请输入切片结束的坐标,例:2000,3000(不写默认切整张图片)：")
	startPointArr = []
	endPointArr = []
	if startPoint != '':
		startPoint = startPoint.replace("，", ",")
		startPointArr = startPoint.split(",")
		if len(startPointArr) != 2:
			print("开始坐标输入有误！");
			quit()
	if endPoint != '':
		endPoint = endPoint.replace("，", ",")
		endPointArr = endPoint.split(",")
		if len(endPointArr) != 2:
			print("结束坐标输入有误！")
			quit()

	cut_image(img, int(sliceW),int(sliceH), savePath, startPointArr, endPointArr)

	

