/////////////////////////////////////////////////////////////////////////////
// Coldsnap is a "Hello World" example of a snapshot fuzzer built in python /
/////////////////////////////////////////////////////////////////////////////
//
// Author: Evan Custodio
//
// Copyright 2020 Evan Custodio
// 
// Permission is hereby granted, free of charge, to any person obtaining
// a copy of this software and associated documentation files (the "Software"),
// to deal in the Software without restriction, including without limitation
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the Software
//  is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included
// in all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
// OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
// IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
// DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
// TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//
// Description: target is our target application for fuzzing

#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h> 

// Our flawless Processing Function
void process(char** argv)
{
	if (strlen(argv[1]) < 8)
		return;
	
	if (argv[1][0] == 'C')
	{
		if (argv[1][1] == 'r')
		{
			if (argv[1][2] == 'A')
			{
				if (argv[1][3] == 'S')
				{
					if (argv[1][4] == 'h')
					{
						if (argv[1][5] == '!')
						{
							if (argv[1][6] == '!')
							{
								// Crash #1 - CrASh!!
								*(char*)(0) = 0;					
							}							
						}							
					}						
				}					
			}			
		}
	}
	if (argv[1][0] == 'B')
	{
		if (argv[1][1] == 'u')
		{
			if (argv[1][2] == 'R')
			{
				if (argv[1][3] == 'N')
				{
					if (argv[1][4] == 'n')
					{
						if (argv[1][5] == '!')
						{
							if (argv[1][6] == '!')
							{
								// Crash #2 - BuRNn!!
								// Make Burn a little harder, must me an 8 char string
								if (strlen(argv[1]) == 8) *(char*)(0) = 0;					
							}							
						}							
					}						
				}					
			}			
		}
	}
}

// Null function to act as our snapshot start point
void startf(void)
{
	__asm__ ( "nop;");
}

// Null function to act as our snapshot end point
void endf(void) 
{
	__asm__ ( "nop;");
}

int main(int argc, char** argv) {

    if (argc < 2) {
        printf("Usage: ./target <argument>\n");
        exit(1);
    }
	// Snapshot start location
	startf();
	// Function under test
	process(argv);
	// Snapshot end location
	endf();
	return 0;
}