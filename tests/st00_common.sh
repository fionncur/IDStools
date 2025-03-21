#!/bin/bash

execute_scripts() {
    declare -A SCRIPT_STATUS
    declare -A SCRIPT_TIME

    local SCRIPTS=("$@")

    for script in "${SCRIPTS[@]}"; do
        # Set the log file for each script
        executable=$(echo "$script" | awk '{print $1}')
        LOG_FILE="$LOG_DIR/${executable}.log"

        echo "$script" >>"$LOG_DIR/${executable}.log"
        start_time=$(date +%s.%N)
        # Execute the script and redirect both stdout and stderr to the log file
        eval "$script">>"$LOG_FILE" 2>&1
        output=$?
        # Calculate execution time
        end_time=$(date +%s.%N)
        SCRIPT_TIME["$script"]=$(awk -v start="$start_time" -v end="$end_time" 'BEGIN { printf "%.9f", end - start }')

        # Check if the script exited with an error
        if [ "$output" -ne 0 ]; then
            echo "[$script] error occurred!"
            SCRIPT_STATUS["$script"]="FAIL"
            cat "$LOG_FILE"
            echo ""
            break
        else
            echo "[$script] executed successfully!"
            SCRIPT_STATUS["$script"]="PASS"
        fi
        echo "---------------------------------------------------------------------" >> "$LOG_FILE"
    done

    RETURN_STATUS=0
    echo "---------------------------------------------------------------------"
    printf "%-10s %-5s %-50s\n" "Status" "Time" "Script"
    echo "---------------------------------------------------------------------"
    for script in "${SCRIPTS[@]}"; do
        printf "%-10s %.2f %-50s\n" "${SCRIPT_STATUS[$script]}" "${SCRIPT_TIME[$script]}" "$script"
        if [ "${SCRIPT_STATUS[$script]}" == "FAIL" ]; then
            RETURN_STATUS=1
            break
        fi
    done
    echo "---------------------------------------------------------------------"
    return $RETURN_STATUS
}