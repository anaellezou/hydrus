#!/bin/bash

INSTANCE_ID="i-0f8d6c7b67615abe5"

echo "Stopping Hydrus instance..."
aws ec2 stop-instances --instance-ids $INSTANCE_ID --output text > /dev/null

echo "Instance stopped billing paused"
