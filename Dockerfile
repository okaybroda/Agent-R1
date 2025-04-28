# Use the recommended verl Docker image as base
FROM whatcanyousee/verl:vemlp-th2.4.0-cu124-vllm0.6.3-ray2.10-te2.0-megatron0.11.0-v0.0.6

# Set working directory
WORKDIR /app

# Install additional dependencies
RUN pip3 install wandb FlagEmbedding faiss-cpu

# Clone Agent-R1 repository
RUN git clone https://github.com/0russwest0/Agent-R1.git && \
    cd Agent-R1 && \
    git submodule update --init --recursive

# Set environment variables
ENV PYTHONPATH=/app/Agent-R1:$PYTHONPATH
ENV PYTHONUNBUFFERED=1

# Create data directory and preprocess math dataset
RUN mkdir -p /app/data/math && \
    cd /app/Agent-R1 && \
    python examples/data_preprocess/math.py --local_dir /app/data/gsm8k

# Copy entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"] 