#include <stdio.h>
#include <string.h>
#include <stdlib.h>

//문제가 생길 수 있는 줄을 찾고 이유를 쓰세요.

#define BUFFER 32

void before_exit(char * temp, char * temp2) {
	free(temp);
	free(temp2);
}

void login() {
	int password1, password2;

	printf("enter first password : ");
	scanf("%d", password1);
	fflush(stdin);

	printf("enter second password : ");
	scanf("%d", password2);

	printf("Let's check\n");
	if (password1 == 1231555 && password2 == 16543252) {
		printf("Login Success\n");
	}
	else {
		printf("Login Fail\n");
		exit(0);
	}
}

void welcome() {
	char name[100];
	printf("enter you name : ");
	scanf("%100s", name);
	printf("Hello %s\n", name);
}

void start() {
	welcome();
	login();
}

int main(int argc, char ** argv[]) {
	char *temp, *temp2;
	int first, second;
	temp = (char*)malloc(BUFFER);
	temp2 = (char*)malloc(BUFFER);

	if (!temp) {
		printf("temp is not allocated");
		return 0;
	}

	if (!temp2) {
		printf("temp2 is not allocated");
		return 0;
	}

	printf("input string : ");
	scanf("%s", temp);
	printf("input string : %s\n", temp);

	strcpy(temp2, temp);
	printf("copied string : %s\n", temp2);

	start();

	before_exit(temp, temp2);

	return 0;
}
