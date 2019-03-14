#include <sys/uio.h>
int main(){
  char part1[] = "part1";
  char part2[] = "part2";
  struct iovec iov[2];
  iov[0].iov_base = part1;
  iov[0].iov_len = strlen(part1);
  iov[1].iov_base = part2;
  iov[1].iov_len = strlen(part2);
  writev(1, iov, 2);
  return 0;
}
