Minimal reproducible test case for triggering: `RuntimeError: You cannot use AsyncToSync in the same thread as an async event loop - just await the async function directly.` when queuing multiple tasks in celery that call django channels group_send using async_to_sync. Steps to reproduce:

- Run `docker-compose up -d` to bring up django, celery, and other requirements
- Run `docker-compose logs -f worker` to watch celery logs
- In a separate tab run `docker-compose exec python src/manage.py shell` and then following in the shell:
    ```
    from celery_channels_test.celery import sync_send
    sync_send.delay()
    # verify task succeeded normally in celery logs
    for i in range(10):
        sync_send.delay()
    # note `RuntimeError` in celery logs
    ```

Now try using a task that doesn't use channels group_send, and note that there is no error thrown because an event loop is never detected:

- Run `docker-compose up -d` to bring up django, celery, and other requirements
- Run `docker-compose logs -f worker` to watch celery logs
- In a separate tab run `docker-compose exec python src/manage.py shell` and then following in the shell:
    ```
    from celery_channels_test.celery import detect_event_loop
    detect_event_loop.delay()
    # verify task succeeded normally in celery logs
    for i in range(10):
        sync_send.delay()
    # note lack of a ValueError that would be thrown if the event loop is running
    ```
