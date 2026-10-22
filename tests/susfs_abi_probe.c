/* Read-only ABI smoke test for KSU/SUSFS prctl interception on arm64.
 * No privileged operations or filesystem mutations.
 */
typedef unsigned long ulong;
static long sys_call(long nr, long a0, long a1, long a2, long a3, long a4) {
  register long x0 __asm__("x0")=a0;
  register long x1 __asm__("x1")=a1;
  register long x2 __asm__("x2")=a2;
  register long x3 __asm__("x3")=a3;
  register long x4 __asm__("x4")=a4;
  register long x8 __asm__("x8")=nr;
  __asm__ __volatile__("svc #0" : "+r"(x0) : "r"(x1), "r"(x2), "r"(x3), "r"(x4), "r"(x8) : "memory");
  return x0;
}
static void output(const char *s) {
  long len=0; while(s[len]) len++;
  sys_call(64, 1, (long)s, len, 0, 0);
}
void _start(void) {
  /* Non-mutating option probes; shell uid should be nonzero. */
  long unrelated = sys_call(167, (long)0xDEADBEEE, 0,0,0,0);
  long susfs = sys_call(167, (long)0xDEADBEEF, 0,0,0,0);
  if (unrelated == -22 && susfs == 0) {
    output("PASS: SUSFS 0xDEADBEEF prctl intercepted; invalid neighboring option returns EINVAL.\n");
    sys_call(93,0,0,0,0,0);
  } else {
    if (unrelated != -22) output("WARNING: control prctl did not return EINVAL.\n");
    if (susfs != 0) output("FAIL: SUSFS prctl magic did not return zero.\n");
    sys_call(93,1,0,0,0,0);
  }
  __builtin_unreachable();
}
