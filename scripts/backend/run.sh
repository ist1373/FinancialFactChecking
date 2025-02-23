docker run -p 8000:8000 \
  --network fact-checker-network -d\
  -e DATABASE_URL="mysql+pymysql://admin:addmin_pass@fact-checker-sql-container:3306/fact_checking_db" \
  --name fact-checker-backend-container fact-checker-backend-image

#fact-checker-network
#fact-checker-sql-container