<?php
    require_once "movie_form.php";

    if (isEditMoviePost($_POST)) {
        $errors = validateMovieForm($_POST);
        if (empty($errors)) {
            updateMovie($_POST['id'], $_POST['title'], $_POST['genres']);
            $id = $_POST['id'];
            header("Location: movie.php?id=${id}");
        }
        else {
            // display errors
        }
    }
    else {
        getMovieForm($_GET['id']);
    }
?>