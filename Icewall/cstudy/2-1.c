#include <stdio.h>
#include <stdlib.h>

typedef struct test{
	int a;
	char *arr;
}test;

int main(){
	test *ptr;
	ptr = (test *)malloc(sizeof(test));
	ptr->arr = (char *)malloc(sizeof(char) * 20);

	ptr->a = 100;
	ptr->arr = "just testing";

	printf("%d %s\n", ptr->a, ptr->arr);

	free(ptr);

	return 0;
}