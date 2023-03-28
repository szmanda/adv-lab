<?php
    require_once "functions.php";

    $movieId = '';
    if (isset($_GET['movieId']))
        $movieId = $_GET['movieId'];

    if (isset($_GET['userId']) && $movieId)
        deleteRating($_GET['userId'], $movieId);

    header("Location: movie.php?id=${movieId}");
?>