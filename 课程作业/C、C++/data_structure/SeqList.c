#include <stdio.h>
#include <stdlib.h>

#define INIT_CAPACITY 10 // 初始容量

typedef struct {
    int *data;     // 动态数组
    int length;    // 当前长度（元素个数）
    int capacity;  // 当前容量
} SeqList;

// 初始化顺序表
SeqList* InitSeqList() {
    SeqList *L = (SeqList*)malloc(sizeof(SeqList));
    if (!L) return NULL;
    L->data = (int*)malloc(INIT_CAPACITY * sizeof(int));
    if (!L->data) return NULL;
    L->length = 0;
    L->capacity = INIT_CAPACITY;
    return L;
}

// 在位置 i（从1开始）插入元素e
int Insert(SeqList *L, int i, int e) {
    if (i < 1 || i > L->length + 1) return 0; // 位置不合法
    if (L->length == L->capacity) { // 扩容（乘2）
        int new_capacity = L->capacity * 2;
        int *new_data = (int*)realloc(L->data, new_capacity * sizeof(int));
        if (!new_data) return 0; // 扩容失败
        L->data = new_data;
        L->capacity = new_capacity;
    }
    // 元素后移
    for (int j = L->length; j >= i; j--) {
        L->data[j] = L->data[j - 1];
    }
    L->data[i - 1] = e;
    L->length++;
    return 1;
}

// 删除位置i的元素，并通过e返回
int Delete(SeqList *L, int i, int *e) {
    if (i < 1 || i > L->length) return 0; // 位置不合法
    *e = L->data[i - 1];
    // 元素前移
    for (int j = i; j < L->length; j++) {
        L->data[j - 1] = L->data[j];
    }
    L->length--;
    return 1;
}

// 删除顺序表中所有值为e的元素
void RemoveElem(SeqList *L, int e) {
    int slow = 0;  // 定义慢指针 (仅在满足条件时移动)
	for (int fast = 0; fast < L->length; fast++) {  // 定义快指针 (每次都移动)
		if (L->data[fast] != e) {  // 当快指针指向的元素是e时，快指针继续移动而慢指针在原地等待
			// 当快指针指向的元素不是 val 时，将快指针指向的值赋给慢指针指向的位置，慢指针再移动
			L->data[slow++] = L->data[fast];
		}
	}
    L->length = slow;  // 一次循环完成后，slow 的值即为数组中剩余元素数量
}

// 获取位置i的元素
int GetElem(SeqList *L, int i, int *e) {
    if (i < 1 || i > L->length) return 0;
    *e = L->data[i - 1];
    return 1;
}

// 查找元素e的位置，找不到返回0
int LocateElem(SeqList *L, int e) {
    for (int i = 0; i < L->length; i++) {
        if (L->data[i] == e) return i + 1;
    }
    return 0;
}

// 获取长度
int GetLength(SeqList *L) {
    return L->length;
}

// 判空
int IsEmpty(SeqList *L) {
    return L->length == 0;
}

// 遍历顺序表
void Traverse(SeqList *L) {
    for (int i = 0; i < L->length; i++) {
        printf("%d ", L->data[i]);
    }
    printf("\n");
}

// 销毁顺序表
void DestroySeqList(SeqList *L) {
    if (L) {
        free(L->data); // 先释放数组
        free(L);       // 再释放结构体
    }
}

// 输出顺序表当前状态信息
void Info(SeqList *L) {
    printf("Length: %d\n", GetLength(L));
    Traverse(L);
    printf("=========================\n");
}

int main() {
    SeqList *L = InitSeqList();

    for(int i=1; i<=10; i++) Insert(L, i, i); // 在空表中逐个插入1~10
    Info(L);

    int e;
    Delete(L, 4, &e);   // 删除位置1的元素
    printf("Deleted: %d\n", e);
    Info(L);

    Insert(L, 3, 8);
    Insert(L, 5, 8);
    Info(L);
    
    RemoveElem(L, 8);  // 删除所有值为8的元素
    Info(L);

    DestroySeqList(L);  // 释放内存
    return 0;
}