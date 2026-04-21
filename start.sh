#!/bin/bash

INSTANCE_ID="i-0f8d6c7b67615abe5"
IP="13.39.245.55"

echo "Starting Hydrus instance..."
aws ec2 start-instances --instance-ids $INSTANCE_ID --output text > /dev/null

echo "Waiting for instance to be ready..."
aws ec2 wait instance-running --instance-ids $INSTANCE_ID

echo ""
echo "✓ Hydrus is running"
echo ""
echo "  App  → http://$IP:5173"
echo "  API  → http://$IP:5001/api/health"
echo "  SSH  → ssh -i ~/.ssh/hydrus ubuntu@$IP"
