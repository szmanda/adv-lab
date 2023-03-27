<?php
    require_once "movie_form.php";

    if (isAddMoviePost($_POST)) {
        $errors = validateMovieForm($_POST);
        if ($errors == null) {
            // insert movie
        }
        else {
            // display errors
        }
    }
    else {
        getMovieForm();
    }
?>