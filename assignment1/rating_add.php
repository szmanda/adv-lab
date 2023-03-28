<?php
    session_start();

    require_once "rating_form.php";

    if (isAddRatingPost($_POST)) {
        $errors = validateRatingForm($_POST);
        if (empty($errors)) {
            $movieId = $_POST['movieId'];
            insertRating($_POST['userId'], $movieId, $_POST['rating'], time());
            header("Location: movie.php?id=${movieId}");
        }
        else {
            // display errors
        }
    }
    else {
        $userId = '';
        $movieId = '';

        if (isset($_SESSION['userId']))
            $userId = $_SESSION['userId'];
            
        if (isset($_GET['movieId']))
            $movieId = $_GET['movieId'];

        getRatingForm($userId, $movieId);
    }
?>