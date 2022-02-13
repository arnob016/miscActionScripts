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

    fp1 = fopen("temp.txt", "w");
    if (fp1 == NULL)
    {
        printf("Error in creating temp file.\n");
        return -1;
    }

    int n = ch = fgetc(fp) - '0';
    ch = fgetc(fp);

    while ((ch = fgetc(fp)) != EOF)
    {
        if (islower(ch))
        {
            ch = ch - 32;
        }
        putc(ch, fp1);
    }
    fclose(fp);
    fclose(fp1);

    rename("temp.txt", "output.txt");

    remove("temp.txt");

    return 0;
}
