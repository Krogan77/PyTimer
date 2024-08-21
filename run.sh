#!/bin/bash

# Runs python script with arguments supplied by user
# configuring the directory and virtual environment as needed.

# Get the path of the current script
script_path=$(realpath "${BASH_SOURCE[0]}")
# Go up two levels to reach the program folder
root_dir=$(dirname "$script_path")

# Retrieves current location
current_dir=""
current_dir=$(pwd)


# Moves to program root directory if not already there.
if [[ "${current_dir:2}" != "${root_dir:2}" ]]; then
	cd "${root_dir}" || { echo "Error: Could not change directory to '${root_dir}'."; return 1; }
	change_directory=true
fi

# Backs up the current virtual environment, if any.
if [[ -n "$VIRTUAL_ENV" ]]; then
	current_env="$VIRTUAL_ENV"
fi

# Activates the program's virtual environment if it is not already active.
if [[ -d "./env" ]]; then
	source "env/Scripts/activate"
fi

# Runs the python script with the arguments passed to this script
python -u "${root_dir}/src/main.py" "$@" | \
	while IFS= read -r line; do
		echo "$line"
	done

# Return to the original directory if it was changed
if [[ "$change_directory" == true ]]; then
	cd "$current_dir" || { echo "Error: Could not change directory to '$current_dir'."; return 1; }
fi

# Reactivates the previous virtual environment if it has been saved
# or deactivates that of the current program.
if [[ -n "$current_env" ]]; then
	source "$current_env/Scripts/activate"
else
	deactivate
fi
