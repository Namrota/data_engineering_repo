SELECT * FROM spotify_data;

//1. Which is the longest song released yet? 
-- 16.74 minutes
SELECT song_title, artist, duration_ms, round((duration_ms/ 60000.0), 2) as duration_minutes
FROM spotify_data
group by song_title, artist, duration_ms
order by duration_ms desc
limit 1;

//2. How many songs has Drake sung? 
-- 16 songs
SELECT COUNT(*) 
FROM spotify_data
WHERE artist ilike 'drake';

//3. List those songs with letter ‘Love’ in them.
-- 88 songs
SELECT  song_id, song_title, artist 
FROM spotify_data
WHERE song_title ILIKE '%Love%';

//4. Select songs which have a number in them.
-- 94 rows
SELECT song_title, artist 
FROM spotify_data
WHERE song_title REGEXP '.*[0-9].*';

//5. You have a bachelorette weekend, which songs would you play the most?
-- song_title has 'LOVE'
-- energy greater than 0.8
-- danceability greater than 0.7

SELECT  song_id, song_title, artist 
FROM spotify_data
WHERE song_title ILIKE '%Love%'
    OR (danceability >= 0.7
    AND energy >= 0.8)
ORDER BY song_title;

//6. In a dance battle, which 3 songs would you choose for a dance off?
SELECT  song_title, artist 
FROM spotify_data
WHERE danceability >= 0.9
    AND energy >= 0.8
    AND loudness >= -9.0
ORDER BY energy desc
LIMIT 3;

//7. Which artist has the max songs released?
-- drake with 16 songs
SELECT artist, count(song_title) as number_of_songs
FROM spotify_data
group by artist
ORDER BY number_of_songs desc
LIMIT 1;

//8. Make a ‘break-up’ song list >..< 
SELECT  song_title, artist 
FROM spotify_data
WHERE tempo between 56 and 85 and instrumentalness < 0.3;

