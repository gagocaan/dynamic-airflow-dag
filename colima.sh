#!/bin/bash

# This is a helper script to manage running Airflow locally.

# Fonts utils
RED_COLOR="\033[0;31m"
GREEN_COLOR="\033[0;32m"
YELLOW_COLOR="\033[0;33m"
BOLD=$(tput bold)
NC=$(tput sgr0)

start_airflow() {
    colima stop

    colima start \
        --cpu 4 \
        --memory 8 \
        --mount-type sshfs \
        --mount $(PWD)/dags:w \
        --mount $(PWD)/logs:w \
        --mount $(PWD)/plugins:w

    docker-compose up -d
}

restart_airflow() {
    docker-compose down
    docker-compose up -d
}

deleter_airflow() {
    docker-compose down --volumes --rmi local
}

main() {
    echo -e "${GREEN_COLOR}"
    echo -e "###############################################################################"
    echo -e "################################ Local Aiflow #################################"
    echo -e "######### This is a helper script to manage running Airflow locally. ##########"
    echo -e "###############################################################################"
    echo -e "${NC}"
    echo -e "${GREEN_COLOR} 1. Start Airflow"
    echo -e "${YELLOW_COLOR} 2. Restart Airflow"
    echo -e "${RED_COLOR} 3. Delete Airflow${NC}"
    read -p "Enter your option: " option
    if [ $option = "1" ]; then
        start_airflow
    elif [ $option = "2" ]; then
        restart_airflow
    elif [ $option = "3" ]; then
        deleter_airflow
    else
        echo -e "${RED_COLOR}Invalid option. Exiting...${NC}"
        exit 1
    fi
}

main
