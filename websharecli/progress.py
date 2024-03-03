from tqdm import tqdm
import threading

# TODO use ThreadPool to download multiple files in parrallel


class ProgressThread(threading.Thread):

    def __init__(self, queue, thread_pool):
        self.queue = queue
        self.keep_running = True
        super(ProgressThread, self).__init__(args, kwargs)

    # Function to print output to a specific line in the terminal
    @staticmethod
    def print_to_line(line, message):
        print(f"\033[{line};0H{message}\033[K", end='', flush=True)

    # Function to update progress bar and print output
    def update_progress(self, total_threads):
        pbar = tqdm(total=total_threads, position=0)
        lines_printed = 0

        while True:
            # Check if queue has data
            if not queue.empty():
                # Get output from queue
                thread_id, message = queue.get()

                # Print output to specific line
                print_to_line(thread_id + 1, message)
                lines_printed += 1

                # Update progress bar
                pbar.update(1)

                # If all threads have printed output, break the loop
                if lines_printed == total_threads:
                    break