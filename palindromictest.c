int judge(char* arr,int len) {
    int i = 0;
    int j= len -1;
    while(i<=j){
        if(arr[i]!=arr[j]){
            return false;
        }
        i=i+1;
        j=j-1;
    }
    return true;
}

int main(){
    char arrsss[9] = "aaabbbaaa";
    judge(arrsss,9);
    return 0;
}