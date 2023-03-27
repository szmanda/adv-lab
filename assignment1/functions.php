<?php

require_once('database.php');

function getMovies($limit = 10) {
    global $mysqli;
    $sql = "SELECT * FROM movies ORDER BY id DESC LIMIT ${limit}";
    $result = $mysqli->query($sql);
    $movies = Array();
    while ($row = mysqli_fetch_assoc($result)) {
        $movies[] = $row;
    }
    return $movies;
}

