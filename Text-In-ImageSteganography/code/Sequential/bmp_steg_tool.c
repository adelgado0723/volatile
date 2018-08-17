#include <stdio.h>
#include <stdlib.h>
// #include <mpi.h>
#include "bmplib.h"
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/time.h>

// This is the size of out encryption/decryption header in bits. The first HEADER_SIZE bits
// in the image is used to state the number of characters encrypted onto the bitmap. 
static const int HEADER_SIZE = 20;

/**
	A simple recursive power function.

	@param base the number to be exponentiated.
	@param exponent the number of times to multiply the base
*/
int power(int base, int exponent) {
    if (exponent == 0) {
        return 1;
    } else {
        return base * power(base, exponent - 1);
    }
}

/**
	Decrpyts an image that was encrypted with a character string by thuis program.
	
	@param bmp1 the bitmap to be decrypted
	@param rows the number of rows the bitmap has
	@param cols the number of columns the bitmap has
	@param hiddenMessage the output string of the decryption process
*/
int decrypt(PIXEL *bmp1, int rows, int cols, char *hiddenMessage) {

    int charsToDecode = 0;

    if ((rows <= 0) || (cols <= 0)) {
        return -1;
    }
    // Pre process the bmp1 array to get the number of chars
    // hidden in the image this wil tell us how to split up
    // the pixel array. Put the number in charsToDecode.
    uint8_t mask = 0b00000001;

    int x;
    int messageCount = 0, octaCount = 0, charValue = 0;
    for (x = 0; x < rows * cols; x++) {
        // Decrypt the number of characters we will be decoding
        if (x < HEADER_SIZE) {
            charsToDecode += (mask & (uint8_t)(bmp1 + x)->r) << ((HEADER_SIZE - 1) - x);

            if (x == (HEADER_SIZE - 1)) {
                messageCount = charsToDecode;
                printf("\n=== Decoding %d Characters (Single Process) ===\n", charsToDecode);
            }
        } else if (messageCount > 0) {

            charValue += (mask & (uint8_t)(bmp1 + x)->r) << (7 - (octaCount % 8));

            octaCount++;
            if (octaCount % 8 == 0 && octaCount != 0) {
                hiddenMessage[(octaCount / 8) - 1] = (char) charValue;
                messageCount--;
                charValue = 0;
            }
        } else // break
        {
            x = rows * cols;
        }

    }

    // Terminate the string
    hiddenMessage[charsToDecode] = '\0';

    return 0;
}


/**
	Decrpyts an image that was encrypted with a character string by thuis program.
	
	@param bmp1 the bitmap to be decrypted
	@param rows the number of rows the bitmap has
	@param cols the number of columns the bitmap has
	@param message the string to encrypt onto bmp1
	@param bmp2 the output image of the encryption.
*/
int encrypt(PIXEL *bmp1, int rows, int cols, char *message, PIXEL **bmp2) {

    int charsToEncode = strlen(message);

    if ((rows <= 0) || (cols <= 0) || charsToEncode * 8 + HEADER_SIZE > rows * cols) {
        fprintf(stderr, "Picture is empty or too small for the message...\nExiting Program.\n");
        exit(4);
    }

    if (charsToEncode > rows * cols / 8 || charsToEncode > power(2, HEADER_SIZE) - 1) {
        // The message is too big
        fprintf(stderr, "The message is too big...\nExiting Program.\n");
        exit(5);
    }

    // Pre process the bmp2 array to write the number of characters
    // that are going to be encoded into the last bit of the red
    // value for the first HEADER_SIZE pixels
    uint8_t mask1 = 0b00000001,
            mask2 = 0b11111110;

    printf("\n=== Encoding %d Characters (Single Process) ===\n", charsToEncode);

    int x;
    int chartmp = message[0];
    int octaCounter = 0;

    for (x = 0; x < HEADER_SIZE; x++) {
        // Encrypt the number of characters that we are going to be encoding
        int bit = mask1 & (charsToEncode >> ((HEADER_SIZE - 1) - x));
        ((bmp1) + x)->r = ((uint8_t)(bmp1 + x)->r & mask2) | bit;
    }

    // Encrypt all the characters in the message string
    for (x = HEADER_SIZE; x < (8 * charsToEncode) + HEADER_SIZE; x++) {
        int bit = (mask1 & (chartmp >> (7 - (octaCounter % 8))));
        ((bmp1) + x)->r = ((uint8_t)(bmp1 + x)->r & mask2) | bit;
        // printf("Red pixel #%c at position # %d = %d\n", (char) chartmp, x, ((bmp1) + x)->r);

        chartmp = message[octaCounter / 8];
        octaCounter++;
    }
    return 0;
}

