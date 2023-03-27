<?php
    require_once "movie_form.php";

    if (isAddMoviePost($_POST)) {
        $errors = validateMovieForm($_POST);
        if (empty($errors)) {
            insertMovie($_POST['title'], $_POST['genres']);
            header("Location: index.php");
        }
        else {
            // display errors
        }
    }
    else {
        getMovieForm();
    }
?>