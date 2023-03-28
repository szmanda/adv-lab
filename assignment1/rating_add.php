<?php
    require_once "rating_form.php";
    require_once "functions.php";

    if (isAddRatingPost($_POST)) {
        $errors = validateRatingForm($_POST);
        if (empty($errors)) {
            insertRating($_POST['userId'], $_POST['movieId'], $_POST['rating']);
            header("Location: movie.php?id=".$_POST['movieId']);
        }
        else {
            // display errors
        }
    }
    else {
        getRatingForm($_GET['movieId']);
    }
?>