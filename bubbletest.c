int* sort(int arr[],int len) {
    int i = 0;
    while(i<len){
        int j = i + 1;
        while(j<len){
            if(arr[i]<arr[j]){
                int tmp=arr[i];
                arr[i]=arr[j];
                arr[j]=tmp;
            }
            else
            {
                return;
            }
            j=j+1;
        }
        i=i+1;
    }
    return arr;
}

int main(){
    int arrsss[9] = {4,6,1,2,8,0,67,3,5};
    arrsss=sort(arrsss,9);
    return 0;
}