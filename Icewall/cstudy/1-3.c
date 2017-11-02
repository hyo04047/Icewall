#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	int n;
	scanf("%d",&n);
	int num = 1;

	//memory allocation
	int **arr;
	arr = (int **)malloc(sizeof(int *) * (n + 1));
	for(int i = 0; i < n; i++){
		arr[i] = (int *)malloc(sizeof(int) * (n + 1));
	}

	//insert numbers
	int x = -1, y = 0, k = 1;
	int index;
	for(index = n; index > 0;){
		for(int i = 0; i < index; i++){
			x += k;
			arr[y][x] = num++;
		}

		index--;

		for(int i = 0; i < index; i++){
			y += k;
			arr[y][x] = num++;
		}

		k *= -1;
	}

	//print
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++){
			printf("%3d ", arr[i][j]);
		}
		printf("\n");
	}

	//free memory
	for(int i = 0; i < n; i++)
		free(arr[i]);
	free(arr);

	return 0;
}