import logging
import structlog
from datetime import datetime


def configure_logger():
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    shared_processors = [
        structlog.stdlib.add_log_level,
        # Add a timestamp in ISO 8601 format.
        timestamper,
        # Add callsite parameters.
        structlog.processors.CallsiteParameterAdder(
            parameters=[
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.FUNC_NAME,
                structlog.processors.CallsiteParameter.LINENO,
            ]
        ),
        extract_from_record,
    ]

    structlog.configure(
        processors=[
            # If log level is too low, abort pipeline and throw away log entry.
            structlog.stdlib.filter_by_level,
            # # Add the name of the logger to event dict.
            # structlog.stdlib.add_logger_name,
            # # Add log level to event dict.
            # structlog.stdlib.add_log_level,
            # Perform %-style formatting.
            structlog.stdlib.PositionalArgumentsFormatter(),
            # # Add a timestamp in ISO 8601 format.
            # structlog.processors.TimeStamper(fmt="iso"),
            # If the "stack_info" key in the event dict is true, remove it and
            # render the current stack trace in the "stack" key.
            structlog.processors.StackInfoRenderer(),
            # If the "exc_info" key in the event dict is either true or a
            # sys.exc_info() tuple, remove "exc_info" and render the exception
            # with traceback into the "exception" key.
            structlog.processors.format_exc_info,
            # If some value is in bytes, decode it to a unicode str.
            structlog.processors.UnicodeDecoder(),
            # # Add callsite parameters.
            # structlog.processors.CallsiteParameterAdder(
            #     parameters=[
            #         structlog.processors.CallsiteParameter.FILENAME,
            #         structlog.processors.CallsiteParameter.FUNC_NAME,
            #         structlog.processors.CallsiteParameter.LINENO,
            #     ]
            # ),
            # Render the final event dict as JSON.
            # structlog.processors.JSONRenderer(),
            structlog.dev.ConsoleRenderer(),
        ],
        # `wrapper_class` is the bound logger that you get back from
        # get_logger(). This one imitates the API of `logging.Logger`.
        wrapper_class=structlog.stdlib.BoundLogger,
        # `logger_factory` is used to create wrapped loggers that are used for
        # OUTPUT. This one returns a `logging.Logger`. The final value (a JSON
        # string) from the final processor (`JSONRenderer`) will be passed to
        # the method of the same name as that you've called on the bound logger.
        logger_factory=structlog.stdlib.LoggerFactory(),
        # Effectively freeze configuration after creating the first bound
        # logger.
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        # These run ONLY on `logging` entries that do NOT originate within
        # structlog.
        foreign_pre_chain=shared_processors,
        # These run on ALL entries after the pre_chain is done.
        processors=[
            # Remove _record & _from_structlog.
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.dev.ConsoleRenderer(),
        ],
    )

    handler = logging.StreamHandler()
    # Use OUR `ProcessorFormatter` to format all `logging` entries.
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

    return structlog.get_logger()


def extract_from_record(_, __, event_dict):
    """
    Extract thread and process names and add them to the event dict.
    """
    record = event_dict["_record"]
    event_dict["thread_name"] = record.threadName
    event_dict["process_name"] = record.processName

    return event_dict
