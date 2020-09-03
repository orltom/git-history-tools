FROM python:3.8.5

RUN pip install --upgrade pip && \
    pip install --no-cache-dir git-history-tools

ENTRYPOINT [ "githistory" ]