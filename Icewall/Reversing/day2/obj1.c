#include <cstdio>
#include <cstdlib>

int main(void)
{
	int sum = 0;
	for(int i=1; i<10; ++i) sum += i;
	printf("Hello! I'm %d years old\n", sum);

	return 0;
}