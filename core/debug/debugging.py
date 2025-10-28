import inspect


from core.globals import debug


def log(*messages, level=""):
    if not debug: return

    frame = inspect.currentframe().f_back
    cls_name = None

    if 'self' in frame.f_locals:

        cls_name = type(frame.f_locals['self']).__name__

    prefix = f"[{cls_name}]" if cls_name else "no class?"

    message_str = ' '.join(str(m) for m in messages)
    print(f"{level}{prefix}: {message_str}")
