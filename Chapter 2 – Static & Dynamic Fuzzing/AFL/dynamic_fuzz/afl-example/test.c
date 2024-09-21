#include <stdio.h>
#include <string.h>
 
int main(void){
    char login[16];
    char password[16];
 
    printf("Login : ");
    scanf("%s",login);
    printf("Password : ");
    scanf("%s",password);
 
    if(strcmp(login,"root") == 0){
        if(strcmp(password,"toor") == 0){
            printf("Success.\n");
            return 0;
        }
    }
    printf("Fail.\n");
    return 1;
}
