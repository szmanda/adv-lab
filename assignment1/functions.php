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

