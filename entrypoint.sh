#!/bin/bash

# Login to wandb if WANDB_API_KEY is set
if [ ! -z "$WANDB_API_KEY" ]; then
    wandb login $WANDB_API_KEY
fi

# Change to Agent-R1 directory
cd /app/Agent-R1

# Run GRPO training script
bash run_grpo.sh 