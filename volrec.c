/* volrec.c - a volume recovery tool */

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <stdarg.h>
#include <stdint.h>
#include <string.h>

#define BUFSIZE 4096

struct HFS_BOOT_BLK_HDR {
    uint32_t bbID;
    uint64_t bbEntry;
    uint32_t bbVersion;
    uint32_t bbPageFlags;
    char bbSysName[15];
    char bbShellName[15];
    char bbDbg1Name[15];
    char bbDbg2Name[15];
    char bbScreenName[15];
    char bbHelloName[15];
    char bbScrapName[15];
    uint32_t bbCntFCBs;
    uint32_t bbCntEvts;
    uint64_t bb128KSHeap;
    uint64_t bb256KSHeap;
    uint64_t bbSysHeapSize;
    uint32_t filler;
    uint64_t bbSysHeapExtra;
    uint64_t bbSysHeapFract;
};

void err_sys(const char*, ...);
void err_quit(const char*, ...);
static void err_doit(int, int, const char*, va_list);

int main(int argc, char* argv[]) {
    char buf[BUFSIZE];

    if (argc < 2) {
        err_quit("Must provide volume path on command line");
    }

    int fd = open(argv[1], O_RDONLY);
    if (fd == -1) {
        err_sys("Failed to open file");
    }

    ssize_t count = read(fd, buf, BUFSIZE);
    printf("Count: %zd\n", count);
    struct HFS_BOOT_BLK_HDR* phdr = (struct HFS_BOOT_BLK_HDR*) buf;
    printf("ID: %x\n", phdr->bbID);

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
