<?php

require_once('database.php');

function timestampToDate($timestamp) {
    $dt = new DateTime("@$timestamp");
    return $dt->format('Y-m-d');
}

function dateToTimestamp($date) {
    return strtotime($date);
}

function getMovies($start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM movies ORDER BY id DESC LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $movies = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $movies[] = $row;
    }
    return $movies;
}

function getMovie($movieId) {
    global $mysqli;
    $sql = "SELECT * FROM movies WHERE id = ${movieId};";
    $result = $mysqli->query($sql);
    $movie = mysqli_fetch_assoc($result);
    return $movie;
}

function getMovieRatings($movieId, $start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM ratings WHERE movieId = ${movieId} ORDER BY movieId LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $ratings = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $ratings[] = $row;
    }
    return $ratings;
}

function getMovieTags($movieId, $start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM tags WHERE movieId = ${movieId} ORDER BY movieId LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $ratings = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $ratings[] = $row;
    }
    return $ratings;
}

function updateMovie($id, $title, $genres) {
    global $mysqli;
    $query = "UPDATE movies SET title = '${title}', genres = '${genres}' WHERE id = ${id};";
    mysqli_query($mysqli, $query);
}

function insertMovie($title, $genres) {
    global $mysqli;
    $query = "INSERT INTO movies(title, genres) VALUES ('${title}', '${genres}');";
    mysqli_query($mysqli, $query);
}

function insertRating($userId, $movieId, $rating, $timestamp) {
    global $mysqli;
    $query = "INSERT INTO ratings(userId, movieId, rating, timestamp) VALUES (${userId}, ${movieId}, ${rating}, ${timestamp});";
    mysqli_query($mysqli, $query);
}

function deleteMovie($id) {
    global $mysqli;
    $query = "DELETE FROM movies WHERE id = ${id};";
    mysqli_query($mysqli, $query);
}

// TAGS

function getTags($start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM tags ORDER BY movieId LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $tags = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $tags[] = $row;
    }
    return $tags;
}

function insertTag($userId, $movieId, $tag) {
    global $mysqli;
    $query = "INSERT INTO tags(userId, movieId, tag) VALUES (${userId}, ${movieId}, '${tag}');";
    mysqli_query($mysqli, $query);
}

function deleteTag($userId, $movieId, $tag) {
    global $mysqli;
    $query = "DELETE FROM tags WHERE userId = ${userId} AND movieId = ${movieId} AND tag = '${tag}';";
    mysqli_query($mysqli, $query);
}

// RATINGS
function getRatings($start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM ratings ORDER BY movieId LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $ratings = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $ratings[] = $row;
    }
    return $ratings;
}

function deleteRating($userId, $movieId) {
    global $mysqli;
    $query = "DELETE FROM ratings WHERE userId = ${userId} AND movieId = ${movieId};";
    mysqli_query($mysqli, $query);
}