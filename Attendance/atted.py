import pytesseract
from PIL import Image
from datetime import date
import re


at_file=open("attendance.csv", "r")
at_lines=at_file.readlines()
at_file.close()
nums=[]
names=[]
for line in at_lines:
	temp=line.split(",")
	nums.append(temp[0])
	names.append(temp[1])
indices=[]
trash=[]
n=int(input("Enter number of pics: "))
ext=input("Enter img extension: ")
for i in range(n):
	temp=pytesseract.image_to_string(Image.open('/home/kakashi/Data/vnit/extras/'+str(i+1)+"."+ext)).split('\n')
	for el in temp:
		txt=el.upper()
		changed=txt.replace("I","1").replace("O","0").replace("S","5").replace("Q","")
		roll_nums=re.findall("BT[1]+[789]+MME[0-9]*",changed)
		if len(roll_nums)!=0:
			for roll_num in roll_nums:
				if len(roll_num)==10:
					try:
						k=nums.index(roll_num)
						if len(indices)==0 or k not in indices:
							indices.append(k)
						else:
							trash.append(roll_num)
					except:
						print("This is not found in roll list:",roll_num)
						trash.append(txt)
						break
				else:
					bt=re.findall("BT[0-9]+",roll_num)
					if len(bt)!=1:
						print(txt,bt)
						raise Exception
					yr=bt[0][-2:]
					roll=re.findall("MME[0-9]+",roll_num)
					if len(roll)!=1:
						print(txt, bt)
						raise Exception
					num=int(roll[0][3:])
					if num>112 and num!=9750:
						final=int(str(num)[-2:])
					else:
						if num==9750:
							final=int(str(num)[:2])
						else:
							final=int(str(num))
					final=str("{:03d}".format(final))
					if len(final)!=3:
						print("This is final {}, roll {}, sample {}, txt {}: ".format(final, roll, sample, txt))
						raise Exception
					final_num="BT"+yr+"MME"+final
					try:
						k=nums.index(final_num)
						if len(indices)==0 or k not in indices:
							indices.append(k)
						else:
							trash.append(txt)
					except:
						print("This is not found in roll list:",txt)
						trash.append(txt)
						break
		else:
			num_removed = txt
			for j in range(1,len(names)):
				b=False
				if j not in indices:
					separated=re.split("[ ,-]",num_removed)
					for elem in separated:
						if len(elem)>2 and elem in names[j]:
							if elem not in "HIMANSHU" and elem not in "DIVYA":
								b=True
								indices.append(j)
								print(elem, "is matched with", names[j], txt)
								break
							else:
								continue
					if b:
						break
			if not b:
				trash.append(txt)

at_file=open("attendance.csv", "w")
print(at_lines[0][:-1]+","+str(date.today()),file=at_file)
for i in range(1,len(at_lines)):
	if i in indices:
		print(at_lines[i][:-1]+","+"1",file=at_file)
	else:
		print(at_lines[i][:-1]+","+"0",file=at_file)


print("\n\nTrash")
for el in trash:
	print(el)
for el in indices:
	print(at_lines[el])
print("Total number of attendees: ", len(indices))
'''
		regex=["BT19MME","BT18MME","BT17MME","BTI9MME","BTI7MME","BTI8MME"]
		index=None
		for r in regex:
			if r in txt:
				index=txt.find(r)
				roll_num=txt[index:index+10]
				
				try:
					indices.append(nums.index(roll_num))
				except:
					print("index error",roll_num, txt)
					index=None
					break
		if index==None:
			matched=False
			for j in range(len(names)):
				if separated != None:
					for sep in separated:
						try:
							if len(sep)>=3 and sep in names[j]:
								if sep == separated[-1]:
									indices.append(j)
									matched=True
							else:
								break
						except:
							break
				if matched:
					break
			if not matched:
				trash.append(txt)

	#print(temp)

lst2 = []
lst3=[]
for el in lst:
	name = el.upper()
	if "BT19MME" in name or "BT18MME" in name or "BT17MME" in name:
		if "BT19MME" in name:
			ind=name.find("BT19MME")
		elif "BT18MME" in name:
			ind=name.find("BT18MME")
		else:
			ind=name.find("BT17MME")
		print(name[ind:ind+10], name)
		lst2.append(name)
	else:
		lst3.append(name)

for el in lst3:
	print(el)
print(len(lst2))'''
