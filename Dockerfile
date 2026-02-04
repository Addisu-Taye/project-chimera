FROM python:3.11-slim 
WORKDIR /app 
COPY pyproject.toml . 
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 
COPY . . 
CMD ["bash"] 
