#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
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
	The main function of this parallel process program, written using the MPI library.
	
	To encrypt with 8 cores, for example, enter the following on the cmd line:
	mpirun -np 8 bmpsteg -e -m text_to_encrypt.txt -o output.bmp input.bmp
	
	To decrypt:
	mpirun -np 8 bmpsteg -d encrpyted_bitmap.bmp
*/
int main(int argc, char **argv) {

    const int sendTag = 2001;
    const int receiveTag = 2001;
    int ierr,
            processID,
            numProcesses,
            rowsIn,
            rowsOut = 0,
            distributedPixels,
            charsToEncode,
            charsIn,
            charsOut,
            distributedChars,
            root;
    MPI_Status status;

    extern char *optarg;
    extern int optind;
    int c;
    int eflag = 0, dflag = 0, oflag = 0, mflag = 0, rows, cols;
    char *oname, *mname, *message, *fileName, *hiddenMessage, *messageIn;
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

        strcat(message, "\0");
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
            strcat(message, "\0");
        }

        fclose(in);
        free(input);
    }


    if (optind < argc)    /* these are the arguments after the command-line options */
    {
        fileName = argv[optind];
        // Input file provided
        //	printf("flileName = %s\n",fileName);

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
//	printf("File read\n");

	// ~~~~~ ENCRYPTION Code ~~~~~ //
    if (eflag) {

        if (MPI_Init(&argc, &argv) != MPI_SUCCESS) {
            perror("Unable to initialize MPI\n");
            exit(1);
        }
		
        // Creates an MPI pixel Type
        const int nitems = 3;
        int blocklengths[3] = {1, 1, 1};
        MPI_Datatype types[3] = {MPI_UNSIGNED_CHAR, MPI_UNSIGNED_CHAR, MPI_UNSIGNED_CHAR};
        MPI_Datatype mpi_pixel_type;
        MPI_Aint offsets[3];
        offsets[0] = offsetof(PIXEL, r);
        offsets[1] = offsetof(PIXEL, g);
        offsets[2] = offsetof(PIXEL, b);

        if (ierr = MPI_Type_create_struct(nitems, blocklengths, offsets, types, &mpi_pixel_type)) {
            printf("Trouble creating struct\n");
        }
        if (ierr = MPI_Type_commit(&mpi_pixel_type)) {
            printf("Trouble commiting struct\n");
        }

        struct timeval tv1, tv2;
        gettimeofday(&tv1, NULL);
        root = 0;
        if (ierr = MPI_Comm_rank(MPI_COMM_WORLD, &processID)) {
            printf("Trouble ");
        }
        ierr = MPI_Comm_size(MPI_COMM_WORLD, &numProcesses);


        charsToEncode = strlen(message);
        messageIn = (char *) malloc(sizeof(char) * charsToEncode + 1);
        bmp2 = (PIXEL *) malloc(sizeof(PIXEL) * rows * cols);

        if (processID == root) {
            //Preprocess first HEADER_SIZE pixels (encrypt them)
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
 
            printf("\n=== Encoding %d Characters (Multi-Process) ===\n", charsToEncode);

            int x;
            for (x = 0; x < HEADER_SIZE; x++) {
                // Encrypt the number of characters that we are going to be encoding
                int bit = mask1 & (charsToEncode >> ((HEADER_SIZE - 1) - x));
                ((bmp1) + x)->r = ((uint8_t)(bmp1 + x)->r & mask2) | bit;
            }

            // Distributing chars
            int parentPixels = 0;
            int charsParent = 0;
            int slaveID;

            int *pixelOffset = (int *) malloc(sizeof(int) * numProcesses);
            int *charOffset = (int *) malloc(sizeof(int) * numProcesses);
            int iStart = 0;
            int iEnd = 0;

			// Distribute, assign, and send pixels/strings to each child process
            for (slaveID = 0; slaveID < numProcesses; slaveID++) {
                iStart = iEnd;
                iEnd += charsToEncode / numProcesses;
                if (slaveID < charsToEncode % numProcesses) {
                    iEnd++;
                }

                charOffset[slaveID] = iStart;
                pixelOffset[slaveID] = HEADER_SIZE + (iStart * 8);

                if (slaveID != 0) {
                    charsOut = iEnd - iStart;

                    ierr = MPI_Send(&charsOut, 1, MPI_INT, slaveID, sendTag, MPI_COMM_WORLD);
                    ierr = MPI_Send(&message[charOffset[slaveID]], charsOut, MPI_CHAR, slaveID, sendTag,
                                    MPI_COMM_WORLD);

                    rowsOut = (iEnd - iStart) * 8;
                    ierr = MPI_Send(&rowsOut, 1, MPI_INT, slaveID, sendTag, MPI_COMM_WORLD);
                    ierr = MPI_Send(&bmp1[pixelOffset[slaveID]], rowsOut, mpi_pixel_type, slaveID, sendTag,
                                    MPI_COMM_WORLD);
                } else {
                    charsParent = iEnd - iStart;
                    parentPixels = (iEnd - iStart) * 8;
                }
            }

			// Encyrption logic for the parent process
            int chartmp = message[0];
            int octaCounter = 0;

            for (x = HEADER_SIZE; x < (HEADER_SIZE + parentPixels); x++) {
                int bit = (mask1 & (chartmp >> (7 - (octaCounter % 8))));
                ((bmp1) + x)->r = ((uint8_t)(bmp1 + x)->r & mask2) | bit;
                chartmp = message[octaCounter / 8];
                octaCounter++;
            }

            printf("Encrypted %d pixels from parent process (Process #0)\n", parentPixels);

			// Logic for receiving child processes
            int pixelsIn = 0;
            for (slaveID = 1; slaveID < numProcesses; slaveID++) {
                ierr = MPI_Recv(&pixelsIn, 1, MPI_INT, MPI_ANY_SOURCE, slaveID, MPI_COMM_WORLD, &status);

                PIXEL *bmp3 = (PIXEL *) malloc(sizeof(PIXEL) * pixelsIn);
                ierr = MPI_Recv(bmp3, pixelsIn, mpi_pixel_type, status.MPI_SOURCE, slaveID, MPI_COMM_WORLD, &status);

                printf("Recieved %d encrypted pixels from Process #%d\n", pixelsIn, status.MPI_SOURCE);

				// Marges all processes' changes to original bitmap
                for (x = 0; x < pixelsIn; x++) {
                    (bmp1 + pixelOffset[slaveID] + x)->r = (bmp3 + x)->r;
                }
            }

            gettimeofday(&tv2, NULL);
            printf("Total time = %f seconds\n",
                   (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
                   (double) (tv2.tv_sec - tv1.tv_sec));

            free(pixelOffset);
            free(charOffset);

        } else {	// This is logic for encryption for each child process
			
            uint8_t mask1 = 0b00000001,
                    mask2 = 0b11111110;

			// Recives all needed information from parent
            int pixelsIn = 0;
            int charsIn = 0;

            ierr = MPI_Recv(&charsIn, 1, MPI_INT, 0, receiveTag, MPI_COMM_WORLD, &status);
            char *messageIn = (char *) malloc(sizeof(char) * charsIn);

            ierr = MPI_Recv(messageIn, charsIn, MPI_CHAR, 0, receiveTag, MPI_COMM_WORLD, &status);
            ierr = MPI_Recv(&pixelsIn, 1, MPI_INT, 0, receiveTag, MPI_COMM_WORLD, &status);

            PIXEL *bmp2 = (PIXEL *) malloc(sizeof(PIXEL) * pixelsIn);
            ierr = MPI_Recv(bmp2, pixelsIn, mpi_pixel_type, 0, receiveTag, MPI_COMM_WORLD, &status);

			// Begin encryption
            int octaCounter = 0;
            int chartmp = messageIn[0];

            int x = 0;
            for (x = 0; x < pixelsIn; x++) {
                int bit = (mask1 & (chartmp >> (7 - (octaCounter % 8))));
                ((bmp2) + x)->r = ((uint8_t)(bmp2 + x)->r & mask2) | bit;
                chartmp = messageIn[octaCounter / 8];
                octaCounter++;
            }

			// Send encrypted pixels back to parent
            ierr = MPI_Send(&pixelsIn, 1, MPI_INT, root, processID, MPI_COMM_WORLD);
            ierr = MPI_Send(bmp2, pixelsIn, mpi_pixel_type, root, processID, MPI_COMM_WORLD);
        } // ~~~~~ END of Encryption Process ~~~~~ //

        if (oflag && processID == root) {
            // put picture in output file
            // Writing to file...
            if (writeFile(oname, rows, cols, bmp1)) {
                fprintf(stderr, "Unable to write the file: %s\n", oname);
                fprintf(stderr, usage, argv[0]);
                exit(4);
            }
            printf("File written to provided output filename.\n");
        } else if (processID == root) {
            // put picture in console
            // Writing to std out...
            if (writeFile(NULL, rows, cols, bmp1)) {
                fprintf(stderr, "Unable to write to the console.\n");
                fprintf(stderr, usage, argv[0]);
                exit(4);
            }

        }

        free(bmp2);
        free(message);
        free(messageIn);
        MPI_Type_free(&mpi_pixel_type);
		
    } else if (dflag) {  // ~~~~~ Decryption Process ~~~~~ //

        if (MPI_Init(&argc, &argv) != MPI_SUCCESS) {
            perror("Unable to initialize MPI\n");
            exit(1);
        }
		
        // Create an MPI pixel Type
        const int nitems = 3;
        int blocklengths[3] = {1, 1, 1};
        MPI_Datatype types[3] = {MPI_UNSIGNED_CHAR, MPI_UNSIGNED_CHAR, MPI_UNSIGNED_CHAR};
        MPI_Datatype mpi_pixel_type;
        MPI_Aint offsets[3];
        offsets[0] = offsetof(PIXEL, r);
        offsets[1] = offsetof(PIXEL, g);
        offsets[2] = offsetof(PIXEL, b);

        MPI_Type_create_struct(nitems, blocklengths, offsets, types, &mpi_pixel_type);
        MPI_Type_commit(&mpi_pixel_type);

        root = 0;
        ierr = MPI_Comm_rank(MPI_COMM_WORLD, &processID);
        ierr = MPI_Comm_size(MPI_COMM_WORLD, &numProcesses);

        bmp2 = (PIXEL *) malloc(sizeof(PIXEL) * rows * cols);
        messageIn = (char *) malloc(sizeof(char) * power(2, HEADER_SIZE) - 1);

        if (processID == root) {
            struct timeval tv1, tv2;
            gettimeofday(&tv1, NULL);

            int charsToDecode = 0;

            if ((rows <= 0) || (cols <= 0)) {
                fprintf(stderr, "Picture is empty...\nExiting Program.\n");
                exit(4);
            }
            // Pre process the bmp1 array to get the number of chars
            // hidden in the image this wil tell us how to split up
            // the pixel array. Put the nuber in charsToDecode.
            uint8_t mask = 0b00000001;

            int x;
            int messageCount = 0, octaCount = 1, charValue = 0;
            for (x = 0; x < HEADER_SIZE; x++) {
                charsToDecode += (mask & (uint8_t)(bmp1 + x)->r) << ((HEADER_SIZE - 1) - x);
                if (x == (HEADER_SIZE - 1)) {
                    messageCount = charsToDecode;
                }
            }

            printf("\n=== Decoding %d Characters (Multi-Process) ===\n", charsToDecode);

            // Distribute, assign, and send pixels/strings to each child process
            int parentPixels = 0;
            int slaveID;
            int iStart = 0;
            int iEnd = 0;
            int *offset = (int *) malloc(sizeof(int) * numProcesses);
            iStart = HEADER_SIZE;    // Start at header
            iEnd = HEADER_SIZE;
            for (slaveID = 0; slaveID < numProcesses; slaveID++) {
                iStart = iEnd;
                iEnd += (messageCount / numProcesses) * 8;
                if (slaveID < messageCount % numProcesses) {
                    iEnd += 8;
                }

                offset[slaveID] = iStart;

                if (slaveID != 0) {
                    rowsOut = iEnd - iStart;
                    ierr = MPI_Send(&rowsOut, 1, MPI_INT, slaveID, sendTag, MPI_COMM_WORLD);
                    ierr = MPI_Send(&bmp1[iStart], rowsOut, mpi_pixel_type, slaveID, sendTag, MPI_COMM_WORLD);
                } else {
                    parentPixels = iEnd - iStart;
                }

            }

			// Decyrption logic for the parent process 
            octaCount = 0;
            for (x = HEADER_SIZE; x < HEADER_SIZE + parentPixels; x++) {
                charValue += (mask & (uint8_t)(bmp1 + x)->r) << (7 - (octaCount % 8));
                octaCount++;
                if (octaCount % 8 == 0 && octaCount != 0) {
                    hiddenMessage[(octaCount / 8) - 1] = (char) charValue;
                    charValue = 0;
                }
            }
			
            printf("Decrypted %d characters from parent process (Process #0)\n", parentPixels / 8);

			// Logic for receiving child processes
            int charsIn = 0;
            charValue = 0;

            for (slaveID = 1; slaveID < numProcesses; slaveID++) {
                charsIn = 0;
                ierr = MPI_Recv(&charsIn, 1, MPI_INT, MPI_ANY_SOURCE, slaveID, MPI_COMM_WORLD, &status);

                char *messageIn = (char *) malloc(sizeof(char) * charsIn);
                ierr = MPI_Recv(messageIn, charsIn, MPI_CHAR, status.MPI_SOURCE, slaveID, MPI_COMM_WORLD, &status);

                printf("Received %d decrypted characters from Process #%d\n", charsIn, status.MPI_SOURCE);

				// Merge all decrypted characters into one string
                int charOffset = (offset[slaveID] - HEADER_SIZE) / 8;
                for (x = 0; x < charsIn; x++) {
                    hiddenMessage[charOffset + x] = messageIn[x];
                }
            }

			// Terminate the string
            hiddenMessage[charsToDecode] = '\0';

            gettimeofday(&tv2, NULL);
            printf("Total time = %f seconds\n",
                   (double) (tv2.tv_usec - tv1.tv_usec) / 1000000 +
                   (double) (tv2.tv_sec - tv1.tv_sec));

            free(offset);

        } else {  // This is logic for decryption for each child process
            uint8_t mask = 0b00000001;

            int pixelsIn = 0;
            ierr = MPI_Recv(&pixelsIn, 1, MPI_INT, 0, receiveTag, MPI_COMM_WORLD, &status);

            int charsIn = pixelsIn / 8;
            char *message = (char *) malloc(sizeof(char) * charsIn);

            PIXEL *bmp2 = (PIXEL *) malloc(sizeof(PIXEL) * pixelsIn);
            ierr = MPI_Recv(bmp2, pixelsIn, mpi_pixel_type, 0, receiveTag, MPI_COMM_WORLD, &status);

            int x;
            int octaCount = 0, charValue = 0;
            for (x = 0; x < pixelsIn; x++) {
                charValue += (mask & (uint8_t)(bmp2 + x)->r) << (7 - (octaCount % 8));

                octaCount++;
                if (octaCount % 8 == 0 && octaCount != 0) {
                    message[(octaCount / 8) - 1] = (char) charValue;
                    charValue = 0;
                }
            }

            ierr = MPI_Send(&charsIn, 1, MPI_INT, root, processID, MPI_COMM_WORLD);
            ierr = MPI_Send(message, charsIn, MPI_CHAR, root, processID, MPI_COMM_WORLD);
        } // ~~~~~ END of decryption logic ~~~~~ //


        if (oflag && processID == root) {
            //put message in output file
            FILE *out;
            out = fopen(oname, "w");
            if (out == NULL) {
                printf("Error: Could not open %s\n", oname);
                printf(usage, argv[0]);
                exit(3);
            }
            fprintf(out, "The decoded message is:\n%s\n", hiddenMessage);
            fclose(out);
            printf("HiddenMessage written to provided output filename.");
        } else if (processID == root) {
            // Puts message in console
			printf("The decoded message is:%s\n", hiddenMessage);
        }
        MPI_Type_free(&mpi_pixel_type);

        free(hiddenMessage);
        free(bmp2);
        free(messageIn);
    }

	// Finalize MPI and exit
    ierr = MPI_Finalize();
    free(bmp1);
    exit(0);
}