int main(int argc, char **argv) {
    extern char *optarg;
    extern int optind;
    int c;
    int eflag = 0, dflag = 0, oflag = 0, mflag = 0, rows, cols;
    char *oname, *mname, *message, *fileName, *hiddenMessage;
    PIXEL *bmp1;
    PIXEL *bmp2;
    static char usage[] = "usage: %s [-e | -d] [-m messageFile] [-o ouput_file]  [image_file]\n";

    while ((c = getopt(argc, argv, "deo:m:")) != -1)
        switch (c) {
            case 'd':
                dflag = 1;
                if (!(hiddenMessage = (char *) malloc(sizeof(char) * power(2, HEADER_SIZE) - 1))) {
                    exit(5);        //Out of Memory Error
                }
                break;
            case 'e':
                eflag = 1;
                if (!(message = (char *) malloc(sizeof(char) * power(2, HEADER_SIZE) - 1))) {
                    exit(5);        //Out of Memory Error
                }
                break;
            case 'o':
                oflag = 1;
                oname = optarg;
                break;
            case 'm':
                mflag = 1;
                mname = optarg;
                break;
            case '?':
                fprintf(stderr, usage, argv[0]);
        }


    if (eflag && dflag) {
        fprintf(stderr, "Error: cannot have both -e and -d flags at the same time.\n");
        fprintf(stderr, usage, argv[0]);
        exit(1);
    }

    if (eflag && !mflag) {
        // prompt user for message to encrypt
        printf("Please enter a message to encode:\n");
        if (fgets(message, sizeof(char) * power(2, HEADER_SIZE) - 1, stdin) == NULL) {
            fprintf(stderr, "Error reading message from console.\n");
        }
    } else if (mflag && !dflag) {
        FILE *in;
        char *input;
        if (!(input = (char *) malloc(sizeof(char) * 200))) {
            exit(5);        //Out of Memory Error
        }

        if ((in = fopen(mname, "r")) == NULL) {
            //Error, couldn't open file.
            printf("Error: Could not open %s\n", mname);
            printf(usage, argv[0]);
            exit(3);
        } else {
            while (fgets(input, sizeof(char) * 200, in) != NULL) {
                strcat(message, input);
            }
            //	strcat(message, "\n");
        }
        fclose(in);
        free(input);
        //	printf("Your message is:\n%s", message);
    }


    if (optind < argc)    /* these are the arguments after the command-line options */
    {
        fileName = argv[optind];

        // Input file is provided.
        if (readFile(fileName, &rows, &cols, &bmp1)) {
            fprintf(stderr, "Unable to read the file: %s\n", fileName);
            fprintf(stderr, usage, argv[0]);
            exit(4);
        }
    } else {
        // Read binary file from console
        if (readFile(NULL, &rows, &cols, &bmp1)) {
            fprintf(stderr, "Unable to read from the console.\n");
            fprintf(stderr, usage, argv[0]);
            exit(4);
        }
    }

    printf("File read.\n");

    if (eflag) {
        // encrypt picture
        struct timeval tv1, tv2;
        gettimeofday(&tv1, NULL);
        encrypt(bmp1, rows, cols, message, &bmp2);
        gettimeofday(&tv2, NULL);

        printf("Total time = %f seconds\n",
               (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
               (double) (tv2.tv_sec - tv1.tv_sec));
        free(message);

        if (oflag) {
            // put picture in output file
            // Writing to file...
            if (writeFile(oname, rows, cols, bmp1)) {
                fprintf(stderr, "Unable to write the file: %s\n", oname);
                fprintf(stderr, usage, argv[0]);
                exit(4);
            }
            printf("File encrypted as %s\n", oname);
        } else {
            //put picture in console
            // Writing to std out...
            if (writeFile(NULL, rows, cols, bmp1)) {
                fprintf(stderr, "Unable to write to the console.\n");
                fprintf(stderr, usage, argv[0]);
                exit(4);
            }

        }
    } else if (dflag) {
        //decrypt picture
        struct timeval tv1, tv2;
        gettimeofday(&tv1, NULL);
        decrypt(bmp1, rows, cols, hiddenMessage);
        gettimeofday(&tv2, NULL);

        printf("Total time = %f seconds\n",
               (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
               (double) (tv2.tv_sec - tv1.tv_sec));

        if (oflag) {
            // Puts message in output file
            FILE *out;
            out = fopen(oname, "w");
            if (out == NULL) {
                printf("Error: Could not open %s\n", oname);
                printf(usage, argv[0]);
                exit(3);
            }
            fprintf(out, "The decoded message is:\n%s \n\n", hiddenMessage);
            fclose(out);
            printf("HiddenMessage written to provided output filename.");
        } else {
            // Puts message in console
            printf("The decoded message is: \n%s\n", hiddenMessage);
            int i = 0;
        }

        free(hiddenMessage);
    }

    free(bmp1);
    exit(0);
}


