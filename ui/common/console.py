import io
import sys
import threading
import time
import traceback


stdout_stream = io.StringIO()
stderr_stream = io.StringIO()


class DualStream:
    def __init__(self, stream1, stream2):
        self.stream1 = stream1
        self.stream2 = stream2

    def write(self, text):
        self.stream1.write(text)
        self.stream2.write(text)

    def flush(self):
        self.stream1.flush()
        self.stream2.flush()


def capture_init():
    # Create the dual stream object
    dual_stream = DualStream(sys.stdout, stdout_stream)

    # Redirect stdout and stderr to the dual stream
    sys.stdout = dual_stream
    sys.stderr = dual_stream


def capture_snapshot():
    # Get the captured stdout and stderr
    stdout_value = stdout_stream.getvalue()
    stderr_value = stderr_stream.getvalue()

    return stdout_value, stderr_value


def capture_clear():
    stdout_stream.truncate(0)
    stdout_stream.seek(0)
    stderr_stream.truncate(0)
    stderr_stream.seek(0)


def capture_wrap(func, num_result=1):
    def wrapper(*args, **kwargs):
        # Create a thread to capture the stdout and stderr
        output_thread = threading.Thread(target=capture_init)
        output_thread.start()

        out = ''
        err = ''
        start_time = time.time_ns() // 1_000_000  # Record the start time
        try:
            results = func(*args, **kwargs)  # Execute the decorated function
            # Wait for the thread to finish capturing output
            output_thread.join()

            end_time = time.time_ns() // 1_000_000  # Record the end time
            time_consumed = end_time - start_time  # Calculate the time consumption

            result_text = ""
            result_remain = tuple()

            if results is None:
                results = tuple("")

            if isinstance(results, str):
                result_text = results

            if isinstance(results, tuple) and len(results) > 0:
                result_text = str(results[0])
                result_remain = results[1:]

            out, err = capture_snapshot()
            message = f"[result]:\n{result_text}\n\n"
            message += f"[time consumed]: {time_consumed} milliseconds\n\n"  # Add the time consumption to the message
            if out:
                message += f"[stdout]\n{out}\n\n"
            if err:
                message += f"[stderr]\n{err}\n\n"
            if num_result <= 1:
                return message
            return message, *result_remain
        except Exception:
            output_thread.join()
            out, err = capture_snapshot()
            stack_trace = traceback.format_exc()
            message = ""
            if out:
                message += f"[stdout]\n{out}\n\n"
            if err:
                message += f"[stderr]\n{err}\n\n"
            message += f"[trace]\n{stack_trace}"
            if num_result <= 1:
                return message
            padding = (None,) * (num_result - 1)
            return message, *padding
        finally:
            capture_clear()
            if err:
                print(err)

    return wrapper

