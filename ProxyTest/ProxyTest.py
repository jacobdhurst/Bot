from selenium import webdriver
from queue import Queue
import threading
import signal
import time
import os

# def handler():
#     raise Exception("timeout")
class threadTest(threading.Thread):
    def __init__(self, queue, output):
        threading.Thread.__init__(self)
        self.queue = queue
        self.output = output

    # noinspection PyBroadException
    def run(self):
        while True:
            # grabs host from queue
            proxyToTest = self.queue.get()
            try:
                # signal.signal(signal.SIGALRM, handler)
                # signal.alarm(10)
                # driverLocation = "/usr/local/share/chromedriver"
                driverLocation = "C:/Users/Jacob/Documents/chromedriver.exe"
                # driverLocation = "/Users/danielguzman/Documents/workspace/chromedriver"

                os.environ["webdriver.chrome.driver"] = driverLocation

                options = webdriver.ChromeOptions()
                options.add_argument('--proxy-server=%s' % proxyToTest)
                options.add_experimental_option("detach", True)
                options.set_headless(True)

                driver = webdriver.Chrome(driverLocation, chrome_options=options)
                driver.get("http://google.com")
                if driver.title == "Google":
                    # print ("Success:", proxyToTest)
                    self.output.append(("Success:", proxyToTest))
                else:
                    raise Exception("Uh...")
                driver.close()
            except:
                # print ("Failure:", proxyToTest)
                self.output.append(("Failure:", proxyToTest))
            # signals to queue job is done
            self.queue.task_done()


def main():
    output = []
    input_file = 'FilteredProxyList.txt'
    queue = Queue()

    start = time.clock()
    # spawn a pool of threads, and pass them queue instance
    for i in range(50):  # 50 threads
        t = threadTest(queue, output)
        t.setDaemon(True)
        t.start()

    hosts = [host.strip() for host in open(input_file).readlines()]
    # populate queue with data
    for host in hosts:
        queue.put(host)

    # wait on the queue until everything has been processed
    queue.join()

    for proxyToTest, host in output:
        print(proxyToTest, host)
    print("Elapsed Time: %lf seconds" % (time.clock() - start))
