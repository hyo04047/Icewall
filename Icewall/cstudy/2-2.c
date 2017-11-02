#include <stdio.h>
#include <stdlib.h>

typedef struct character{
	int c_pos_x;
	int c_pos_y;
}character;

void print(character *coordinate){
	char arr[4][4];
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++)
			arr[j][i] = '0';
	}
	arr[coordinate->c_pos_y][coordinate->c_pos_x] = '1';
	for(int i = 0; i < 4; i++){
		for(int j = 0; j < 4; j++){
			printf("%c ",arr[i][j]);
		}
		printf("\n");
	}
}

int main(){
	character *test;
	test = (character *)malloc(sizeof(test));
	
	test->c_pos_y = 0;
	test->c_pos_x = 0;
	print(test);
	
	while(1){
		printf("x값을 입력해주세요.\n");
		scanf("%d", &(test->c_pos_x));
		if(test->c_pos_x < 0) break;
		
		printf("y값을 입력해주세요.\n");
		scanf("%d", &(test->c_pos_y));
		if(test->c_pos_y < 0) break;

		print(test);
	}

	return 0;
}