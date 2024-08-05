#!/bin/bash

execute_scripts() {
    declare -A SCRIPT_STATUS
    declare -A SCRIPT_TIME

    local SCRIPTS=("$@")

    # Loop through each script and execute
    for script in "${SCRIPTS[@]}"; do
        # Set the log file for each script
        executable=$(echo "$script" | awk '{print $1}')
        LOG_FILE="$LOG_DIR/${executable}.log"

        echo "$script" >>"$LOG_DIR/${executable}.log"
        start_time_sec=$(date +%s)
        start_time_nsec=$(date +%N)
        # Execute the script and redirect both stdout and stderr to the log file
        eval "$script">>"$LOG_FILE" 2>&1
        output=$?
        # Calculate execution time
        end_time_sec=$(date +%s)
        end_time_nsec=$(date +%N)
        start_time=$((start_time_sec * 1000000000 + start_time_nsec))
        end_time=$((end_time_sec * 1000000000 + end_time_nsec))
        SCRIPT_TIME["$script"]=$((end_time - start_time))

        # Check if the script exited with an error
        if [ "$output" -ne 0 ]; then
            echo "[$script] error occurred!"
            SCRIPT_STATUS["$script"]="FAIL"
            cat "$LOG_FILE"
            echo ""
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
        fi
    done
    echo "---------------------------------------------------------------------"
    return $RETURN_STATUS
}