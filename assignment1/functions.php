<?php

require_once('database.php');

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

function deleteMovie($id) {
    global $mysqli;
    $query = "DELETE FROM movies WHERE id = ${id}";
    mysqli_query($mysqli, $query);
}

function deleteRating() {
    // TODO what is the pk
}

function deleteTag() {
    // TODO what is the pk
}