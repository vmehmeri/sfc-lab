from nsd_parser import NsdParser
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

class CatalogueEventHandler(FileSystemEventHandler):
    """Logs all the events captured."""

    def on_created(self, event):
        super(CatalogueEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'

        if what == 'directory' or 'yaml/.' in event.src_path or '.yaml' not in event.src_path:
            return

        logging.info("Added %s: %s", what, event.src_path)

        nsd_parser = NsdParser()
        nsd_parser.parseAll()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else 'yaml/'
    print("Monitoring ", path)
    event_handler = CatalogueEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

#test = nsd_parser.NsdParser()
#test.test()