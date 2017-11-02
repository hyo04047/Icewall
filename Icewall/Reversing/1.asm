global _start

- register -
ecx : count(for문)
eax, ebx, edx : any
esi, edi : String 같은 squence한 변수의 처음과 끝
esp : program의 stack top

_start:
	sub $esp 16


	push ebp : stack에 ebp 저장
	mov ebp, esp : ebp에 esp 저장, 기존 esp 위치 저장

	sub esp 0x16 : 16byte out
	push 2
	push 1
	push esi : operation 크기를 알고 다음의 위치를 알고 현재 위치/동작 저장
	jump funcA
	(call funcA = push esi + jump funcA)
	...
	(A)

	mov esp ebp : 저장해둔 esp 값 복원
	pop ebp : 원래 ebp 복원
	pop esi

_funcA:     <- int a, int b
	push ebp
	mov ebp, esp
	sub esp, 0x16

	...

	move esp, ebp
	pop ebp
	ret 8 : = pop esi 함수의 끝, (A)위치로 돌아감, 인자 크기만큼 stack return



- call table -
printf, scanf 같은 함수 사용 원할시 system call을 
하는데 table에 함수별로 번호를 붙여서 사용

// printf("abc");
push 4407873 : = 0x434241(cba)
mov eax, 4 : 4번 function(sys_write)
mov ebx, 0
mov ecx, esp : 시작위치 = esp
int 0x80
