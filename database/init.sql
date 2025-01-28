CREATE TABLE vulnerabilities (
                                 id SERIAL PRIMARY KEY,
                                 cve_id VARCHAR(50) NOT NULL,
                                 description TEXT,
                                 severity VARCHAR(20),
                                 status VARCHAR(20),
                                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                 frontend_key VARCHAR(50) UNIQUE;
);

