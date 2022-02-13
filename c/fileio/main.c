#include <stdio.h>
#include <ctype.h>

int main()
{

    const char *fileName = "input.txt";

    FILE *fp, *fp1;

    char ch;

    fp = fopen(fileName, "r");
    if (fp == NULL)
    {
        printf("Error in opening file.\n");
        return -1;
    }

    fp1 = fopen("output.txt", "w");
    if (fp1 == NULL)
    {
        printf("Error in creating output file.\n");
        return -1;
    }

    int n = fgetc(fp) - '0';
    ch = fgetc(fp);

    while ((ch = fgetc(fp)) != EOF)
    {
        if(n<= 0)
            break;
        if(ch == '\n'){
            n--;
        }
        
        if (islower(ch))
        {
            ch = ch - 32;
        }
        putc(ch, fp1);
    }
    fclose(fp);
    fclose(fp1);

    return 0;
}
