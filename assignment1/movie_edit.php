<?php
    require_once "movie_form.php";

    if (isEditMoviePost($_POST)) {
        $errors = validateMovieForm($_POST);
        if ($errors == null) {
            // update movie
        }
        else {
            // display errors
        }
    }
    else {
        getMovieForm($_GET['id']);
    }
?>