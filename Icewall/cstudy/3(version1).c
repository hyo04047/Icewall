#include <stdio.h>
#include <stdlib.h>

int fibo(int a, int print){
	int k = 0;
	if(a < 2){
		k = 1;
		if(print != 0) printf("%d ", k);
	}

	if(a >= 2){
		if(print != 0) k = fibo(a - 1, 1) + fibo(a - 2, 0);
		if(print == 0) k = fibo(a - 1, 0) + fibo(a - 2, 0);
	}

	if(print != 0)
		printf("%d ", k);

	return k;
}

int main(){
	int a, print;
	scanf("%d", &a);
	if(a > 0){
		fibo(a - 1, 1);
	}
	return 0;
}