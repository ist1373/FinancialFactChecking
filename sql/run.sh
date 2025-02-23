
docker run \
  --name fact-checker-sql-container \
  -e MYSQL_ROOT_PASSWORD=fact_checking_root_pass \
  -e MYSQL_DATABASE=fact_checking_db \
  -e MYSQL_USER=admin \
  -e MYSQL_PASSWORD=addmin_pass \
  -v fact-checker-mysql-data:/var/lib/mysql \
  -p 3306:3306 \
  -d fact-checker-sql-image
 
# fact-checker-network
  # --network fact-checker-network \