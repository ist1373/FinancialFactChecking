# Use the official Neo4j image
FROM mysql:latest

# Set environment variables
ENV MYSQL_ROOT_PASSWORD=fact_checking_root_pass
ENV MYSQL_DATABASE=fact_checking_db
ENV MYSQL_USER=admin
ENV MYSQL_PASSWORD=addmin_pass

# Expose the MySQL port
EXPOSE 3306

# Copy initialization script (if any) to container
# COPY ./init.sql /docker-entrypoint-initdb.d/

# Default command
CMD ["mysqld"]