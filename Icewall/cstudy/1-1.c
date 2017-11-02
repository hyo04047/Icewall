#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	int arr[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
	int *p;
	p = arr;
	printf("*p = %d, p = %p\n", *p, p);
	
	*p++;
	printf("*p = %d, p = %p\n", *p, p);
	p--;
	
	*p--;
	printf("*p = %d, p = %p\n", *p, p);
	p++;
	
	(*p)++;
	printf("*p = %d, p = %p\n", *p, p);
	(*p)--;
	
	(*p)--;
	printf("*p = %d, p = %p\n", *p, p);
	(*p)++;

	return 0;
}