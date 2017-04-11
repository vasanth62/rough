//This program is demo for using pthreads with libev.
//Try using Timeout values as large as 1.0 and as small as 0.000001
//and notice the difference in the output

//(c) 2009 debuguo
//(c) 2013 enthusiasticgeek for stack overflow
//Free to distribute and improve the code. Leave credits intact

#include <ev.h>
#include <stdio.h> // for puts
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>

pthread_mutex_t lock;
double timeout = 0.00001;
int timeout_count = 0;
ev_timer t1;
ev_timer t2;

ev_async async_watcher;
int async_count = 0;

struct ev_loop* loop2;
struct ev_loop *loop ;

static void timeout_cb (EV_P_ ev_timer *w, int revents);
void* loop2thread(void* args)
{

    printf("loop2 thread id %u\n", pthread_self());
    sleep(3);
    ev_timer_init(&t1, timeout_cb, 1.0, 1.); // Non repeating timer. The timer starts repeating in the timeout callback function
    t1.data = 1;
    ev_timer_start(loop, &t1);
    ev_async_send(loop, &async_watcher);
    sleep(3);
    ev_timer_init(&t2, timeout_cb, 2.0, 2.); // Non repeating timer. The timer starts repeating in the timeout callback function
    t2.data = 2;
    ev_timer_start(loop, &t2);
    ev_async_send(loop, &async_watcher);
    sleep(100);
    return NULL;
}

static void async_cb (EV_P_ ev_async *w, int revents)
{
    //puts ("async ready");
    printf("async thread id %u\n", pthread_self());
    pthread_mutex_lock(&lock);     //Don't forget locking
    ++async_count;
    printf("async = %d, timeout = %d \n", async_count, timeout_count);
    pthread_mutex_unlock(&lock);   //Don't forget unlocking
}

static void timeout_cb (EV_P_ ev_timer *w, int revents) // Timer callback function
{
    //puts ("timeout");
    printf("timer thread id %u timer %d\n", pthread_self(), w->data);
    pthread_mutex_lock(&lock);     //Don't forget locking
    ++timeout_count;
    pthread_mutex_unlock(&lock);   //Don't forget unlocking
}

int main (int argc, char** argv)
{
    struct timeval a = {};
    struct timeval b;
    struct timeval c = {0};

    if (argc < 2) {
        puts("Timeout value missing.\n./demo <timeout>");
        return -1;
    }
    timeout = atof(argv[1]);

    printf("main thread id %u\n", pthread_self());

    loop = EV_DEFAULT;  //or ev_default_loop (0);
    //Initialize pthread
    pthread_mutex_init(&lock, NULL);
    pthread_t thread;

    //This block is specifically used pre-empting thread (i.e. temporary interruption and suspension of a task, without asking for its cooperation, with the intention to resume that task later.)
    //This takes into account thread safety
    ev_async_init(&async_watcher, async_cb);
    ev_async_start(loop, &async_watcher);
    pthread_create(&thread, NULL, loop2thread, NULL);

    // now wait for events to arrive
    ev_loop(loop, 0);
    //Wait on threads for execution
    pthread_join(thread, NULL);

    pthread_mutex_destroy(&lock);
    return 0;
}
