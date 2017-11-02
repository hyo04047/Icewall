#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
	int x[6] = {1, 2, 3, 4, 5, 6};
	int *p;
	p = &x[2];

	printf("*(p+3) = %d, *(p-2) = %d, *(p+3) * *(p-2) = %d\n", *(p+3), *(p-2), *(p+3) * *(p-2));

	return 0;
}