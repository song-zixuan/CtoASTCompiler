def judge(arr, len):
     
    i = 0
    j = len - 1
    while i <= j:
         
        if arr[i] != arr[j]:
             
            return False
        i = i + 1
        j = j - 1
    return True
def main( ):
     
    arrsss="aaabbbaaa"
    judge(arrsss,9)
    return 0