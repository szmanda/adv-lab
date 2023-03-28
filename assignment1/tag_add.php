<?php
    require_once "tag_form.php";
    require_once "functions.php";

    if (isAddTagPost($_POST)) {
        $errors = validateTagForm($_POST);
        if (empty($errors)) {
            insertTag($_POST['userId'], $_POST['movieId'], $_POST['tag']);
            header("Location: movie.php?id=".$_POST['movieId']);
        }
        else {
            // display errors
        }
    }
    else {
        getTagForm($_GET['movieId']);
    }
?>