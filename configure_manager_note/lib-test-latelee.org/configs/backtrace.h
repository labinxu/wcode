#ifndef _BACKTRACE_H
#define _BACKTRACE_H

/* Even complicated programs rather seldom have a nesting 
 * level of more than, say, 50 and with 200 possible entries
 * probably all programs should be covered. -- from glibc manual
 */
/* here, we let it be 30 */
#define NEST	30
void print_trace(int sig);
void print_trace_fd(int sig);
void print_trace_file(int sig);

#endif /* _BACKTRACE_H */