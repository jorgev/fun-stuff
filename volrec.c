/* volrec.c - a volume recovery tool */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <stdarg.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <hfs/hfs_format.h>

#define BUFSIZE 4096

void err_sys(const char*, ...);
void err_quit(const char*, ...);
static void err_doit(int, int, const char*, va_list);

int main(int argc, char* argv[]) {
    char buf[BUFSIZE];

    // user must supply device name
    if (argc < 2) {
        err_quit("Must provide volume path on command line");
    }

    // open the file
    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        err_sys("Failed to open file");
    }

    // read it for partition info
    ssize_t count = read(fd, buf, sizeof(buf));
    if (count == -1) {
        err_sys("Error reading file");
    }

    // check for valid HFS+ signature, header starts at 1k
    HFSPlusVolumeHeader* phdr = (HFSPlusVolumeHeader*) (buf + 1024);
    if (phdr->signature != 0x2b48) {
        err_quit("Not a valid HFS+ signature");
    }

    close(fd);

    exit(0);
}

void err_sys(const char* fmt, ...) {
    va_list ap;

    va_start(ap, fmt);
    err_doit(1, errno, fmt, ap);
    va_end(ap);
    exit(1);
}

void err_quit(const char* fmt, ...) {
    va_list ap;

    va_start(ap, fmt);
    err_doit(0, 0, fmt, ap);
    va_end(ap);
    exit(1);
}

static void err_doit(int errnoflag, int error, const char* fmt, va_list ap) {
    char buf[BUFSIZE];

    int len = vsnprintf(buf, BUFSIZE - 1, fmt, ap);
    if (errnoflag) {
        snprintf(buf + len, BUFSIZE - len - 1, ": %s", strerror(error));
    }
    strcat(buf, "\n");
    fflush(stdout);
    fputs(buf, stderr);
    fflush(NULL);
}
