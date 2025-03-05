FROM python:3.12-slim-bookworm

# Create working directory
WORKDIR /project

# Copy and install requirements
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy source files
COPY src ./src
COPY .streamlit .streamlit
COPY pyproject.toml .

CMD ["/bin/bash"]