#include <windows.h>
#include <tchar.h> 
#include <stdio.h>
#include <strsafe.h>
#include <stdlib.h>
#include <math.h>
#pragma comment(lib, "User32.lib")


//code based on a windows tutorial: https://msdn.microsoft.com/en-us/library/aa365200(v=vs.85).aspx
//also repurposed from cmsc491 malware project

void DisplayErrorBox(LPTSTR lpszFunction);


//this file gets the names of all the files in the "data/" path and stores them in the "files.txt" file
int _tmain(int argc, TCHAR *argv[]) {
   WIN32_FIND_DATA ffd;
   LARGE_INTEGER filesize;
   TCHAR szDir[MAX_PATH];
   size_t length_of_arg;
   HANDLE hFind = INVALID_HANDLE_VALUE;
   DWORD dwError=0;
   
	 //get the current directory
	 int size = GetCurrentDirectory(0, NULL);
	 TCHAR *dir = malloc(sizeof(TCHAR) * 30);
	 GetCurrentDirectory(size, dir);

   // Prepare string for use with FindFile functions.  First, copy the
   // string to a buffer, then append 'data\*' to the directory name.

   StringCchCopy(szDir, MAX_PATH, dir);
   StringCchCat(szDir, MAX_PATH, TEXT("\\data\\*"));
	 
   // Find the first file in the directory.

   hFind = FindFirstFile(szDir, &ffd);

   if (INVALID_HANDLE_VALUE == hFind) 
   {
      DisplayErrorBox(TEXT("FindFirstFile"));
      return dwError;
   } 
   
   //open file handle for output
	 FILE *f = fopen("files.txt", "w");
	 if (f == NULL) {
		 fprintf(stderr, "Error: could not open file\n");
		 exit(1);
	 }

	 //write file name as output
   do
   {
		 //ignore weird input
		 if (strstr(ffd.cFileName, ".jl") == NULL) {
			 continue;
		 }
		 fprintf(f, "%s\n" , ffd.cFileName);
   }
   while (FindNextFile(hFind, &ffd) != 0);
 
   //errors and cleanup
   dwError = GetLastError();
   if (dwError != ERROR_NO_MORE_FILES) 
   {
      DisplayErrorBox(TEXT("FindFirstFile"));
   }
	
		fclose(f);
   FindClose(hFind);

}


void DisplayErrorBox(LPTSTR lpszFunction) 
{ 
    // Retrieve the system error message for the last-error code

    LPVOID lpMsgBuf;
    LPVOID lpDisplayBuf;
    DWORD dw = GetLastError(); 

    FormatMessage(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | 
        FORMAT_MESSAGE_FROM_SYSTEM |
        FORMAT_MESSAGE_IGNORE_INSERTS,
        NULL,
        dw,
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (LPTSTR) &lpMsgBuf,
        0, NULL );

    // Display the error message and clean up

    lpDisplayBuf = (LPVOID)LocalAlloc(LMEM_ZEROINIT, 
        (lstrlen((LPCTSTR)lpMsgBuf)+lstrlen((LPCTSTR)lpszFunction)+40)*sizeof(TCHAR)); 
    StringCchPrintf((LPTSTR)lpDisplayBuf, 
        LocalSize(lpDisplayBuf) / sizeof(TCHAR),
        TEXT("%s failed with error %d: %s"), 
        lpszFunction, dw, lpMsgBuf); 
    MessageBox(NULL, (LPCTSTR)lpDisplayBuf, TEXT("Error"), MB_OK); 

    LocalFree(lpMsgBuf);
    LocalFree(lpDisplayBuf);
}







