FROM public.ecr.aws/lambda/python:3.8

COPY app.py requirements.txt ./
COPY build_custom_model.py ./

RUN mkdir -p ./models
COPY models models

RUN mkdir -p ./checkpoint
COPY checkpoint ./checkpoint

RUN python3.8 -m pip install -r requirements.txt -t .

# Command can be overwritten by providing a different command in the template directly.
CMD ["app.lambda_handler"]
