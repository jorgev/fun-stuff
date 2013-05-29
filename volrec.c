/* volrec.c - a volume recovery tool */

#include <stdio.h>
#include <fcntl.h>
#include <errno.h>
#include <stdarg.h>

#define BUFSIZE 4096

void err_sys(const char*, ...);
void err_exit(int error, const char*, ...);
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

    // read the mft
    read(fd, buf, BUFSIZE);

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
