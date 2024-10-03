#!/usr/bin/env bash

repository=$1

envs=(
  "dev"
  "staging"
  "prod"
  "ro-prod"
)

repository_name=$(echo $repository | cut -d'/' -f2)

for env in "${envs[@]}"; do
    echo "Creating environment $env for repository $repository_name"
    # Create environment with GitHub cli
    gh api --method PUT -H "Accept: application/vnd.github+json" repos/$repository/environments/$env

    # Create environment variables
    gh secret set -R $repository --env $env -f secrets/$repository_name-$env.env
    # Create environment secrets
    gh variable set -R $repository --env $env -f variables/$repository_name-$env.env
done

