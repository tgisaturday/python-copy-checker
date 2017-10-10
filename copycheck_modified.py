#컴퓨팅 사고력 카피체크_프로그램
import glob
import chardet
import difflib
import os
import sys


# class for unionfind
class disjointSet:
    def __init__(self):
        self.elements = {}

    def makeSet(self, x):
        if x not in self.elements:
            self.elements[x] = [x, 0]
        return

    def find(self, x):
        if self.elements[x][0][:8] == x:
            return x
        self.elements[x][0] = self.find(self.elements[x][0])
        return self.elements[x][0][:8]

    def union(self, x, y):
        xRoot = self.find(x)
        yRoot = self.find(y)
        if xRoot == yRoot:
            return
        if self.elements[xRoot][1] < self.elements[yRoot][1]:
            self.elements[xRoot][0] = yRoot
        elif self.elements[xRoot][1] > self.elements[yRoot][1]:
            self.elements[yRoot][0] = xRoot
        else:
            self.elements[yRoot][0] = xRoot
            self.elements[xRoot][1] += 1

    def print(self,fd):
        for k, l in sorted(self.elements.items()):
            if l[0][:8] != k:
                new_k = self.find(k)
                self.elements[new_k][0] += ', ' + k
                del self.elements[k]
        for k, l in self.elements.items():
            print(l[0],file=fd)

copy_pair = disjointSet()

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    sys.stdout.flush()


    
folder_name = input("Folder Name : ")
copy_percentage=float(input("Copy Percentage(1~100) : "))/100
print("------------------------------------------------------------")
print("폴더 내 파일의 주석제거를 시작합니다.")
print("------------------------------------------------------------")
file_list = []
if not os.path.isdir('주석제거_'+folder_name):
    os.mkdir('주석제거_'+folder_name)
    
#Pass 1: 모든 파이썬 코드의 주석을 제거하고 이를 주석제거_folder_name에 저장

# folder 내에 있는 모든 파일 이름을 append
for s in glob.glob(folder_name+'/*'):
    file_list.append(s)
file_list.sort()

# i번째 파일에 작업 수행
for i in range(len(file_list)):
     # 사용하고 있는 문자열 set 체크 ex. UTF-8, EUC-KR ...
    eni = chardet.detect(open(file_list[i], 'rb').read())['encoding']
    fr=open(file_list[i],"r",encoding=eni)
    # 해당 문자열 set으로 파일 오픈
    fw=open("주석제거_"+file_list[i],"w",encoding=eni)
    
    flag = False; # block comment 체크용 flag
    for aLine in fr:
        buffer=[] #한 줄 씩 비교하면서 주석을 제외한 내용을 임시 저장하는 buffer

        # block comment시작과 끝 체크
        count1=aLine.count("\'\'\'")
        count2=aLine.count("\"\"\"")
        if (count1 > 0 ) or (count2 > 0):
            if flag == False:
                flag = True
                if count1> 1 or count2 > 1:
                    flag = False
                    continue
                
            elif flag == True:
                flag = False
                continue

        
        if flag == False: #block comment가 아닌 정상적인 code일 경우
            # '#'기호가 나올때까지 해당 문자를 buffer에 append
            
            flag_string = False #string 내부 '#'인지 체크
            
            for c in range(len(aLine)):
                if aLine[c] == '\'' or aLine[c] =='\"':
                    if flag_string == False:
                        flag_string = True
                    else:
                        flag_string = False
                        
                if aLine[c] == '#' and flag_string == False:
                    buffer.append("\n")
                    break
                buffer.append(aLine[c])
            fw.write("".join(buffer))
            
    fr.close()
    fw.close()
    printProgress(i, len(file_list), 'Progress:', 'Complete', 1, 50)
printProgress(len(file_list), len(file_list), 'Progress:', 'Complete', 1, 50)
print("\n------------------------------------------------------------")
print("폴더 내 파일의 주석제거가 끝났습니다. 카피체크를 시작합니다.")
print("------------------------------------------------------------")

#Pass 2: 카피체크 수행

folder_name_removed = '주석제거_'+folder_name
file_list_removed = []

f_result = open(folder_name+"_카피체크_학번.txt",'w')

# folder 내에 있는 모든 파일 이름을 append
for s in glob.glob(folder_name_removed+'/*'):
    file_list_removed.append(s)
file_list_removed.sort()

N=len(file_list_removed)
total=(N * (N-1))/2
count=0


# i번째 파일과 j번째 파일을 비교
for i in range(len(file_list_removed)):
    for j in range(i):
        # 사용하고 있는 문일자열 셋 체크 ex. UTF-8, EUC-KR ...
        eni = chardet.detect(open(file_list_removed[i], 'rb').read())['encoding']
        enj = chardet.detect(open(file_list_removed[j], 'rb').read())['encoding']
        # 해당 encoding으로 open한 뒤 difflib 내의 함수를 통해 차이 체크
        f_r = difflib.SequenceMatcher(
                a=open(file_list_removed[i], encoding=eni).read(),
                b=open(file_list_removed[j], encoding=enj).read()
                ).ratio()
        # 0 <= f <= 1, 0인 경우 완벽하게 다른 파일, 1인 경우 동일한 파일
        # f >= 0.9인 경우 파일 이름을 출력
        # 파일 이름은 folder/filename.py이므로, filename만을 출력하기 위해 replace & split
        if f_r >= copy_percentage:
            file_i=file_list_removed[i].split(']')[-2].split('-')[-1]
            file_j=file_list_removed[j].split(']')[-2].split('-')[-1]
            copy_pair.makeSet(file_i)
            copy_pair.makeSet(file_j)
            copy_pair.union(file_i, file_j)
            break
        count+=1
        printProgress(count, total, 'Progress:', 'Complete', 1, 50)
printProgress(total, total, 'Progress:', 'Complete', 1, 50)
copy_pair.print(f_result)
f_result.close()
print("\n------------------------------------------------------------")
print("카피체크가 끝났습니다. 학번과 비밀번호를 매칭중입니다.")
print("------------------------------------------------------------")
print("잠시만 기다려 주세요.")
#Pass 3: 비밀번호 매칭
password_dict={}
f_dict=open("password.csv","r")
for aLine in f_dict.readlines():
    temp=aLine.replace('\n','').split(',')
    password_dict[temp[0]] = temp[1]
   
f_pass=open(folder_name+"_카피체크_학번.txt","r")
f_final=open(folder_name+"_카피체크_비번.txt","w")

for aLine in f_pass.readlines():
    tmp_pass=aLine.replace('\n','').split(', ')
    print("Copy set : ",end='',file=f_final)
    for i in range(len(tmp_pass)):        
        print(password_dict[tmp_pass[i]],end=' ',file=f_final)
    print(file=f_final)
f_final.close()
print("------------------------------------------------------------")
print("카피체크가 모두 끝났습니다. 종료하려면 아무 키나 누르세요.")
print("------------------------------------------------------------")
input()
