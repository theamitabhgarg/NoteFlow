-- NoteFlow PostgreSQL practice queries
-- Run these after setting DATABASE_TYPE=postgresql and seeding the database.

-- 1. List all users
SELECT * FROM users;

-- 2. List notes with their authors
SELECT
    n.id,
    n.title,
    u.username AS author
FROM notes n
JOIN users u ON n.user_id = u.id
ORDER BY n.created_at DESC;

-- 3. Count notes per user
SELECT
    u.username,
    COUNT(n.id) AS notes_created
FROM users u
LEFT JOIN notes n ON n.user_id = u.id
GROUP BY u.id, u.username
ORDER BY notes_created DESC;

-- 4. Most popular notes
SELECT
    n.title,
    u.username AS author,
    n.upvote_count
FROM notes n
JOIN users u ON n.user_id = u.id
ORDER BY n.upvote_count DESC;

-- 5. Notes and their comments
SELECT
    n.title,
    c.content,
    u.username AS commenter
FROM comments c
JOIN notes n ON c.note_id = n.id
JOIN users u ON c.user_id = u.id
ORDER BY n.id, c.created_at;

-- 6. Users who have never created a note
SELECT u.username
FROM users u
LEFT JOIN notes n ON n.user_id = u.id
WHERE n.id IS NULL;

-- 7. Users who have given votes
SELECT
    u.username,
    COUNT(v.id) AS votes_given
FROM users u
LEFT JOIN votes v ON v.user_id = u.id
GROUP BY u.id, u.username
ORDER BY votes_given DESC;

-- 8. Notes containing the PostgreSQL tag
SELECT id, title, tags
FROM notes
WHERE 'postgresql' = ANY(tags);

-- 9. Average number of votes per note
SELECT AVG(upvote_count) AS average_votes
FROM notes;

-- 10. Notes with more than one comment
SELECT
    title,
    comment_count
FROM notes
WHERE comment_count > 1
ORDER BY comment_count DESC;
