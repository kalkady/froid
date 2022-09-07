FROM  python:3.7-alpine

ARG DEVELOPMENT=false

LABEL maintainer=achillesrasquinha@gmail.com

ENV FROID_PATH=/froid

RUN apk add --no-cache \
        bash \
        git \
    && mkdir -p $FROID_PATH && \
    pip install --upgrade pip

COPY . $FROID_PATH
COPY ./docker/entrypoint.sh /entrypoint
RUN sed -i 's/\r//' /entrypoint \
	&& chmod +x /entrypoint

WORKDIR $FROID_PATH

RUN if [[ "${DEVELOPMENT}" ]]; then \
        pip install -r ./requirements-dev.txt; \
        python setup.py develop; \
    else \
        pip install -r ./requirements.txt; \
        python setup.py install; \
    fi

ENTRYPOINT ["/entrypoint"]

CMD ["froid"]