<?php
    require_once "functions.php";
    require_once "rating_form.php";

    if (isset($_GET['userId']) && isset($_GET['movieId']) && isset($_GET['rating'])) {
        $errors = validateRatingForm($_POST);
        if (empty($errors)) {
            deleteRating($_GET['userId'], $_GET['movieId'], $_GET['rating']);
            header("Location: movie.php?id=".$_GET['movieId']);
        }
    }
    header('Location: movie.php?id='.$_GET['movieId'].'&error=1');
?>