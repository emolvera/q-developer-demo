#!/bin/bash

# Function to retrieve MySQL password from AWS Secrets Manager
get_mysql_password() {
  local secret_arn="$1"
  json_secret=$(aws secretsmanager get-secret-value --secret-id "$secret_arn" --query SecretString --output text)
  password=$(echo "$json_secret" | jq -r '.password')
  echo $password
}

# Prompt user to choose between MySQL 5.7 or 8.0
echo "\nChoose MySQL cluster to connect:"
echo "1. MySQL 5.7"
echo "2. MySQL 8.0"
read -p "Enter your choice (1 or 2): " mysql_version

# Use a case statement for cleaner conditional logic
case "$mysql_version" in
  1)
    mysql_endpoint="aurora-mysql-5-7-instance-1.cykxuprqcxvu.us-east-1.rds.amazonaws.com"
    mysql_password=$(get_mysql_password "arn:aws:secretsmanager:us-east-1:811400410548:secret:rds!cluster-2d4c782c-f990-4538-a230-2984f61788f0-Dot2nz")
    ;;
  2)
    mysql_endpoint="aurora-mysql-8-0-instance-1.cykxuprqcxvu.us-east-1.rds.amazonaws.com"
    mysql_password=$(get_mysql_password "arn:aws:secretsmanager:us-east-1:811400410548:secret:rds!cluster-753fcaac-2ee9-486b-a718-0987f5505023-QdIzp0")
    ;;
  *)
    echo "Invalid choice. Exiting."
    exit 1
    ;;
esac


# Prompt user to choose between old or new SQL code
#echo "\nChoose SQL query version:"
#echo "1. Old SLQ query"
#echo "2. New SLQ query"
#read -p "Enter your choice (1 or 2): " sql_query_version

#case "$sql_query_version" in
#  1)
#    sql_query_file="./sql_query_mysql_5.7.sql"
#    ;;
#  2)
#    sql_query_file="./sql_query_mysql_8.0.sql"
#    ;;
#  *)
#    echo "Invalid choice. Exiting."
#    exit 1
#    ;;
#esac

mysql -h $mysql_endpoint -P 3306 -u admin -p$mysql_password demo_database
#mysql -h $mysql_endpoint -P 3306 -u admin -p demo_database < $sql_query_file
