CREATE TABLE authors (
    author_id VARCHAR(100) PRIMARY KEY,
    display_name VARCHAR(255),
    platform VARCHAR(20),
    account_created_at TIMESTAMP,
    followers INTEGER,
    following INTEGER
);

CREATE TABLE posts (
    post_id VARCHAR(100) PRIMARY KEY,
    platform VARCHAR(20) NOT NULL,
    source_id VARCHAR(100),
    author_id VARCHAR(100) REFERENCES authors(author_id),
    text TEXT,
    timestamp TIMESTAMP NOT NULL,
    language VARCHAR(20),
    hashtags TEXT[],
    reply_to VARCHAR(100),
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0
);

CREATE TABLE analysis (
    post_id VARCHAR(100) PRIMARY KEY REFERENCES posts(post_id),
    sentiment VARCHAR(20),
    sentiment_confidence FLOAT,
    demographics JSONB,
    topics TEXT[],
    trend_score FLOAT,
    network_features JSONB
);

CREATE TABLE security_log (
    id SERIAL PRIMARY KEY,
    post_id VARCHAR(100) REFERENCES posts(post_id),
    record_hash VARCHAR(64),
    previous_hash VARCHAR(64),
    audit_timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_posts_timestamp ON posts(timestamp);
CREATE INDEX idx_posts_platform ON posts(platform);