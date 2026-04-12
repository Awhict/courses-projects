#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int main(){
    printf("Enter a string (up to 10 letters) in the input dialog window. \n\n");
    char str[100];
    scanf("%s", str);
    if(strlen(str) > 10){
        printf("The string is too long. \n");
        return 0;
    }else{
        int i = 0;
        int test_char = 0;
        for(i = 0; str[i] != '\0'; i++){
            if(isalpha(str[i])){
                test_char += 0;
            }else{
                test_char += 1;
            }
            if(test_char != 0){
                printf("The string contains invalid characters. \n");
                return 0;
            }
        }
        for(i = 0; str[i] != '\0'; i++){
            if(islower(str[i])){
                str[i] = toupper(str[i]);
            }else{
                str[i] = tolower(str[i]);
            }
            //printf("%c\n", str[i]);
        }
        printf("%s\n", str);
        //system("pause");
        return 0;
    } 
}
