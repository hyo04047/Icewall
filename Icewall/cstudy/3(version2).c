#include <stdio.h>
#include <stdlib.h>

int fibo(int n){
	if(n > 2)
		return fibo(n - 1) + fibo(n - 2);
	else
		return 1;

}

int main(){
	int n;
	scanf("%d", &n);

	for(int i = 1; i <= n; i++)
		printf(" %d", fibo(i));

	printf("\n");

	return 0;
}