<?php

require_once('database.php');

function getMovies($start = 0, $limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM movies ORDER BY id LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $movies = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $movies[] = $row;
    }
    return $movies;
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
    $sql = "SELECT * FROM ratings WHERE movieId = ${movieId} ORDER BY movieId LIMIT ${start},${limit}";
    $result = $mysqli->query($sql);
    $ratings = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $ratings[] = $row;
    }
    return $ratings;
}